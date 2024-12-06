from pathlib import Path

from zhixin import __version__, app, fs, util
from zhixin.home.rpc.handlers.base import BaseRPCHandler
from zhixin.project.helpers import is_zhixin_project


class AppRPC(BaseRPCHandler):
    IGNORE_STORAGE_KEYS = [
        "cid",
        "coreVersion",
        "coreSystype",
        "coreCaller",
        "coreSettings",
        "homeDir",
        "projectsDir",
    ]

    @staticmethod
    def load_state():
        with app.State(
            app.resolve_state_path("core_dir", "homestate.json"), lock=True
        ) as state:
            storage = state.get("storage", {})

            # base data
            caller_id = app.get_session_var("caller_id")
            storage["cid"] = app.get_cid()
            storage["coreVersion"] = __version__
            storage["coreSystype"] = util.get_systype()
            storage["coreCaller"] = str(caller_id).lower() if caller_id else None
            storage["coreSettings"] = {
                name: {
                    "description": data["description"],
                    "default_value": data["value"],
                    "value": app.get_setting(name),
                }
                for name, data in app.DEFAULT_SETTINGS.items()
            }

            storage["homeDir"] = fs.expanduser("~")
            storage["projectsDir"] = storage["coreSettings"]["projects_dir"]["value"]

            # skip non-existing recent projects
            storage["recentProjects"] = list(
                set(
                    str(Path(p).resolve())
                    for p in storage.get("recentProjects", [])
                    if is_zhixin_project(p)
                )
            )

            state["storage"] = storage
            state.modified = False  # skip saving extra fields
            return state.as_dict()

    @staticmethod
    def get_state():
        return AppRPC.load_state()

    @staticmethod
    def save_state(state):
        with app.State(
            app.resolve_state_path("core_dir", "homestate.json"), lock=True
        ) as s:
            s.clear()
            s.update(state)
            storage = s.get("storage", {})
            for k in AppRPC.IGNORE_STORAGE_KEYS:
                if k in storage:
                    del storage[k]
        return True
