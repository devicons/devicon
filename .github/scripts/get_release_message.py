import requests
from build_assets import arg_getters, api_handler
import re

def main():
    print("Please wait a few seconds...")
    args = arg_getters.get_release_message_args()

    # fetch first page by default
    data = api_handler.get_merged_pull_reqs_since_last_release(args.token)
    newIcons = []
    features = []

    print("Parsing through the pull requests")
    for pullData in data:
        authors = api_handler.find_all_authors(pullData, args.token)
        markdown = f"- [{pullData['title']}]({pullData['html_url']}) by {authors}."

        if api_handler.is_feature_icon(pullData):
            newIcons.append(markdown)
        else:
            features.append(markdown)

    print("Constructing message")
    thankYou = "A huge thanks to all our maintainers and contributors for making this release possible!"
    iconTitle = f"**{len(newIcons)} New Icons**"
    featureTitle = f"**{len(features)} New Features**"
    finalString = "{0}\n\n {1}\n{2}\n\n {3}\n{4}".format(thankYou, 
        iconTitle, "\n".join(newIcons), featureTitle, "\n".join(features))

    print("--------------Here is the build message--------------\n", finalString)
    print("Script finished")
    

if __name__ == "__main__":
    main()
