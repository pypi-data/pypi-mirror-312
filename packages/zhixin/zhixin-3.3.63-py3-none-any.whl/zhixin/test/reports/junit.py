import datetime
import os
import xml.etree.ElementTree as ET

import click

from zhixin import __version__
from zhixin.test.reports.base import TestReportBase
from zhixin.test.result import TestStatus


class JunitTestReport(TestReportBase):
    def generate(self, output_path, verbose=False):
        if os.path.isdir(output_path):
            output_path = os.path.join(
                output_path,
                "zx-test-report-%s-%s-junit.xml"
                % (
                    os.path.basename(self.test_result.project_dir),
                    datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                ),
            )

        with open(output_path, mode="wb") as fp:
            self.build_xml_tree().write(fp, encoding="utf8")

        if verbose:
            click.secho(f"Saved JUnit report to the {output_path}", fg="green")

    def build_xml_tree(self):
        root = ET.Element("testsuites")
        root.set("name", self.test_result.project_dir)
        root.set("zhixin_version", __version__)
        root.set("tests", str(self.test_result.case_nums))
        root.set("errors", str(self.test_result.get_status_nums(TestStatus.ERRORED)))
        root.set("failures", str(self.test_result.get_status_nums(TestStatus.FAILED)))
        root.set("time", str(self.test_result.duration))
        for suite in self.test_result.suites:
            root.append(self.build_testsuite_node(suite))
        return ET.ElementTree(root)

    def build_testsuite_node(self, test_suite):
        element = ET.Element("testsuite")
        element.set("name", f"{test_suite.env_name}:{test_suite.test_name}")
        element.set("tests", str(len(test_suite.cases)))
        element.set("errors", str(test_suite.get_status_nums(TestStatus.ERRORED)))
        element.set("failures", str(test_suite.get_status_nums(TestStatus.FAILED)))
        element.set("skipped", str(test_suite.get_status_nums(TestStatus.SKIPPED)))
        element.set("time", str(test_suite.duration))
        if test_suite.timestamp:
            element.set(
                "timestamp",
                datetime.datetime.fromtimestamp(test_suite.timestamp).strftime(
                    "%Y-%m-%dT%H:%M:%S"
                ),
            )
        for test_case in test_suite.cases:
            element.append(self.build_testcase_node(test_case))
        return element

    def build_testcase_node(self, test_case):
        element = ET.Element("testcase")
        element.set("name", str(test_case.name))
        element.set("time", str(test_case.duration))
        element.set("status", str(test_case.status.name))
        if test_case.source:
            element.set("file", test_case.source.filename)
            element.set("line", str(test_case.source.line))
        if test_case.status == TestStatus.SKIPPED:
            element.append(ET.Element("skipped"))
        elif test_case.status == TestStatus.ERRORED:
            element.append(self.build_testcase_error_node(test_case))
        elif test_case.status == TestStatus.FAILED:
            element.append(self.build_testcase_failure_node(test_case))
        return element

    @staticmethod
    def build_testcase_error_node(test_case):
        element = ET.Element("error")
        element.set("type", test_case.exception.__class__.__name__)
        element.set("message", str(test_case.exception))
        if test_case.stdout:
            element.text = test_case.stdout
        return element

    @staticmethod
    def build_testcase_failure_node(test_case):
        element = ET.Element("failure")
        if test_case.message:
            element.set("message", test_case.message)
        if test_case.stdout:
            element.text = test_case.stdout
        return element
