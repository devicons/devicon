import requests
import sys
import re
from typing import List
from io import FileIO


# our base url which leads to devicon
base_url = "https://api.github.com/repos/devicons/devicon/"

def get_merged_pull_reqs_since_last_release(token, log_output: FileIO=sys.stdout):
    """
    Get all the merged pull requests since the last release.
    """
    stopPattern = r"^(r|R)elease v"
    pull_reqs = []
    found_last_release = False
    page = 1

    while not found_last_release:
        data = get_merged_pull_reqs(token, page, log_output)
        # assume we don't encounter it during the loop
        last_release_index = 101 

        for i in range(len(data)):
            if re.search(stopPattern, data[i]["title"]):
                found_last_release = True
                last_release_index = i
                break
        pull_reqs.extend(data[:last_release_index])
        page += 1

    # should contain all the PRs since last release
    return pull_reqs


def get_merged_pull_reqs(token, page, log_output: FileIO=sys.stdout):
    """
    Get the merged pull requests based on page. There are 
    100 results per page. See https://docs.github.com/en/rest/reference/pulls
    for more details on the parameters.
    :param token, a GitHub API token.
    :param page, the page number.
    """
    url = base_url + "pulls"
    headers = {
        "Authorization": f"token {token}"
    }
    params = {
        "accept": "application/vnd.github.v3+json",
        "state": "closed",
        "per_page": 100,
        "page": page
    }

    print(f"Querying the GitHub API for requests page #{page}", file=log_output)
    response = requests.get(url, headers=headers, params=params)
    if not response:
        print(f"Can't query the GitHub API. Status code is {response.status_code}. Message is {response.text}")
        sys.exit(1)

    closed_pull_reqs = response.json()
    return [merged_pull_req 
        for merged_pull_req in closed_pull_reqs 
        if merged_pull_req["merged_at"] is not None]


def is_feature_icon(pull_req_data):
    """
    Check whether the pullData is a feature:icon PR.
    :param pull_req_data - the data on a specific pull request from GitHub.
    :return true if the pullData has a label named "feature:icon"
    """
    for label in pull_req_data["labels"]:
        if label["name"] == "feature:icon":
            return True
    return False


def find_all_authors(pull_req_data, token):
    """
    Find all the authors of a PR based on its commits.
    :param pull_req_data - the data on a specific pull request from GitHub.
    :param token - a GitHub API token.
    """
    headers = {
        "Authorization": f"token {token}"
    }
    response = requests.get(pull_req_data["commits_url"], headers=headers)
    if not response:
        print(f"Can't query the GitHub API. Status code is {response.status_code}")
        print("Response is: ", response.text)
        return

    commits = response.json()
    authors = set()  # want unique authors only
    for commit in commits:
        try:
            # this contains proper referenceable github name
            authors.add(commit["author"]["login"]) 
        except TypeError:
            # special case
            authors.add(commit["commit"]["author"]["name"]) 
            print(f"This URL didn't have an `author` attribute: {pull_req_data['commits_url']}")
    return ", ".join(["@" + author for author in list(authors)])


def label_issues(token: str, issues: List[str], labels: List[str]):
    """
    Label the issues specified with the label specified.
    :param token: the GitHub API token.
    :param issues: the issue numbers (as str) that we are labelling.
    :param labels: the labels that we are labelling.
    """
    headers = {
        "Authorization": f"token {token}",
        "accept": "application/vnd.github.v3+json"
    }
    url = base_url + "issues/{}/labels"
    for issue in issues:
        body = {
            "labels": labels
        }
        response = requests.post(url.format(issue), headers=headers, json=body)
        if not response:
            raise Exception(f"Can't label the Issue provided. Issue: {issue}, labels: {labels}, API response: " + response.text)
        else:
            print(f"Successfully labelled issue {issue}")


def close_issues(token: str, issues: List[str]):
    """
    Close issues.
    :param token: the GitHub API token.
    :param issues: the issue numbers (as str) that we are labelling.
    """
    headers = {
        "Authorization": f"token {token}",
        "accept": "application/vnd.github.v3+json"
    }
    url = base_url + "issues/{}"
    body = {
        "state": "closed"
    }
    for issue in issues:
        response = requests.patch(url.format(issue), headers=headers, json=body)
        if not response:
            raise Exception(f"Can't close Issue provided. Issue: {issue}, API response: " + response.text)
        else:
            print(f"Successfully closed issue {issue}")


def get_issues_by_labels(token: str, labels: List[str]):
    """
    Get a list of issues based on their labels.
    :param token: the GitHub API token.
    :param labels: the labels that we are labelling.
    """
    url = base_url + "issues?per_page=100&labels={}&page={}"
    headers = {
        "Authorization": f"token {token}",
        "accept": "application/vnd.github.v3+json"
    }
    issues = []
    done = False
    page_num = 1
    while not done:
        response = requests.get(url.format(",".join(labels), page_num), headers=headers)
        if not response:
            raise Exception(f"Can't access API. Can't get issues for labels: {labels}, API response: " + response.text)
        else:
            results = response.json()
            if len(results) < 100:
                done = True # we are done
            else:
                page_num += 1 # page is full => might need to check another page

            # GitHub API also returns PRs for issues queries => have to check
            issues_only = [issue for issue in results if issue.get("pull_request") is None]
            issues.extend(issues_only)

    return issues


def get_pr_by_number(token: str, pr_num: str):
    url = base_url + "pulls/" + pr_num
    headers = {
        "Authorization": f"token {token}"
    }

    print(f"Querying the GitHub API for requests")
    response = requests.get(url, headers=headers)
    if not response:
        print(f"Can't query the GitHub API. Status code is {response.status_code}. Message is {response.text}")
        sys.exit(1)

    pr = response.json()
    return pr
