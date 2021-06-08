from pathlib import Path
import sys
from selenium.common.exceptions import TimeoutException
import re
import subprocess
import json
from typing import List


# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets.SeleniumRunner import SeleniumRunner
from build_assets import filehandler, arg_getters, util, api_handler


def main():
    """
    Build the icons using Icomoon. Also optimize the svgs.
    """
    runner = None
    try:
        args = arg_getters.get_selenium_runner_args()
        new_icons = get_icons_for_building(args.devicon_json_path, args.token)
        if len(new_icons) == 0:
            sys.exit("No files need to be uploaded. Ending script...")

        print(f"There are {len(new_icons)} icons to be build. Here are they:", *new_icons, sep = "\n")

        # optimize_svgs(new_icons, args.icons_folder_path)
        update_icomoon_json(new_icons, args.icomoon_json_path)

        # icon_svgs = filehandler.get_svgs_paths(
        #     new_icons, args.icons_folder_path, icon_versions_only=True)
        # runner = SeleniumRunner(args.download_path,
        #                         args.geckodriver_path, args.headless)
        # runner.upload_icomoon(args.icomoon_json_path)
        # runner.upload_svgs(icon_svgs)

        # zip_name = "devicon-v1.0.zip"
        # zip_path = Path(args.download_path, zip_name)
        # runner.download_icomoon_fonts(zip_path)
        # filehandler.extract_files(str(zip_path), args.download_path)
        # filehandler.rename_extracted_files(args.download_path)
        print("Task completed.")
    except TimeoutException as e:
        util.exit_with_err("Selenium Time Out Error: \n" + str(e))
    except Exception as e:
        util.exit_with_err(e)
    finally:
        if runner is not None:
            runner.close() 


def get_icons_for_building(devicon_json_path: str, token: str):
    """
    Get the icons for building.
    :param devicon_json_path - the path to the `devicon.json`.
    :param token - the token to access the GitHub API.
    """
    all_icons = filehandler.get_json_file_content(devicon_json_path)
    pull_reqs = api_handler.get_merged_pull_reqs_since_last_release(token)
    new_icons = []

    for pull_req in pull_reqs:
        if api_handler.is_feature_icon(pull_req):
            filtered_icon = util.find_object_added_in_this_pr(all_icons, pull_req["title"])
            new_icons.append(filtered_icon)
    return new_icons


def optimize_svgs(new_icons: List[str], icons_folder_path: str):
    """
    Optimize the newly added svgs. This is done in batches
    since the command line has a limit on characters allowed.
    :param new_icons - the new icons that need to be optimized.
    :param icons_folder_path - the path to the /icons folder.
    """
    print("Begin optimizing files")
    svgs = filehandler.get_svgs_paths(new_icons, icons_folder_path, icon_versions_only=False)
    start = 0
    step = 10
    for i in range(start, len(svgs), step):
        batch = svgs[i:i + step]
        subprocess.run(["npm", "run", "optimize-svg", "--", f"--svgFiles={json.dumps(batch)}"], shell=True)


def update_icomoon_json(new_icons: List[str], icomoon_json_path: str):
    """
    Update the `icomoon.json` if it contains any icons
    that needed to be updated. This will remove the icons
    from the `icomoon.json` so the build script will reupload
    it later.
    """
    icomoon_json = filehandler.get_json_file_content(icomoon_json_path)
    wrapper_function = lambda icomoon_icon : find_icomoon_icon_not_in_new_icons(icomoon_icon, new_icons)
    icons_to_keep = filter(wrapper_function, icomoon_json["icons"])
    icomoon_json["icons"] = icons_to_keep
    print(len(icons_to_keep))
    # filehandler.write_to_file(icomoon_json_path, json.dumps(icomoon_json))
  

def find_icomoon_icon_not_in_new_icons(icomoon_icon, new_icons):
    for new_icon in new_icons:
        pattern = re.compile(f"^{new_icon['name']}-")
        if pattern.search(icomoon_icon["properties"]["name"]):
            return False
    return True


if __name__ == "__main__":
    main()
