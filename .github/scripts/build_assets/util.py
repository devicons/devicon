import os
from pathlib import Path
import re
from typing import List, Tuple
import platform
import sys
import traceback
import json
import subprocess
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


def find_object_added_in_pr(icons: List[dict], pr_title: str):
    """
    Find the icon name from the PR title. 
    :param icons, a list of the font objects found in the devicon.json.
    :pr_title, the title of the PR that this workflow was called on.
    :return a dictionary with the "name"
    entry's value matching the name in the pr_title.
    :raise If no object can be found, raise an Exception.
    """
    try:
        pattern = re.compile(r"(?<=^new icon: )\w+ (?=\(.+\))|(?<=^update icon: )\w+ (?=\(.+\))", re.I)
        icon_name_index = 0
        icon_name = pattern.findall(pr_title)[icon_name_index].lower().strip()  # should only have one match
        icon = [icon for icon in icons if icon["name"] == icon_name][0]
        return icon
    except IndexError as e:  # there are no match in the findall()
        print(e)
        message = "util.find_object_added_in_pr: Couldn't find an icon matching the name in the PR title.\n" \
            f"PR title is: '{pr_title}'"
        raise Exception(message)


def get_pr_icon_changes(devicon_json: List[dict], base: str="HEAD^1"):
    """
    Find out which icons a PR touches by diffing against `base`. In a PR's
    merge commit (what actions/checkout checks out), HEAD^1 is the target branch.
    :param devicon_json, the devicon.json content of the PR.
    :param base, the commit to compare against.
    :return a dict with:
        "svgs": {icon folder name: [SVG file names added/modified]}
        "icon_folders": sorted names of the icons/<name>/ folders with any change
            (added, modified or deleted files)
        "other_files": changed paths outside icons/<name>/ and devicon.json
        "json": names of devicon.json entries that were added, changed or removed
        "existing": names of devicon.json entries that already existed at `base`
    """
    # -z: NUL-separated "status, path" pairs, so unusual file names parse safely.
    # --no-renames: a rename shows up as a delete + add, so both paths count.
    out = subprocess.run(
        ["git", "diff", "--name-status", "-z", "--no-renames", base, "HEAD"],
        capture_output=True, text=True, check=True).stdout.split("\0")
    svgs, icon_folders, other_files = {}, set(), []
    for status, path in zip(out[0::2], out[1::2]):
        if path == "devicon.json":
            continue
        parts = path.split("/")  # icons/<name>/<file>
        if len(parts) == 3 and parts[0] == "icons":
            icon_folders.add(parts[1])
            if status != "D" and parts[2].endswith(".svg"):
                svgs.setdefault(parts[1], []).append(parts[2])
        else:
            other_files.append(path)

    try:
        base_json = json.loads(subprocess.run(["git", "show", f"{base}:devicon.json"],
            capture_output=True, text=True, check=True).stdout)
    except subprocess.CalledProcessError:
        base_json = []
    base_icons = {icon["name"]: icon for icon in base_json}
    current_names = {icon["name"] for icon in devicon_json}
    changed_json = [icon["name"] for icon in devicon_json if base_icons.get(icon["name"]) != icon]
    changed_json += [name for name in base_icons if name not in current_names]

    return {"svgs": svgs, "icon_folders": sorted(icon_folders), "other_files": other_files,
            "json": changed_json, "existing": set(base_icons)}


def get_svg_versions(icon: dict, svg_files: List[str]) -> Tuple[List[str], List[str]]:
    """
    Get the versions of the given SVG files of an icon.
    :param icon, the icon's devicon.json object.
    :param svg_files, SVG file names in the icon's folder.
    :return (versions, invalid file names). Versions are ordered like
    versions.svg in devicon.json.
    """
    versions, invalid = [], []
    for file in svg_files:
        stem = Path(file).stem
        version = stem[len(icon["name"]) + 1:]
        if stem.startswith(icon["name"] + "-") and is_svg_version_valid(version):
            versions.append(version)
        else:
            invalid.append(file)

    order = icon["versions"]["svg"]
    versions.sort(key=lambda v: (order.index(v) if v in order else len(order), v))
    return versions, invalid


pr_title_pattern = re.compile(r"^(new|update) icon:\s*([\w.-]+)\s*\(([^)]*)\)\s*$", re.I)
def check_pr_title(pr_title: str, icon: dict, is_new: bool, versions: List[str]):
    """
    Check that an icon PR's title is `new icon: <name> (<versions>)` or
    `update icon: <name> (<versions>)`, matching what the PR actually does.
    :param pr_title, the PR title.
    :param icon, the devicon.json object of the icon whose SVGs the PR changes.
    :param is_new, whether the icon is new (not in the target branch's devicon.json).
    :param versions, the SVG versions the PR adds/changes.
    :return (problems, expected title): problems is a string with the issues and
    the expected title, or "" if the title is fine.
    """
    kind = "new" if is_new else "update"
    expected = f"{kind} icon: {icon['name']} ({', '.join(versions)})"

    problems = []
    match = pr_title_pattern.match(pr_title.strip())
    if not match:
        problems.append("it doesn't follow the format `new icon: <name> (<versions>)` or `update icon: <name> (<versions>)`")
    else:
        title_kind, title_name = match.group(1).lower(), match.group(2).lower()
        title_versions = {v.strip().lower() for v in match.group(3).split(",") if v.strip()}
        if title_kind != kind:
            what = "adds a new icon" if is_new else "updates an existing icon"
            problems.append(f"this PR {what}, so the title should start with `{kind} icon:`")
        if title_name != icon["name"]:
            problems.append(f"the icon name should be `{icon['name']}` (as in the folder name and `devicon.json`), not `{title_name}`")
        if title_versions != set(versions):
            verb = "adds" if is_new else "changes"
            problems.append(f"the versions should be the SVGs this PR {verb}: {', '.join(versions)}")

    if problems:
        return "PR title issues:\n" + "\n".join(f"- {p}" for p in problems) + f"\n\nExpected title:\n{expected}", expected
    return "", expected


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
