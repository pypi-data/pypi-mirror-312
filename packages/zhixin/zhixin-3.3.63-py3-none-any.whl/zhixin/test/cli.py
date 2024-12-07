import os
import shutil
import subprocess

import click

from zhixin import app, exception, fs, util
from zhixin.project.config import ProjectConfig
from zhixin.test.helpers import list_test_suites
from zhixin.test.reports.base import TestReportFactory
from zhixin.test.result import TestResult, TestStatus
from zhixin.test.runners.base import TestRunnerOptions
from zhixin.test.runners.factory import TestRunnerFactory


@click.command("test", short_help="Unit Testing")
@click.option("--environment", "-e", multiple=True)
@click.option(
    "--filter",
    "-f",
    multiple=True,
    metavar="PATTERN",
    help="Filter tests by a pattern",
)
@click.option(
    "--ignore",
    "-i",
    multiple=True,
    metavar="PATTERN",
    help="Ignore tests by a pattern",
)
@click.option("--upload-port")
@click.option("--test-port")
@click.option(
    "-d",
    "--project-dir",
    default=os.getcwd,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
)
@click.option(
    "-c",
    "--project-conf",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
)
@click.option("--without-building", is_flag=True)
@click.option("--without-uploading", is_flag=True)
@click.option("--without-testing", is_flag=True)
@click.option("--no-reset", is_flag=True)
@click.option(
    "--monitor-rts",
    default=None,
    type=click.IntRange(0, 1),
    help="Set initial RTS line state for Serial Monitor",
)
@click.option(
    "--monitor-dtr",
    default=None,
    type=click.IntRange(0, 1),
    help="Set initial DTR line state for Serial Monitor",
)
@click.option(
    "-a",
    "--program-arg",
    "program_args",
    multiple=True,
    help="A program argument (multiple are allowed)",
)
@click.option("--list-tests", is_flag=True)
@click.option("--json-output", is_flag=True)
@click.option("--json-output-path", type=click.Path())
@click.option("--junit-output-path", type=click.Path())
@click.option(
    "--verbose",
    "-v",
    count=True,
    help="Increase verbosity level, maximum is 3 levels (-vvv), see docs for details",
)
@click.pass_context
def cli(  # pylint: disable=too-many-arguments,too-many-locals,redefined-builtin
    ctx,
    environment,
    ignore,
    filter,
    upload_port,
    test_port,
    project_dir,
    project_conf,
    without_building,
    without_uploading,
    without_testing,
    no_reset,
    monitor_rts,
    monitor_dtr,
    program_args,
    list_tests,
    json_output,
    json_output_path,
    junit_output_path,
    verbose,
):
    app.set_session_var("custom_project_conf", project_conf)

    with fs.cd(project_dir):
        project_config = ProjectConfig.get_instance(project_conf)
        project_config.validate(envs=environment)

        test_result = TestResult(project_dir)
        test_suites = list_test_suites(
            project_config, environments=environment, filters=filter, ignores=ignore
        )
        test_names = sorted(set(s.test_name for s in test_suites))

        if not verbose:
            click.echo("Verbosity level can be increased via `-v, -vv, or -vvv` option")
        click.secho("Collected %d tests" % len(test_names), bold=True, nl=not verbose)
        if verbose:
            click.echo(" (%s)" % ", ".join(test_names))

        for test_suite in test_suites:
            test_result.add_suite(test_suite)
            if list_tests or test_suite.is_finished():  # skipped by user
                continue
            runner = TestRunnerFactory.new(
                test_suite,
                project_config,
                TestRunnerOptions(
                    verbose=verbose,
                    without_building=without_building,
                    without_uploading=without_uploading,
                    without_testing=without_testing,
                    upload_port=upload_port,
                    test_port=test_port,
                    no_reset=no_reset,
                    monitor_rts=monitor_rts,
                    monitor_dtr=monitor_dtr,
                    program_args=program_args,
                ),
            )
            click.echo()
            print_suite_header(test_suite)
            runner.start(ctx)
            print_suite_footer(test_suite)

    stdout_report = TestReportFactory.new("stdout", test_result)
    stdout_report.generate(verbose=verbose or list_tests)

    for output_format, output_path in [
        ("json", subprocess.STDOUT if json_output else None),
        ("json", json_output_path),
        ("junit", junit_output_path),
    ]:
        if not output_path:
            continue
        custom_report = TestReportFactory.new(output_format, test_result)
        custom_report.generate(output_path=output_path, verbose=True)

    # Reset custom project config
    app.set_session_var("custom_project_conf", None)

    if test_result.is_errored or test_result.get_status_nums(TestStatus.FAILED):
        raise exception.ReturnErrorCode(1)


def print_suite_header(test_suite):
    click.echo(
        "Processing %s in %s environment"
        % (
            click.style(test_suite.test_name, fg="yellow", bold=True),
            click.style(test_suite.env_name, fg="cyan", bold=True),
        )
    )
    terminal_width = shutil.get_terminal_size().columns
    click.secho("-" * terminal_width, bold=True)


def print_suite_footer(test_suite):
    is_error = test_suite.status in (TestStatus.FAILED, TestStatus.ERRORED)
    util.print_labeled_bar(
        "%s [%s] Took %.2f seconds"
        % (
            click.style(
                "%s:%s" % (test_suite.env_name, test_suite.test_name), bold=True
            ),
            (
                click.style(test_suite.status.name, fg="red", bold=True)
                if is_error
                else click.style("PASSED", fg="green", bold=True)
            ),
            test_suite.duration,
        ),
        is_error=is_error,
        sep="-",
    )
