import invoke as inv

from personal_mnemonic_medium.subtasks.github import (
    get_issues_assigned_to_me,
    issue_dialog,
)
from personal_mnemonic_medium.subtasks.graphite import (
    create_branch_from_issue,
    submit_pr,  # noqa: F401 # type: ignore
)

PYTEST_CMD = "pytest --durations=5 --cov=personal_mnemonic_medium personal_mnemonic_medium --cov-report xml:.coverage.xml --cov-report lcov:.coverage.lcov"


@inv.task  # type: ignore
def install_dev(c: inv.Context):
    print("--- Installing development dependencies ---")
    c.run("pip install --upgrade .[dev]")
    print("✅✅✅ Development dependencies installed ✅✅✅")


@inv.task  # type: ignore
def install_test(c: inv.Context):
    print("--- Installing development dependencies ---")
    c.run("pip install --upgrade .[dev,tests]")
    print("✅✅✅ Development dependencies installed ✅✅✅")


@inv.task  # type: ignore
def install(c: inv.Context):
    print("--- Installing dependencies ---")
    c.run("pip install --upgrade .")
    print("✅✅✅ Installed package ✅✅✅")


@inv.task  # type: ignore
def generate_coverage(c: inv.Context):
    coverage_report = c.run(PYTEST_CMD)
    if coverage_report is None:
        print("No coverage report generated")
        return

    # Find line containing "Coverage: \d%"
    lines = coverage_report.stdout.split("\n")
    coverage_line = next(
        line for line in lines if "Coverage: " in line
    )
    coverage_percent = int(coverage_line.split(" ")[1][:-1])
    if coverage_percent < 80:
        proceed = input(
            f"⚠⚠️⚠️️ Coverage is {coverage_percent}%. Proceed? [y/N] "
        )
        return


@inv.task  # type: ignore
def test(c: inv.Context):
    print("--- Testing ---")
    generate_coverage(c)
    c.run("diff-cover .coverage.xml --fail-under=80")
    print("✅✅✅ Tests passed ✅✅✅")


@inv.task  # type: ignore
def lint(c: inv.Context):
    print("--- Linting ---")
    c.run("ruff format .")
    c.run("ruff . --fix --extend-select F401 --extend-select F841")
    print("✅✅✅ Lint ✅✅✅")


@inv.task  # type: ignore
def types(c: inv.Context):
    print("--- Type-checking ---")
    c.run("pyright personal_mnemonic_medium")
    print("✅✅✅ Types ✅✅✅")


@inv.task(aliases=("next",))  # type: ignore
def branch_from_next_issue(c: inv.Context):
    my_issues = get_issues_assigned_to_me(c)

    if my_issues is None:
        print("No issues found")
        return

    selected_issue_index = issue_dialog(my_issues)
    create_branch_from_issue(
        c=c, selected_issue=my_issues[selected_issue_index]
    )


@inv.task  # type: ignore
def validate_ci(c: inv.Context):
    print("--- Validating CI ---")
    lint(c)
    types(c)
    generate_coverage(c)
    print("✅✅✅ CI valid ✅✅✅")


@inv.task(aliases=("new",))  # type: ignore
def new_branch_from_issue(c: inv.Context):
    my_issues = get_issues_assigned_to_me(c)

    if my_issues is None:
        print("No issues found")
        return

    selected_issue_index = issue_dialog(my_issues)
    c.run("git checkout main")
    c.run("git pull")
    create_branch_from_issue(
        c=c, selected_issue=my_issues[selected_issue_index]
    )
