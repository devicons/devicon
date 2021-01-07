from typing import List
import sys
import xml.etree.ElementTree as et
import time


# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets import filehandler, arg_getters
from build_assets import github_env


def main():
    args = arg_getters.get_check_svgs_args()
    new_icons = filehandler.find_new_icons(args.devicon_json_path, args.icomoon_json_path)

    if len(new_icons) == 0:
        sys.exit("No files need to be uploaded. Ending script...")

    # print list of new icons
    print("SVGs being checked:", *new_icons, sep = "\n", end='\n\n')

    time.sleep(1)  # do this so the logs stay clean
    try:
        # check the svgs
        svgs = filehandler.get_svgs_paths(new_icons, args.icons_folder_path)
        check_svgs(svgs)
        print("All SVGs found were good.\nTask completed.")
    except Exception as e:
        github_env.set_env_var("ERR_MSGS", str(e))
        sys.exit(str(e))


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
            err_msgs.append("<svg> 'viewBox' is not '0 0 128 128': " + svg_path)

        acceptable_size = [None, "128px", "128"]
        if root.get("height") not in acceptable_size:
            err_msgs.append("<svg> 'height' is present but is not '128' or '128px': " + svg_path)

        if root.get("width") not in acceptable_size:
            err_msgs.append("<svg> 'width' is present but is not '128' or '128px': " + svg_path)

        if root.get("style") is not None and "enable-background" in root.get("style"):
            err_msgs.append("<svg> uses 'enable-background' in its style. This is deprecated: " + svg_path)

        if root.get("x") is not None:
            err_msgs.append("<svg> has an 'x' attribute, this is not needed: " + svg_path)

        if root.get("y") is not None:
            err_msgs.append("<svg> has an 'y' attribute, this is not needed: " + svg_path)

        style = root.findtext(f".//{namespace}style")
        if style != None and "fill" in style:
            err_msgs.append("Found 'fill' in <style>. Use the 'fill' attribute instead: " + svg_path)

    if len(err_msgs) > 0:
        raise Exception("\n" + "\n".join(err_msgs))


if __name__ == "__main__":
    main()
