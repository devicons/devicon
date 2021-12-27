from enum import Enum
from typing import List
import xml.etree.ElementTree as et
from pathlib import Path


# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets import filehandler, arg_getters, util


class SVG_STATUS_CODE(Enum):
    """
    The status codes to check for in post_check_svgs_comment.yml
    """
    NO_SVG = 0  # action: do nothing
    SVG_OK = 1  # action: let user know their svgs are fine


def main():
    """
    Check the quality of the svgs IF this is an icon PR. Else, does nothing.
    If any svg error is found, create a json file called 'svg_err_messages.json'
    in the root folder that will contains the error messages.
    """
    args = arg_getters.get_check_icon_pr_args()
    try:
        all_icons = filehandler.get_json_file_content(args.devicon_json_path)

        # get only the icon object that has the name matching the pr title
        filtered_icon = util.find_object_added_in_pr(all_icons, args.pr_title)
        devicon_err_msg = check_devicon_object(filtered_icon)

        # check the svgs
        svgs = filehandler.get_svgs_paths([filtered_icon], args.icons_folder_path)
        print("SVGs to check: ", *svgs, sep='\n')

        if len(svgs) == 0:
            print("No SVGs to check, ending script.")
            err_messages = str(SVG_STATUS_CODE.NO_SVG.value)
        else:
            err_messages = check_svgs(svgs)

        filehandler.write_to_file("./svg_err_messages.txt", devicon_err_msg + "\n\n" + err_messages)
        print("Task completed.")
    except Exception as e:
        filehandler.write_to_file("./svg_err_messages.txt", str(e))
        util.exit_with_err(e)


def check_devicon_object(icon: dict):
    """
    Check that the devicon object added is up to standard.
    :return a string containing the error messages if any.
    """
    err_msgs = []
    try:
        for tag in icon["tags"]:
            if type(tag) != str:
                raise TypeError()
    except TypeError:
        err_msgs.append("- 'tags' must be an array of strings, not: " + str(icon["tags"]))
    except KeyError:
        err_msgs.append("- missing key: 'tags'.")

    try:
        if type(icon["versions"]) != dict:
            err_msgs.append("- 'versions' must be an object.")
    except KeyError:
        err_msgs.append("- missing key: 'versions'.")

    try:
        if type(icon["versions"]["svg"]) != list or len(icon["versions"]["svg"]) == 0:
            err_msgs.append("- must contain at least 1 svg version in a list.")
    except KeyError:
        err_msgs.append("- missing key: 'svg' in 'versions'.")
    
    try:
        if type(icon["versions"]["font"]) != list or len(icon["versions"]["svg"]) == 0:
            err_msgs.append("- must contain at least 1 font version in a list.")
    except KeyError:
        err_msgs.append("- missing key: 'font' in 'versions'.")

    try:
        if type(icon["color"]) != str or "#" not in icon["color"]:
            err_msgs.append("- 'color' must be a string in the format '#abcdef'")
    except KeyError:
        err_msgs.append("- missing key: 'color'.")

    try:
        if type(icon["aliases"]) != list:
            err_msgs.append("- 'aliases' must be an array.")
    except KeyError:
        err_msgs.append("- missing key: 'aliases'.")
    
    if len(err_msgs) > 0:
        message = "Error found in 'devicon.json' for '{}' entry: \n{}".format(icon["name"], "\n".join(err_msgs))
        return message
    return ""


def check_svgs(svg_file_paths: List[Path]):
    """
    Check the width, height, viewBox and style of each svgs passed in.
    The viewBox must be '0 0 128 128'.
    If the svg has a width and height attr, ensure it's '128px'.
    The style must not contain any 'fill' declarations.
    If any error is found, they will be thrown.
    :param: svg_file_paths, the file paths to the svg to check for.
    :return: None if there no errors. If there is, return a JSON.stringified
    list with the error messages in it.
    """
    # batch err messages together so user can fix everything at once
    err_msgs = []
    for svg_path in svg_file_paths:
        try:
            err_msg = [f"{svg_path}:"]

            # name check
            if not util.is_svg_name_valid(svg_path.name):
                err_msg.append("-SVG file name didn't match our pattern of `name-(original|plain|line)(-wordmark)?.svg`")

            # svg check
            tree = et.parse(svg_path)
            root = tree.getroot()
            namespace = "{http://www.w3.org/2000/svg}"

            if root.tag != f"{namespace}svg":
                err_msg.append(f"-root is '{root.tag}'. Root must be an 'svg' element")

            if root.get("viewBox") != "0 0 128 128":
                err_msg.append("-'viewBox' is not '0 0 128 128' -> Set it or scale the file using https://www.iloveimg.com/resize-image/resize-svg.")

            # goes through all elems and check for strokes
            for child in tree.iter():
                if child.get("stroke") != None:
                    err_msg.append("-SVG contains `stroke` property. This will get ignored by Icomoon. Please convert them to fills.")
                    break

            if len(err_msg) > 1:
                err_msgs.append("\n".join(err_msg))
        except et.ParseError as e:
            raise Exception(f"SVG Error in file: {svg_path}. Full Error: \n" + str(e))

    if len(err_msgs) > 0:
        return "\n\n".join(err_msgs)
    return str(SVG_STATUS_CODE.SVG_OK.value)


if __name__ == "__main__":
    main()
