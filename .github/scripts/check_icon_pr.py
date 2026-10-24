from typing import List
import xml.etree.ElementTree as et
from pathlib import Path


# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets import filehandler, arg_getters, util


def main():
    """
    Check the icons touched by this PR, found from the changed files: the
    `devicon.json` entries and the SVGs.

    An icon PR (one that changes anything in icons/) must only change one
    icons/<name>/ folder and that icon's `devicon.json` entry, and its title must
    describe it. If the title is the only thing wrong about the PR's scope, the
    expected title is written to './expected_title.txt' so the bot can rename the
    PR, instead of reporting it as an error.

    Error messages are written to './err_messages.txt' (empty if all is well).
    """
    args = arg_getters.get_check_icon_pr_args()
    try:
        all_icons = filehandler.get_json_file_content(args.devicon_json_path)
        icons_by_name = {icon["name"]: icon for icon in all_icons}
        changes = util.get_pr_icon_changes(all_icons, args.base)
        print("Changed icon folders:", changes["icon_folders"])
        print("Changed SVGs:", changes["svgs"])
        print("Changed devicon.json entries:", changes["json"])
        print("Other changed files:", changes["other_files"])

        err_msg = []
        #First check if devicon.json is sorted
        if sorted(all_icons, key=lambda d: d['name']) != all_icons:
            err_msg.append(f"devicon.json is not sorted correctly.\nPlease make sure that your icon is added in the `devicon.json` file at the correct alphabetic position\nas seen here: https://github.com/devicons/devicon/wiki/Updating-%60devicon.json%60")

        # An icon PR only touches one icons/<name>/ folder and that icon's devicon.json entry
        icon_folders = changes["icon_folders"]
        if icon_folders:
            if changes["other_files"]:
                err_msg.append("Icon PRs should only change files in `icons/<icon name>/` and `devicon.json`, but this PR also changes:\n" +
                    "\n".join(f"- {path}" for path in changes["other_files"]) +
                    "\nPlease remove these changes from this PR (open a separate PR for them if they're needed).")
            if len(icon_folders) > 1:
                err_msg.append(f"This PR changes several icons ({', '.join(icon_folders)}).\nPlease open a separate PR for each icon.")

        expected_title = ""
        if len(icon_folders) == 1:
            name = icon_folders[0]
            other_entries = [n for n in changes["json"] if n != name]
            if other_entries:
                err_msg.append(f"Icon PRs should only change the `devicon.json` entry of their own icon (\"{name}\"), but this PR also changes: {', '.join(other_entries)}.")

            if name in changes["svgs"] and name not in icons_by_name:
                err_msg.append(f"`icons/{name}/` was changed, but `devicon.json` has no entry named \"{name}\".")
            elif name in changes["svgs"]:
                icon = icons_by_name[name]
                versions, invalid_files = util.get_svg_versions(icon, changes["svgs"][name])
                if invalid_files:
                    err_msg.append("These SVG file names don't match our pattern of `<name>-(original|plain|line)(-wordmark)?.svg`:\n" +
                        "\n".join(f"- icons/{name}/{file}" for file in invalid_files))
                if versions:
                    title_err, title = util.check_pr_title(args.pr_title, icon, name not in changes["existing"], versions)
                    # Only rename automatically when the PR's scope is clean
                    if title_err and not (changes["other_files"] or other_entries or invalid_files):
                        expected_title = title
                    elif title_err:
                        err_msg.append(title_err)

        # Check every icon this PR touches
        to_check = sorted(set(icon_folders) | set(changes["json"]))
        for name in to_check:
            if name not in icons_by_name:
                continue
            icon = icons_by_name[name]
            print("Checking devicon.json object: " + str(icon))
            devicon_err = check_devicon_object(icon)
            if devicon_err:
                err_msg.append(devicon_err)

            try:
                svgs = filehandler.get_svgs_paths([icon], args.icons_folder_path, as_str=False)
                print("SVGs to check: ", *svgs, sep='\n')
            except ValueError as e:
                err_msg.append(f"Error found regarding filenames of \"{name}\":\n- " + e.args[0])
                continue

            if len(svgs) == 0:
                err_msg.append(f"Error checking SVGs of \"{name}\": no SVGs to check. Might be caused by above issues.")
            else:
                svg_err = check_svgs(svgs, icon)
                if svg_err:
                    err_msg.append(svg_err)

        filehandler.write_to_file("./err_messages.txt", "\n\n".join(err_msg))
        filehandler.write_to_file("./expected_title.txt", expected_title)
        if expected_title:
            print(f"PR title should be: {expected_title}")
        print("Task completed.")
    except Exception as e:
        filehandler.write_to_file("./err_messages.txt", str(e))
        util.exit_with_err(e)


def check_devicon_object(icon: dict):
    """
    Check that the devicon object added is up to standard.
    :return a string containing the error messages if any.
    """
    err_msgs = []

    try:
        if type(icon["name"]) != str:
            err_msgs.append("- Property \"name\" value must be type string.")
    except KeyError:
        err_msgs.append("- Missing property key: \"name\".")

    try:
        for altname in icon["altnames"]:
            if type(altname) != str:
                raise TypeError()
            if altname == icon["name"]:
                err_msgs.append(f"- \"altnames\" should not contain the same name as \"name\" property. Please remove \"{altname}\" from \"altnames\"")
    except TypeError:
        err_msgs.append("- \"altnames\" must be an array of strings, not: " + str(icon["altnames"]))
    except KeyError:
        err_msgs.append("- Missing property key: \"altnames\".")

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

        for version in icon["versions"]["svg"]:
            if not util.is_svg_version_valid(version):
                err_msgs.append(f"- Invalid version name in versions['svg']: '{version}'. Must match regexp: (original|plain|line)(-wordmark)?")
    except KeyError:
        err_msgs.append("- missing key: 'svg' in 'versions'.")
    
    try:
        if type(icon["versions"]["font"]) != list or len(icon["versions"]["svg"]) == 0:
            err_msgs.append("- must contain at least 1 font version in a list.")

        for version in icon["versions"]["font"]:
            if not util.is_svg_version_valid(version):
                err_msgs.append(f"- Invalid version name in versions['font']: '{version}'. Must match regexp: (original|plain|line)(-wordmark)?")
    except KeyError:
        err_msgs.append("- missing key: 'font' in 'versions'.")

    try:
        if type(icon["color"]) != str or "#" not in icon["color"]:
            err_msgs.append("- 'color' must be a string in the format '#abcdef'")
    except KeyError:
        err_msgs.append("- missing key: 'color'.")

    try:
        if type(icon["aliases"]) != list:
            err_msgs.append("- \"aliases\" must be an array of objects.")
    except KeyError:
        err_msgs.append("- missing key: 'aliases'.")

    try:
        for alias_objects in icon["aliases"]:
            if type(alias_objects) != dict:
                raise TypeError()
    except TypeError:
        err_msgs.append("- \"aliases\" must be an array of objects, not: " + str(icon["aliases"]))

    try:
        for alias_objects in icon["aliases"]:
            if type(alias_objects["base"]) != str:
                err_msgs.append("- must contain at least 1 base in aliases.")
            if not util.is_svg_version_valid(alias_objects['base']):
                err_msgs.append(f"- Invalid base name in aliases[\"base\"]: \"{alias_objects['base']}\". Must match regexp: (original|plain|line)(-wordmark)?")
    except KeyError:
        err_msgs.append("- missing key: \"base\" in \"aliases\".")

    try:
        for alias_objects in icon["aliases"]:
            if type(alias_objects["alias"]) != str:
                err_msgs.append("- must contain at least 1 alias in aliases.")
            if not util.is_svg_version_valid(alias_objects['alias']):
                err_msgs.append(f"- Invalid alias name in aliases['alias']: \"{alias_objects['alias']}\". Must match regexp: (original|plain|line)(-wordmark)?")
    except KeyError:
        err_msgs.append("- missing key: \"alias\" in \"aliases\".")

    if len(err_msgs) > 0:
        message = "Error found in \"devicon.json\" for \"{}\" entry: \n{}".format(icon["name"], "\n".join(err_msgs))
        return message
    return "" 


def check_svgs(svg_file_paths: List[Path], devicon_object: dict):
    """
    Check the width, height, viewBox and style of each svgs passed in.
    The viewBox must be '0 0 128 128'.
    The style must not contain any 'stroke' declarations.
    If any error is found, they will be thrown.
    :param: svg_file_paths, the file paths to the svg to check for.
    :return: None if there no errors. If there is, return a JSON.stringified
    list with the error messages in it.
    """
    # batch err messages together so user can fix everything at once
    err_msgs = []
    for svg_path in svg_file_paths:
        try:
            err_msg = [f"SVG Error in '{svg_path.name}':"]

            # name check
            if not util.is_svg_name_valid(svg_path.name):
                err_msg.append("- SVG file name didn't match our pattern of `name-(original|plain|line)(-wordmark)?.svg`")

            # svg check
            tree = et.parse(svg_path)
            root = tree.getroot()
            namespace = "{http://www.w3.org/2000/svg}"

            if root.tag != f"{namespace}svg":
                err_msg.append(f"- root is '{root.tag}'. Root must be an 'svg' element")

            if root.get("viewBox") != "0 0 128 128":
                err_msg.append("- 'viewBox' is not '0 0 128 128' -> Set it or scale the file using https://www.iloveimg.com/resize-image/resize-svg.")

            # goes through all elems and check for strokes
            if util.is_svg_in_font_attribute(svg_path, devicon_object):
                for child in tree.iter():
                    if child.get("stroke") != None:
                        err_msg.append("- SVG contains `stroke` property. This will get ignored by Icomoon. Please convert them to fills.")
                        break

            if len(err_msg) > 1:
                err_msgs.append("\n".join(err_msg))
        except et.ParseError as e:
            raise Exception(f"SVG Error in file: {svg_path}. Full Error: \n" + str(e))

    if len(err_msgs) > 0:
        return "\n\n".join(err_msgs)
    return ""


if __name__ == "__main__":
    main()
