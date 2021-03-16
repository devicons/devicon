from enum import Enum
from typing import List
import xml.etree.ElementTree as et
from pathlib import Path


# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets import filehandler, arg_getters
from build_assets import util


class SVG_STATUS_CODE(Enum):
    """
    The status codes to check for in post_check_svgs_comment.yml
    """
    NO_SVG = 0  # action: do nothing
    SVG_OK = 1  # action: let user know their svgs are fine


def main():
    """
    Check the quality of the svgs.
    If any svg error is found, create a json file called 'svg_err_messages.json'
    in the root folder that will contains the error messages.
    """
    args = arg_getters.get_check_svgs_on_pr_args()
    try:
        # check the svgs
        svgs = filehandler.get_added_modified_svgs(args.files_added_json_path,
            args.files_modified_json_path)
        print("SVGs to check: ", *svgs, sep='\n')

        if len(svgs) == 0:
            print("No SVGs to check, ending script.")
            err_messages = SVG_STATUS_CODE.NO_SVG.value
        else:
            err_messages = check_svgs(svgs)

        filehandler.write_to_file("./svg_err_messages.txt", str(err_messages))
        print("Task completed.")
    except Exception as e:
        util.exit_with_err(e)


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
        tree = et.parse(svg_path)
        root = tree.getroot()
        namespace = "{http://www.w3.org/2000/svg}"
        err_msg = [f"{svg_path}:"]

        if root.tag != f"{namespace}svg":
            err_msg.append(f"-root is '{root.tag}'. Root must be an 'svg' element")

        if root.get("viewBox") != "0 0 128 128":
            err_msg.append("-'viewBox' is not '0 0 128 128' -> Set it or scale the file using https://www.iloveimg.com/resize-image/resize-svg")

        acceptable_size = [None, "128px", "128"]
        if root.get("height") not in acceptable_size:
            err_msg.append("-'height' is present in svg element but is not '128' or '128px' -> Remove it or set it to '128' or '128px'")

        if root.get("width") not in acceptable_size:
            err_msg.append("-'width' is present in svg element but is not '128' or '128px' -> Remove it or set it to '128' or '128px'")

        if root.get("style") is not None and "enable-background" in root.get("style"):
            err_msg.append("-deprecated 'enable-background' in style attribute -> Remove it")

        if root.get("x") is not None:
            err_msg.append("-unneccessary 'x' attribute in svg element -> Remove it")

        if root.get("y") is not None:
            err_msg.append("-unneccessary 'y' attribute in svg element -> Remove it")

        style = root.findtext(f".//{namespace}style")
        if style != None and "fill" in style:
            err_msg.append("-contains style declaration using 'fill' -> Replace classes with the 'fill' attribute instead")

        if len(err_msg) > 1:
            err_msgs.append("\n".join(err_msg))

    if len(err_msgs) > 0:
        return "\n\n".join(err_msgs)
    return SVG_STATUS_CODE.SVG_OK.value


if __name__ == "__main__":
    main()
