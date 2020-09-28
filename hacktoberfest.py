#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import requests
import os
import json


HACKTOBERFEST_LABEL = "Hacktoberfest"


class Github(object):
    GITHUB_API_URL = "https://api.github.com"

    def __init__(self, repository=None, token=None):
        self._token = token or os.getenv("GITHUB_OAUTH_TOKEN", None)
        if not self._token:
            raise ValueError("'GITHUB_OAUTH_TOKEN' must be configure in your environment")
        self._repository = repository or os.getenv("GITHUB_REPO", "conan-io/conan")

    def _auth(self):
        return {"Authorization": "token {}".format(self._token)}

    def add_label(self, issue, label):
        url = f"{Github.GITHUB_API_URL}/repos/{self._repository}/issues/{issue}/labels"
        headers = self._auth()
        headers["Content-Type"] = "application/json"
        response = requests.post(url=url, headers=headers, data=json.dumps({"labels": [label]}))
        if not response.ok:
            raise Exception(response.text)
        return response.json()

    def get_issues(self, label):
        url = f"{Github.GITHUB_API_URL}/repos/{self._repository}/issues"
        response = requests.get(url=url, headers=self._auth(), params={"labels": label})
        if not response.ok:
            raise Exception(response.text)
        issues = []
        for issue in response.json():
            print(f"ISSUE: {issue['number']}")
            issues.append(issue["number"])
        return issues


def get_arguments():
    parser = argparse.ArgumentParser(description="Apply Hacktoberfest label to Github issues.")
    parser.add_argument("--token", type=str, help="Github API Token")
    parser.add_argument("--repository", type=str, help="Github organization/repository name", default="conan-io/conan")
    parser.add_argument("--issue", "-i", type=int, help="Update only one Github issue")
    parser.add_argument("--label", "-l", type=str, help="Update ALL issues based on label name", default="good first issue")
    return parser.parse_args()


def main():
    args = get_arguments()
    github = Github(repository=args.repository, token=args.token)
    if args.issue:
        print(f"Adding label '{HACKTOBERFEST_LABEL}' to issue #{args.issue}")
        github.add_label(args.issue, HACKTOBERFEST_LABEL)
    elif args.label:
        issues = github.get_issues(args.label)
        for issue in issues:
            print(f"Adding label '{HACKTOBERFEST_LABEL}' to issue #{issue}")
            github.add_label(issue, HACKTOBERFEST_LABEL)


if __name__ == "__main__":
    main()
