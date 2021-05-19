from typing import List
import re
import os
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


def find_object_added_in_this_pr(icons: List[dict], pr_title: str, check_object=False):
    """
    Find the devicon.json object that has the name from the PR title. 
    :param icons, a list of the font objects found in the devicon.json.
    :param pr_title, the title of the PR that this workflow was called on.
    :param check_object, whether to check the devicon.json object that was found.
    Default false.
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
        raise Exception from e


def check_devicon_object(icon: dict, icon_name: str):
    """
    Check that the devicon object added is up to standard.
    :return a string containing the error messages if any.
    """
    err_msgs = []
    try:
        if icon["name"] != icon_name:
            err_msgs.append("- 'name' value is not: " + icon_name)
    except KeyError:
        err_msgs.append("- missing key: 'name'.")

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
        message = "Error found in 'devicon.json' for '{}' entry: \n{}".format(icon_name, "\n".join(err_msgs))
        raise ValueError(message)
    return ""
