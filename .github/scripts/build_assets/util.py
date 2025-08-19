import os
from pathlib import Path
import re
from typing import List
import platform
import sys
import traceback
from io import FileIO

def exit_with_err(err: Exception, logfile: FileIO=None):
    """
    Exit the current step and display the err.
    :param: err, the error/exception encountered.
    """
    if logfile:
        traceback.print_exc(file=logfile)
    else:
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


def find_changed_icons(icons: List[dict], changed_files: List[str]) -> List[dict]:
    """
    Find the changed icons provided in the changed_files list.
    :param icons, a list of the font objects found in the devicon.json.
    :param changed_files, SVG files changed in the PR or since the last release/tag.
    :return a list of dictionaries with the "name"
    entry values matching the name of changed icons.
    """
    filtered_icons = []
    icon_names = []
    for file in changed_files:
        icon_name = Path(file).parent.name
        icon = [icon for icon in icons if icon["name"] == icon_name]
        if len(icon) > 0 and icon_name not in icon_names:
            icon_names.append(icon_name)
            filtered_icons.extend(icon)
    return filtered_icons


def is_svg_in_font_attribute(svg_file_path: Path, devicon_object: dict):
    """
    Check if svg is in devicon.json's font attribute.
    :param svg_file_path, the path to a single svg icon
    :devicon_object, an object for a single icon inside devicon.json
    :return true if the svg exists in the devicon_object's font attribute, false if it doesn't
    """
    icon_version = Path(svg_file_path).stem.split('-', 1)[1]
    font_object = devicon_object["versions"]["font"]
    return icon_version in font_object


valid_svg_filename_pattern = re.compile(r"-(original|plain|line)(-wordmark)?\.svg$")
def is_svg_name_valid(filename: str):
    return valid_svg_filename_pattern.search(filename) is not None


valid_svg_version_pattern = re.compile(r"^(original|plain|line)(-wordmark)?$")
def is_svg_version_valid(version):
    return valid_svg_version_pattern.search(version) is not None
