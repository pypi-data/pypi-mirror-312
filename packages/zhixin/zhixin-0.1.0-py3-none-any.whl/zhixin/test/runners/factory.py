import importlib
import os
import re

from zhixin.compat import load_python_module
from zhixin.exception import UserSideException
from zhixin.project.config import ProjectConfig
from zhixin.test.result import TestSuite
from zhixin.test.runners.base import TestRunnerBase, TestRunnerOptions


class TestRunnerFactory:
    @staticmethod
    def get_clsname(name):
        name = re.sub(r"[^\da-z\_\-]+", "", name, flags=re.I)
        return "%sTestRunner" % name.lower().capitalize()

    @classmethod
    def new(cls, test_suite, project_config, options=None) -> TestRunnerBase:
        assert isinstance(test_suite, TestSuite)
        assert isinstance(project_config, ProjectConfig)
        if options:
            assert isinstance(options, TestRunnerOptions)
        test_framework = project_config.get(
            f"env:{test_suite.env_name}", "test_framework"
        )
        module_name = f"zhixin.test.runners.{test_framework}"
        runner_cls = None
        if test_framework == "custom":
            test_dir = project_config.get("zhixin", "test_dir")
            custom_runner_path = os.path.join(test_dir, "test_custom_runner.py")
            test_name = test_suite.test_name if test_suite.test_name != "*" else None
            while test_name:
                if os.path.isfile(
                    os.path.join(test_dir, test_name, "test_custom_runner.py")
                ):
                    custom_runner_path = os.path.join(
                        test_dir, test_name, "test_custom_runner.py"
                    )
                    break
                test_name = os.path.dirname(test_name)  # parent dir

            try:
                mod = load_python_module(module_name, custom_runner_path)
            except (FileNotFoundError, ImportError) as exc:
                raise UserSideException(
                    "Could not find custom test runner "
                    f"by this path -> {custom_runner_path}"
                ) from exc
        else:
            mod = importlib.import_module(module_name)
        runner_cls = getattr(mod, cls.get_clsname(test_framework))
        return runner_cls(test_suite, project_config, options)
