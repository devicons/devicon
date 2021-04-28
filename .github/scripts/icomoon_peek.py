from typing import List
import re
import sys
from selenium.common.exceptions import TimeoutException

# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets.SeleniumRunner import SeleniumRunner
from build_assets import filehandler, arg_getters
from build_assets import util


def main():
    runner = None
    try:
        args = arg_getters.get_selenium_runner_args(True)
        new_icons = filehandler.find_new_icons(args.devicon_json_path, args.icomoon_json_path)

        if len(new_icons) == 0:
            raise Exception("No files need to be uploaded. Ending script...")

        # get only the icon object that has the name matching the pr title
        filtered_icon = find_object_added_in_this_pr(new_icons, args.pr_title)
        print("Icon being checked:", filtered_icon, sep = "\n", end='\n\n')

        runner = SeleniumRunner(args.download_path, args.geckodriver_path, args.headless)
        svgs = filehandler.get_svgs_paths([filtered_icon], args.icons_folder_path, True)
        screenshot_folder = filehandler.create_screenshot_folder("./") 
        runner.upload_svgs(svgs, screenshot_folder)
        print("Task completed.")

        # no errors, do this so upload-artifact won't fail
        filehandler.write_to_file("./err_messages.txt", "0")
    except Exception as e:
        filehandler.write_to_file("./err_messages.txt", str(e))
        util.exit_with_err(e)
    finally:
        runner.close() 


def find_object_added_in_this_pr(icons: List[dict], pr_title: str):
    """
    Find the icon name from the PR title. 
    :param icons, a list of the font objects found in the devicon.json.
    :pr_title, the title of the PR that this workflow was called on.
    :return a dictionary with the "name"
    entry's value matching the name in the pr_title.
    :raise If no object can be found, raise an Exception.
    """
    try:
        pattern = re.compile(r"(?<=^new icon: )\w+ (?=\(.+\))", re.I)
        icon_name = pattern.findall(pr_title)[0].lower().strip()  # should only have one match
        icon =  [icon for icon in icons if icon["name"] == icon_name][0]
        check_devicon_object(icon, icon_name)
        return icon
    except IndexError:  # there are no match in the findall()
        raise Exception("Couldn't find an icon matching the name in the PR title.")
    except ValueError as e:
        raise Exception(str(e))


def check_devicon_object(icon: dict, icon_name: str):
    """
    Check that the devicon object added is up to standard.
    :return a string containing the error messages if any.
    """
    err_msgs = []
    try:
        if type(icon["name"]) != icon_name:
            err_msgs.append("'name' value is not: " + icon_name)
    except KeyError:
        err_msgs.append("Missing key: 'name'.")

    try:
        for tag in icon["tags"]:
            if type(tag) != str:
                raise TypeError()
    except TypeError:
        err_msgs.append("'tags' must be an array of strings, not: " + str(icon["tags"]))
    except KeyError:
        err_msgs.append("Missing key: 'tags'.")

    try:
        if type(icon["versions"]) != dict:
            err_msgs.append("'versions' must be an object.")
    except KeyError:
        err_msgs.append("Missing key: 'versions'.")

    try:
        if type(icon["versions"]["svg"]) != list or len(icon["versions"]["svg"]) == 0:
            err_msgs.append("Must contain at least 1 svg version in a list.")
    except KeyError:
        err_msgs.append("Missing key: 'svg' in 'versions'.")
    
    try:
        if type(icon["versions"]["font"]) != list or len(icon["versions"]["svg"]) == 0:
            err_msgs.append("Must contain at least 1 font version in a list.")
    except KeyError:
        err_msgs.append("Missing key: 'font' in 'versions'.")

    try:
        if type(icon["color"]) != str or "#" not in icon["color"]:
            err_msgs.append("'color' must be a string in the format '#abcdef'")
    except KeyError:
        err_msgs.append("Missing key: 'color'.")

    try:
        if type(icon["aliases"]) != list:
            err_msgs.append("'aliases' must be an array.")
    except KeyError:
        err_msgs.append("Missing key: 'aliases'.")
    
    if len(err_msgs) > 0:
        message = "Error found in 'devicon.json' for '{}' entry: \n{}\n".format(icon_name, "\n".join(err_msgs))
        raise ValueError(message)
    return ""

if __name__ == "__main__":
    main()
