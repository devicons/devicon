from typing import List
import xml.etree.ElementTree as et
from pathlib import Path
import os
import json
import platform
import sys
import traceback


def exit_with_err(err: Exception):
    """
    Exit the current step and display the err.
    :param: err, the error/exception encountered.
    """
    traceback.print_exc()
    sys.exit(1)


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
        err_msg = [f"{svg_path.name}:"]

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
    return 'None'


def set_env_var(key: str, value: str, delimiter: str='~'):
    """
    Set the GitHub env variable of 'key' to 'value' using
    the method specified here:
    https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-commands-for-github-actions#setting-an-environment-variable
    Support both Windows and Ubuntu machines provided by GitHub Actions.

    :param: key, the name of the env variable.
    :param: value, the value of the env variable.
    :param: delimiter, the delimiter that you want to use
    to write to the file. Only applicable if the 'value' contains
    '\n' character aka a multiline string.
    """
    if platform.system() == "Windows":
        if "\n" in value:
            os.system(f'echo "{key}<<{delimiter}" >> %GITHUB_ENV%')
            os.system(f'echo "{value}" >> %GITHUB_ENV%')
            os.system(f'echo "{delimiter}" >> %GITHUB_ENV%')
        else:
            os.system(f'echo "{key}={value}" >> %GITHUB_ENV%')
    elif platform.system() == "Linux":
        if "\n" in value:
            os.system(f'echo "{key}<<{delimiter}" >> $GITHUB_ENV')
            os.system(f'echo "{value}" >> $GITHUB_ENV')
            os.system(f'echo "{delimiter}" >> $GITHUB_ENV')
        else:
            os.system(f'echo "{key}={value}" >> $GITHUB_ENV')
    else:
        raise Exception("This function doesn't support this platform: " + platform.system())