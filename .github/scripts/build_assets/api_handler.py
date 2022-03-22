import requests
import sys
import re


def get_merged_pull_reqs_since_last_release(token):
    """
    Get all the merged pull requests since the last release.
    """
    stopPattern = r"^(r|R)elease v"
    pull_reqs = []
    found_last_release = False
    page = 1

    print("Getting PRs since last release.")
    while not found_last_release:
        data = get_merged_pull_reqs(token, page)
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


def get_merged_pull_reqs(token, page):
    """
    Get the merged pull requests based on page. There are 
    100 results per page. See https://docs.github.com/en/rest/reference/pulls
    for more details on the parameters.
    :param token, a GitHub API token.
    :param page, the page number.
    """
    queryPath = "https://api.github.com/repos/devicons/devicon/pulls"
    headers = {
        "Authorization": f"token {token}"
    }
    params = {
        "accept": "application/vnd.github.v3+json",
        "state": "closed",
        "per_page": 100,
        "page": page
    }

    print(f"Querying the GitHub API for requests page #{page}")
    response = requests.get(queryPath, headers=headers, params=params)
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
