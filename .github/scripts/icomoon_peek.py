from typing import List
import re
import sys
from selenium.common.exceptions import TimeoutException
import xml.etree.ElementTree as et

# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets.SeleniumRunner import SeleniumRunner
from build_assets import filehandler, arg_getters


def main():
    args = arg_getters.get_selenium_runner_args(True)
    new_icons = filehandler.find_new_icons(args.devicon_json_path, args.icomoon_json_path)

    # get only the icon object that has the name matching the pr title
    filtered_icons = find_object_added_in_this_pr(new_icons, args.pr_title)

    if len(new_icons) == 0:
        sys.exit("No files need to be uploaded. Ending script...")

    if len(filtered_icons) == 0:
        message = "No icons found matching the icon name in the PR's title.\n" \
        "Ensure that the PR title matches the convention here: \n" \
        "https://github.com/devicons/devicon/blob/master/CONTRIBUTING.md#overview.\n" \
        "Ending script...\n"
        sys.exit(message)

    # print list of new icons
    print("List of new icons:", *new_icons, sep = "\n")
    print("Icons being uploaded:", *filtered_icons, sep = "\n", end='\n\n')

    runner = None
    try:
        # check the svgs
        svgs = filehandler.get_svgs_paths(filtered_icons, args.icons_folder_path)
        check_svgs(svgs)

        # check icon
        runner = SeleniumRunner(args.download_path, args.geckodriver_path, args.headless)
        svgs = filehandler.get_svgs_paths(filtered_icons, args.icons_folder_path, True)
        screenshot_folder = filehandler.create_screenshot_folder("./") 
        runner.upload_svgs(svgs, screenshot_folder)
        print("Task completed.")
    except TimeoutException as e:
        sys.exit("Selenium Time Out Error: \n" + str(e))
    except Exception as e:
        sys.exit(e)
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


def check_svgs(svg_file_paths: List[str]):
    """
    Check the width, height, viewBox and style of each svgs passed in.
    The viewBox must be '0 0 128 128'.
    If the svg has a width and height attr, ensure it's '128px'.
    The style must not contain any 'fill' declarations.
    If any error is found, they will be thrown.
    :param: svg_file_paths, the file paths to the svg to check for.
    """
    # batch err messages together so user can fix everything at once
    err_msgs = []
    for svg_path in svg_file_paths:
        tree = et.parse(svg_path)
        root = tree.getroot()
        namespace = "{http://www.w3.org/2000/svg}"

        if root.tag != f"{namespace}svg":
            err_msgs.append(f"Root is '{root.tag}'. Root must be an 'svg' element: {svg_path}")

        if root.get("viewBox") != "0 0 128 128":
            err_msgs.append("SVG 'viewBox' is not '0 0 128 128': " + svg_path)

        acceptable_size = [None, "128px", "128"]
        if root.get("height") not in acceptable_size:
            err_msgs.append("SVG 'height' is present but is not '128' or '128px': " + svg_path)

        if root.get("width") not in acceptable_size:
            err_msgs.append("SVG 'width' is present but is not '128' or '128px': " + svg_path)

        style = root.findtext(f".//{namespace}style")
        if style != None and "fill" in style:
            err_msgs.append("Found 'fill' in <style>. Use the 'fill' attribute instead: " + svg_path)

    if len(err_msgs) > 0:
        raise Exception("\n" + "\n".join(err_msgs))


if __name__ == "__main__":
    main()
