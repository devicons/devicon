import colorsys
from pathlib import Path
import re
from typing import List
import xml.etree.ElementTree as et

# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets import arg_getters, filehandler, util


def hex_to_rgb(hex_str: str):
    cleaned = hex_str.lstrip("#").strip()
    if len(cleaned) in (3, 4):
        cleaned = "".join(c * 2 for c in cleaned[:3])
    elif len(cleaned) >= 6:
        cleaned = cleaned[:6]
    else:
        return None
    try:
        val = int(cleaned, 16)
        return (
            ((val >> 16) & 255) / 255.0,
            ((val >> 8) & 255) / 255.0,
            (val & 255) / 255.0,
        )
    except ValueError:
        return None


def is_color_saturated(r: float, g: float, b: float, threshold: float = 0.20) -> bool:
    _, _, s = colorsys.rgb_to_hls(r, g, b)
    return s >= threshold


def svg_contains_saturated_colors(svg_path: Path) -> bool:
    try:
        content = svg_path.read_text(encoding="utf-8")
    except Exception:
        return False

    # Check hex colors: #rgb, #rrggbb, etc.
    hex_matches = re.findall(r"#([0-9a-fA-F]{3,8})\b", content)
    for h in hex_matches:
        rgb = hex_to_rgb(h)
        if rgb and is_color_saturated(*rgb):
            return True

    # Check rgb(...) colors
    rgb_matches = re.findall(
        r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", content
    )
    for r_s, g_s, b_s in rgb_matches:
        rgb = (int(r_s) / 255.0, int(g_s) / 255.0, int(b_s) / 255.0)
        if is_color_saturated(*rgb):
            return True

    # Check hsl(...) colors
    hsl_matches = re.findall(
        r"hsl\(\s*[\d.]+\s*,\s*([\d.]+)%\s*,\s*[\d.]+%?\s*\)", content
    )
    for s_s in hsl_matches:
        try:
            if float(s_s) / 100.0 >= 0.20:
                return True
        except ValueError:
            pass

    return False


def icon_svgs_have_saturated_colors(icon: dict, icons_folder_path="./icons") -> bool:
    if not icon or "name" not in icon:
        return False
    icon_dir = Path(icons_folder_path) / icon["name"]
    if not icon_dir.is_dir():
        return False

    for svg_file in icon_dir.glob("*.svg"):
        if svg_contains_saturated_colors(svg_file):
            return True
    return False


def main():
    """
    Check the quality of the svgs IF this is an icon PR. Else, does nothing.
    If any svg error is found, create a json file called 'svg_err_messages.json'
    in the root folder that will contains the error messages.
    """
    args = arg_getters.get_check_icon_pr_args()
    try:
        all_icons = filehandler.get_json_file_content(args.devicon_json_path)

        devicon_err_msg = []
        # First check if devicon.json is sorted
        if sorted(all_icons, key=lambda d: d["name"]) != all_icons:
            devicon_err_msg.append(
                "devicon.json is not sorted correctly.\n"
                "Please make sure that your icon is added in the `devicon.json` file at the correct alphabetic position\n"
                "as seen here: https://github.com/devicons/devicon/wiki/Updating-%60devicon.json%60"
            )

        # get only the icon object that has the name matching the pr title
        filtered_icon = util.find_object_added_in_pr(all_icons, args.pr_title)
        print("Checking devicon.json object: " + str(filtered_icon))
        devicon_err_msg.append(check_devicon_object(filtered_icon, args.icons_folder_path))

        # check the file names
        filename_err_msg = ""
        svgs = None
        try:
            svgs = filehandler.get_svgs_paths(
                [filtered_icon], args.icons_folder_path, as_str=False
            )
            print("SVGs to check: ", *svgs, sep="\n")
        except ValueError as e:
            filename_err_msg = "Error found regarding filenames:\n- " + e.args[0]

        # check the svgs
        if svgs is None or len(svgs) == 0:
            print("No SVGs to check, ending script.")
            svg_err_msg = (
                "Error checking SVGs: no SVGs to check. Might be caused by above issues."
            )
        else:
            svg_err_msg = check_svgs(svgs, filtered_icon)

        err_msg = []
        if devicon_err_msg != []:
            err_msg.extend(devicon_err_msg)

        if filename_err_msg != "":
            err_msg.append(filename_err_msg)

        if svg_err_msg != "":
            err_msg.append(svg_err_msg)

        filehandler.write_to_file("./err_messages.txt", "\n\n".join(err_msg))
        print("Task completed.")
    except Exception as e:
        filehandler.write_to_file("./err_messages.txt", str(e))
        util.exit_with_err(e)


def check_devicon_object(icon: dict, icons_folder_path="./icons"):
    """
    Check that the devicon object added is up to standard.
    :return a string containing the error messages if any.
    """
    err_msgs = []

    try:
        if type(icon["name"]) != str:
            err_msgs.append('- Property "name" value must be type string.')
    except KeyError:
        err_msgs.append('- Missing property key: "name".')

    try:
        for altname in icon["altnames"]:
            if type(altname) != str:
                raise TypeError()
            if altname == icon["name"]:
                err_msgs.append(
                    f'- "altnames" should not contain the same name as "name" property. Please remove "{altname}" from "altnames"'
                )
    except TypeError:
        err_msgs.append(
            '- "altnames" must be an array of strings, not: ' + str(icon["altnames"])
        )
    except KeyError:
        err_msgs.append('- Missing property key: "altnames".')

    try:
        for tag in icon["tags"]:
            if type(tag) != str:
                raise TypeError()
    except TypeError:
        err_msgs.append(
            "- 'tags' must be an array of strings, not: " + str(icon["tags"])
        )
    except KeyError:
        err_msgs.append("- missing key: 'tags'.")

    try:
        if type(icon["versions"]) != dict:
            err_msgs.append("- 'versions' must be an object.")
    except KeyError:
        err_msgs.append("- missing key: 'versions'.")

    try:
        if (
            type(icon["versions"]["svg"]) != list
            or len(icon["versions"]["svg"]) == 0
        ):
            err_msgs.append("- must contain at least 1 svg version in a list.")

        for version in icon["versions"]["svg"]:
            if not util.is_svg_version_valid(version):
                err_msgs.append(
                    f"- Invalid version name in versions['svg']: '{version}'. Must match regexp: (original|plain|line)(-wordmark)?"
                )
    except KeyError:
        err_msgs.append("- missing key: 'svg' in 'versions'.")

    try:
        if (
            type(icon["versions"]["font"]) != list
            or len(icon["versions"]["svg"]) == 0
        ):
            err_msgs.append("- must contain at least 1 font version in a list.")

        for version in icon["versions"]["font"]:
            if not util.is_svg_version_valid(version):
                err_msgs.append(
                    f"- Invalid version name in versions['font']: '{version}'. Must match regexp: (original|plain|line)(-wordmark)?"
                )
    except KeyError:
        err_msgs.append("- missing key: 'font' in 'versions'.")

    try:
        color = icon["color"]
        if type(color) != str or "#" not in color:
            err_msgs.append("- 'color' must be a string in the format '#abcdef'")
        else:
            normalized_color = color.strip().lower()
            if normalized_color in ["#000000", "#000", "#ffffff"]:
                if icon_svgs_have_saturated_colors(icon, icons_folder_path):
                    err_msgs.append(
                        f"- 'color' property '{color}' appears to be a placeholder, but the icon's SVG contains colored fills/strokes. "
                        "Please specify the official brand color (e.g. hex code '#abcdef') instead of a placeholder."
                    )
    except KeyError:
        err_msgs.append("- missing key: 'color'.")

    try:
        if type(icon["aliases"]) != list:
            err_msgs.append('- "aliases" must be an array of objects.')
    except KeyError:
        err_msgs.append('- missing key: "aliases".')

    try:
        for alias_objects in icon["aliases"]:
            if type(alias_objects) != dict:
                raise TypeError()
    except TypeError:
        err_msgs.append(
            '- "aliases" must be an array of objects, not: ' + str(icon["aliases"])
        )

    try:
        for alias_objects in icon["aliases"]:
            if type(alias_objects["base"]) != str:
                err_msgs.append("- must contain at least 1 base in aliases.")
            if not util.is_svg_version_valid(alias_objects["base"]):
                err_msgs.append(
                    f'- Invalid base name in aliases["base"]: "{alias_objects["base"]}". Must match regexp: (original|plain|line)(-wordmark)?'
                )
    except KeyError:
        err_msgs.append('- missing key: "base" in "aliases".')

    try:
        for alias_objects in icon["aliases"]:
            if type(alias_objects["alias"]) != str:
                err_msgs.append("- must contain at least 1 alias in aliases.")
            if not util.is_svg_version_valid(alias_objects["alias"]):
                err_msgs.append(
                    f"- Invalid alias name in aliases['alias']: \"{alias_objects['alias']}\". Must match regexp: (original|plain|line)(-wordmark)?"
                )
    except KeyError:
        err_msgs.append('- missing key: "alias" in "aliases".')

    if len(err_msgs) > 0:
        message = 'Error found in "devicon.json" for "{}" entry: \n{}'.format(
            icon["name"], "\n".join(err_msgs)
        )
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
                err_msg.append(
                    "- SVG file name didn't match our pattern of `name-(original|plain|line)(-wordmark)?.svg`"
                )

            # svg check
            tree = et.parse(svg_path)
            root = tree.getroot()
            namespace = "{http://www.w3.org/2000/svg}"

            if root.tag != f"{namespace}svg":
                err_msg.append(f"- root is '{root.tag}'. Root must be an 'svg' element")

            if root.get("viewBox") != "0 0 128 128":
                err_msg.append(
                    "- 'viewBox' is not '0 0 128 128' -> Set it or scale the file using https://www.iloveimg.com/resize-image/resize-svg."
                )

            # goes through all elems and check for strokes
            if util.is_svg_in_font_attribute(svg_path, devicon_object):
                for child in tree.iter():
                    if child.get("stroke") != None:
                        err_msg.append(
                            "- SVG contains `stroke` property. This will get ignored by Icomoon. Please convert them to fills."
                        )
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
