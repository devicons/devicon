import requests
from build_assets import arg_getters
import re

def main():
    print("Please wait a few seconds...")
    args = arg_getters.get_release_message_args()
    queryPath = "https://api.github.com/repos/devicons/devicon/pulls?accept=application/vnd.github.v3+json&state=closed&per_page=100"
    stopPattern = r"^(r|R)elease v"
    headers = {
        "Authorization": f"token {args.token}"
    }

    response = requests.get(queryPath, headers=headers)
    if response.status_code != 200:
        print(f"Can't query the GitHub API. Status code is {response.status_code}")
        return

    data = response.json()
    newIcons = []
    features = []

    for pullData in data:
        if re.search(stopPattern, pullData["title"]):
            break

        authors = findAllAuthors(pullData, headers)
        markdown = f"- [{pullData['title']}]({pullData['html_url']}) by {authors}."

        if isFeatureIcon(pullData):
            newIcons.append(markdown)
        else:
            features.append(markdown)

    thankYou = "A huge thanks to all our maintainers and contributors for making this release possible!"
    iconTitle = "**{} New Icons**\n".format(len(newIcons))
    featureTitle = "**{} New Features**\n".format(len(features))
    finalString = "{0}\n\n {1}{2}\n\n {3}{4}".format(thankYou, 
        iconTitle, "\n".join(newIcons), featureTitle, "\n".join(features))

    print("--------------Here is the build message--------------\n", finalString)


"""
 Check whether the pullData is a feature:icon PR.
 :param pullData 
 :return true if the pullData has a label named "feature:icon"
"""
def isFeatureIcon(pullData):
    for label in pullData["labels"]:
        if label["name"] == "feature:icon":
            return True
    return False


"""
Find all the authors of a PR based on its commits.
:param pullData - the data of a pull request.
"""
def findAllAuthors(pullData, authHeader):
    response = requests.get(pullData["commits_url"], headers=authHeader)
    if response.status_code != 200:
        print(f"Can't query the GitHub API. Status code is {response.status_code}")
        print("Response is: ", response.text)
        return

    commits = response.json()
    authors = set()  # want unique authors only
    for commit in commits:
        authors.add("@" + commit["author"]["login"]) 
    return ", ".join(list(authors))


if __name__ == "__main__":
    main()
