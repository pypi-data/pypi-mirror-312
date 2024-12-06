"""Extract milestone details from JSON returned by `gh repo view --json milestones`"""

# pylint: disable=missing-function-docstring

import argparse
import json
import os
import sys

if "CI" not in os.environ:
    sys.exit("Error: You can only run this script within a GitHub workflow.")


def error(title: str, message: str):
    sys.exit(f"::error title={title}::{message}")


def run_exists_cmd():
    milestones = json.loads(arguments.milestones_json)["milestones"]
    version = os.environ["VERSION"]
    for milestone in milestones:
        if milestone["title"] == version:
            with open(os.environ["GITHUB_ENV"], encoding="utf-8", mode="a") as env_file:
                env_file.write(f"MILESTONE={milestone['number']}\n")
            sys.exit(0)
    error(
        "No such milestone",
        f"There is no {version} milestone (https://github.com/brobeson/Rayne/milestones). "
        f"Is it already closed (https://github.com/brobeson/Rayne/milestones?state=closed)?",
    )


def run_issues_cmd():
    issues = json.loads(arguments.issues_json)
    if issues:
        error(
            "Not all issues are done",
            f"Milestone {os.environ['VERSION']} has {len(issues)} open issues "
            f"(https://github.com/brobeson/Rayne/milestone/{os.environ['MILESTONE']}).",
        )
    sys.exit(0)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
exists_parser = subparsers.add_parser("exists")
exists_parser.add_argument("milestones_json")
exists_parser.set_defaults(func=run_exists_cmd)
issues_parser = subparsers.add_parser("issues")
issues_parser.add_argument("issues_json")
issues_parser.set_defaults(func=run_issues_cmd)
arguments = parser.parse_args()
arguments.func()
