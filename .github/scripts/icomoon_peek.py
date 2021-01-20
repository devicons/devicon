from typing import List
import re
import sys
from selenium.common.exceptions import TimeoutException
import xml.etree.ElementTree as et

# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets.SeleniumRunner import SeleniumRunner
from build_assets import filehandler, arg_getters
from build_assets import util


def main():
    args = arg_getters.get_selenium_runner_args(True)
    new_icons = filehandler.find_new_icons(args.devicon_json_path, args.icomoon_json_path)

    # get only the icon object that has the name matching the pr title
    filtered_icons = find_object_added_in_this_pr(new_icons, args.pr_title)

    if len(new_icons) == 0:
        sys.exit("No files need to be uploaded. Ending script...")

    if len(filtered_icons) == 0:
        message = "No icons found matching the icon name in the PR's title.\n" \
        "Ensure that a new icon entry is added in the devicon.json and the PR title matches the convention here: \n" \
        "https://github.com/devicons/devicon/blob/master/CONTRIBUTING.md#overview.\n" \
        "Ending script...\n"
        sys.exit(message)

    # print list of new icons
    print("List of new icons:", *new_icons, sep = "\n")
    print("Icons being uploaded:", *filtered_icons, sep = "\n", end='\n\n')

    runner = None
    try:
        runner = SeleniumRunner(args.download_path, args.geckodriver_path, args.headless)
        svgs = filehandler.get_svgs_paths(filtered_icons, args.icons_folder_path, True)
        screenshot_folder = filehandler.create_screenshot_folder("./") 
        runner.upload_svgs(svgs, screenshot_folder)
        print("Task completed.")
    except TimeoutException as e:
        util.exit_with_err("Selenium Time Out Error: \n" + str(e))
    except Exception as e:
        util.exit_with_err(e)
    finally:
        runner.close() 


def find_object_added_in_this_pr(icons: List[dict], pr_title: str):
    """
    Find the icon name from the PR title. 
    :param icons, a list of the font objects found in the devicon.json.
    :pr_title, the title of the PR that this workflow was called on.
    :return a list containing the dictionary with the "name"
    entry's value matching the name in the pr_title.
    If none can be found, return an empty list.
    """
    try:
        pattern = re.compile(r"(?<=^new icon: )\w+ (?=\(.+\))", re.I)
        icon_name = pattern.findall(pr_title)[0].lower().strip()  # should only have one match
        return [icon for icon in icons if icon["name"] == icon_name]
    except IndexError:  # there are no match in the findall()
        return []  




if __name__ == "__main__":
    main()
