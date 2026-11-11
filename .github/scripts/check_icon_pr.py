from typing import List
import xml.etree.ElementTree as et
from pathlib import Path


# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets import filehandler, arg_getters, util


VERSION_REGEXP = "(original|plain|line)(-wordmark)?"


def main():
    """
    Check the quality of the svgs IF this is an icon PR. Else, does nothing.
    If any error is found, write the error messages to './err_messages.txt'.
    This script only reads files; it never modifies the icons or devicon.json.
    """
    args = arg_getters.get_check_icon_pr_args()
    try:
        all_icons = filehandler.get_json_file_content(args.devicon_json_path)

        devicon_err_msg = []
        # First check if devicon.json is sorted
        if sorted(all_icons, key=lambda d: d['name']) != all_icons:
            devicon_err_msg.append(
                "devicon.json is not sorted correctly.\n"
                "Please make sure that your icon is added in the `devicon.json` file at the correct alphabetic position\n"
                "as seen here: https://github.com/devicons/devicon/wiki/Updating-%60devicon.json%60"
            )

        # get only the icon object that has the name matching the pr title
        filtered_icon = util.find_object_added_in_pr(all_icons, args.pr_title)
        if not filtered_icon:
            devicon_err_msg.append(
                "Could not find an icon in `devicon.json` matching the PR title. "
                "Please make sure the PR title is `new icon: <name>` / `update icon: <name>` "
                "and that the icon's `name` matches."
            )
            filehandler.write_to_file("./err_messages.txt", "\n\n".join(devicon_err_msg))
            print("Task completed.")
            return

        print("Checking devicon.json object: " + str(filtered_icon))

        # check the devicon.json object and the versions/aliases/files
        for msg in (
            check_devicon_object(filtered_icon),
            check_version_files(filtered_icon, args.icons_folder_path),
        ):
            if msg:
                devicon_err_msg.append(msg)

        # check the file names
        filename_err_msg = ""
        svgs = None
        try:
            svgs = filehandler.get_svgs_paths([filtered_icon], args.icons_folder_path, as_str=False)
            print("SVGs to check: ", *svgs, sep='\n')
        except ValueError as e:
            filename_err_msg = "Error found regarding filenames:\n- " + e.args[0]

        # check the svgs
        if svgs is None or len(svgs) == 0:
            print("No SVGs to check, ending script.")
            svg_err_msg = "Error checking SVGs: no SVGs to check. Might be caused by above issues."
        else:
            svg_err_msg = check_svgs(svgs, filtered_icon)

        err_msg = list(devicon_err_msg)

        if filename_err_msg != "":
            err_msg.append(filename_err_msg)

        if svg_err_msg != "":
            err_msg.append(svg_err_msg)

        filehandler.write_to_file("./err_messages.txt", "\n\n".join(err_msg))
        print("Task completed.")
    except Exception as e:
        filehandler.write_to_file("./err_messages.txt", str(e))
        util.exit_with_err(e)


def _is_valid_version(value) -> bool:
    """True if value is a string matching the version naming pattern."""
    return isinstance(value, str) and util.is_svg_version_valid(value)


def check_devicon_object(icon: dict):
    """
    Check that the devicon object added is up to standard.
    :return a string containing the error messages if any.
    """
    err_msgs = []
    name = icon.get("name", "<unknown>")

    # name
    if "name" not in icon:
        err_msgs.append("- Missing property key: \"name\".")
    elif type(icon["name"]) != str:
        err_msgs.append("- Property \"name\" value must be type string.")

    # altnames
    if "altnames" not in icon:
        err_msgs.append("- Missing property key: \"altnames\".")
    elif type(icon["altnames"]) != list or any(type(a) != str for a in icon["altnames"]):
        err_msgs.append("- \"altnames\" must be an array of strings, not: " + str(icon["altnames"]))
    else:
        for altname in icon["altnames"]:
            if altname == icon.get("name"):
                err_msgs.append(f"- \"altnames\" should not contain the same name as \"name\" property. Please remove \"{altname}\" from \"altnames\"")

    # tags
    if "tags" not in icon:
        err_msgs.append("- missing key: 'tags'.")
    elif type(icon["tags"]) != list or any(type(t) != str for t in icon["tags"]):
        err_msgs.append("- 'tags' must be an array of strings, not: " + str(icon["tags"]))

    # versions
    if "versions" not in icon:
        err_msgs.append("- missing key: 'versions'.")
    elif type(icon["versions"]) != dict:
        err_msgs.append("- 'versions' must be an object.")
    else:
        versions = icon["versions"]

        if "svg" not in versions:
            err_msgs.append("- missing key: 'svg' in 'versions'.")
        else:
            if type(versions["svg"]) != list or len(versions["svg"]) == 0:
                err_msgs.append("- must contain at least 1 svg version in a list.")
            else:
                for version in versions["svg"]:
                    if not _is_valid_version(version):
                        err_msgs.append(f"- Invalid version name in versions['svg']: '{version}'. Must match regexp: {VERSION_REGEXP}")

        if "font" not in versions:
            err_msgs.append("- missing key: 'font' in 'versions'.")
        else:
            if type(versions["font"]) != list or len(versions["font"]) == 0:
                err_msgs.append("- must contain at least 1 font version in a list.")
            else:
                for version in versions["font"]:
                    if not _is_valid_version(version):
                        err_msgs.append(f"- Invalid version name in versions['font']: '{version}'. Must match regexp: {VERSION_REGEXP}")

    # color
    if "color" not in icon:
        err_msgs.append("- missing key: 'color'.")
    elif type(icon["color"]) != str or "#" not in icon["color"]:
        err_msgs.append("- 'color' must be a string in the format '#abcdef'")

    # aliases
    if "aliases" not in icon:
        err_msgs.append("- missing key: 'aliases'.")
    elif type(icon["aliases"]) != list:
        err_msgs.append("- \"aliases\" must be an array of objects.")
    elif any(type(a) != dict for a in icon["aliases"]):
        err_msgs.append("- \"aliases\" must be an array of objects, not: " + str(icon["aliases"]))
    else:
        for alias_object in icon["aliases"]:
            for key in ("base", "alias"):
                if key not in alias_object:
                    err_msgs.append(f"- missing key: \"{key}\" in \"aliases\".")
                elif type(alias_object[key]) != str:
                    err_msgs.append(f"- \"{key}\" in \"aliases\" must be a string, not: {alias_object[key]}")
                elif not util.is_svg_version_valid(alias_object[key]):
                    err_msgs.append(f"- Invalid {key} name in aliases[\"{key}\"]: \"{alias_object[key]}\". Must match regexp: {VERSION_REGEXP}")

    if len(err_msgs) > 0:
        return "Error found in \"devicon.json\" for \"{}\" entry: \n{}".format(name, "\n".join(err_msgs))
    return ""


def _get_alias_objects(icon: dict) -> list:
    """Return the well-formed alias objects (dicts) of an icon, ignoring malformed data."""
    raw = icon.get("aliases", [])
    if not isinstance(raw, list):
        return []
    return [a for a in raw if isinstance(a, dict)]


def font_svg_versions(icon: dict) -> set:
    """
    The svg versions whose files go into the icon font.
    A font entry is either an svg version itself, or an alias that
    resolves to its base svg version.
    """
    versions = icon.get("versions", {})
    if not isinstance(versions, dict):
        return set()

    svg_versions = versions.get("svg", [])
    font_versions = versions.get("font", [])
    if not isinstance(svg_versions, list) or not isinstance(font_versions, list):
        return set()

    alias_to_base = {a.get("alias"): a.get("base") for a in _get_alias_objects(icon)}

    resolved = set()
    for version in font_versions:
        if version in svg_versions:
            resolved.add(version)
        elif version in alias_to_base:
            resolved.add(alias_to_base[version])
    return resolved


def check_version_files(icon: dict, icons_folder_path):
    """
    Check (read-only) that:
    - every version in versions['svg'] has a matching file in the icon folder
    - every alias 'base' is listed in versions['svg']
    - every alias name is NOT also in versions['svg'] (an alias is something
      that can be made from another version) and is not defined twice
    - an alias does not point at itself
    - every version in versions['font'] is either in versions['svg'] or is an alias
    :return: a string with the error messages, or "" if there are none.
    """
    err_msgs = []

    try:
        name = icon["name"]
        svg_versions = icon["versions"]["svg"]
        font_versions = icon["versions"]["font"]
    except (KeyError, TypeError):
        return ""  # missing keys are reported by check_devicon_object

    if not isinstance(name, str) or not isinstance(svg_versions, list) or not isinstance(font_versions, list):
        return ""

    icon_folder = Path(icons_folder_path) / name
    if not icon_folder.is_dir():
        return f"- Could not find the icon folder `{icon_folder}`."

    # 1. every svg version listed must exist as a file
    for version in svg_versions:
        if not _is_valid_version(version):
            continue  # reported by check_devicon_object
        expected = icon_folder / f"{name}-{version}.svg"
        if not expected.is_file():
            err_msgs.append(
                f"- `{version}` is listed in versions['svg'], but the file "
                f"`{expected.name}` was not found in `{icon_folder}`."
            )

    # 2. aliases: base must be an svg version; alias must be new and unique
    alias_names = []
    for alias_obj in _get_alias_objects(icon):
        base = alias_obj.get("base")
        alias = alias_obj.get("alias")

        if isinstance(base, str) and base not in svg_versions:
            err_msgs.append(
                f"- alias base `{base}` (for alias `{alias}`) must be listed in versions['svg']."
            )

        if isinstance(base, str) and base == alias:
            err_msgs.append(f"- alias `{alias}` has the same value as its base. Please remove it.")

        if isinstance(alias, str):
            if alias in svg_versions:
                err_msgs.append(
                    f"- alias `{alias}` is also listed in versions['svg']. "
                    "An alias is a version made from another one, so it must not have its own svg version."
                )
            if alias in alias_names:
                err_msgs.append(f"- alias `{alias}` is defined more than once in \"aliases\".")
            alias_names.append(alias)

    # 3. font versions must be an svg version or an alias
    for version in font_versions:
        if not _is_valid_version(version):
            continue  # reported by check_devicon_object
        if version not in svg_versions and version not in alias_names:
            err_msgs.append(
                f"- `{version}` is listed in versions['font'], but is neither in "
                "versions['svg'] nor defined as an alias."
            )

    if err_msgs:
        return f"Error found in the versions of \"{name}\":\n" + "\n".join(err_msgs)
    return ""


def _local_name(tag: str) -> str:
    """Strip the XML namespace, e.g. '{http://www.w3.org/2000/svg}path' -> 'path'."""
    return tag.rsplit("}", 1)[-1].lower()


def check_svgs(svg_file_paths: List[Path], devicon_object: dict):
    """
    Check each svg passed in (read-only):
    - the file name matches the naming pattern
    - the root is an svg element with viewBox '0 0 128 128'
    - the root has no 'width' or 'height' attributes
    - no raster images (<image> / <img>) are embedded
    - if the svg ends up in the icon font (directly or through an alias):
      no 'stroke' and exactly one <path>
    :return: a string with the error messages, or "" if there are none.
    """
    err_msgs = []
    font_versions = font_svg_versions(devicon_object)
    icon_name = devicon_object.get("name", "")

    for svg_path in svg_file_paths:
        err_msg = [f"SVG Error in '{svg_path.name}':"]

        try:
            # name check
            if not util.is_svg_name_valid(svg_path.name):
                err_msg.append("- SVG file name didn't match our pattern of `name-(original|plain|line)(-wordmark)?.svg`")

            tree = et.parse(svg_path)
            root = tree.getroot()
            namespace = "{http://www.w3.org/2000/svg}"

            if root.tag != f"{namespace}svg":
                err_msg.append(f"- root is '{root.tag}'. Root must be an 'svg' element")

            if root.get("viewBox") != "0 0 128 128":
                err_msg.append("- 'viewBox' is not '0 0 128 128' -> Set it or scale the file using https://www.iloveimg.com/resize-image/resize-svg.")

            # width/height on the root: icons must be sized by viewBox only
            present = [attr for attr in ("width", "height") if root.get(attr) is not None]
            if present:
                err_msg.append(
                    f"- The root `svg` element has {' and '.join(f'`{a}`' for a in present)} "
                    "attribute(s). Please remove them and use only the `viewBox` attribute."
                )

            # raster images are not scalable and don't belong in our icons
            raster_tags = sorted({
                _local_name(el.tag) for el in tree.iter()
                if _local_name(el.tag) in ("image", "img")
            })
            if raster_tags:
                err_msg.append(
                    "- SVG contains raster image element(s): "
                    + ", ".join(f"`<{t}>`" for t in raster_tags)
                    + ". Raster images are not scalable. Please convert them to vector paths."
                )

            # checks that only apply to svgs that are built into the icon font
            # "aerospike-original.svg" -> "original"
            version = svg_path.stem[len(icon_name) + 1:]
            if version in font_versions:
                if any(child.get("stroke") is not None for child in tree.iter()):
                    err_msg.append("- SVG contains `stroke` property. This will get ignored by Icomoon. Please convert them to fills.")

                path_count = sum(1 for el in tree.iter() if _local_name(el.tag) == "path")
                if path_count > 1:
                    err_msg.append(
                        f"- SVG contains {path_count} `path` elements, but icons used in the font "
                        "must have exactly one. Please merge them into a single path "
                        "(e.g. select all paths and use Path > Combine / Union in Inkscape or Illustrator)."
                    )

        except et.ParseError as e:
            err_msg.append(f"- Could not parse the SVG. Full error:\n{e}")

        if len(err_msg) > 1:
            err_msgs.append("\n".join(err_msg))

    return "\n\n".join(err_msgs)


if __name__ == "__main__":
    main()
