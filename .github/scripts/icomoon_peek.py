from os import sep
from typing import List
import re
from selenium.common.exceptions import TimeoutException

# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets.SeleniumRunner import SeleniumRunner
from build_assets import filehandler, util


def main():
    args = util.get_commandline_args(True)
    new_icons = filehandler.find_new_icons(args.devicon_json_path, args.icomoon_json_path)

    # get only the icon object that has the name matching the pr title
    filtered_icons = find_object_added_in_this_pr(new_icons, args.pr_title)

    # print list of new icons
    print("List of new icons:", *new_icons, sep = "\n")
    print("Icons being uploaded:", *filtered_icons, sep = "\n")

    if len(new_icons) == 0:
        print("No files need to be uploaded. Ending script...")
        return

    screenshot_folder = filehandler.create_screenshot_folder("./") 
    if len(filtered_icons) == 0:
        print("No icons found matching the icon name in the PR's title. Fallback to uploading all new icons found.")
        screenshot_folder = ""

    runner = None
    try:
        runner = SeleniumRunner(args.download_path, args.geckodriver_path, args.headless)
        svgs = filehandler.get_svgs_paths(new_icons, args.icons_folder_path)
        runner.upload_svgs(svgs, screenshot_folder)
        print("Task completed.")
    except TimeoutException as e:
        print("Selenium Time Out Error: ", e.stacktrace, sep='\n')
    except Exception as e:
        print(e)
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
