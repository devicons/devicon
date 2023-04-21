from pathlib import Path
import sys
from selenium.common.exceptions import TimeoutException
import re
import subprocess
import json
from typing import List, Dict
from io import FileIO

# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets.selenium_runner.BuildSeleniumRunner import BuildSeleniumRunner
from build_assets import filehandler, arg_getters, util, api_handler

def main():
    """
    Build the icons using Icomoon. Also optimize the svgs.
    """
    runner = None
    logfile = open("log.txt", "w")
    try:
        args = arg_getters.get_selenium_runner_args(has_token=False)
        new_icons = get_icons_for_building(args.icomoon_json_path, args.devicon_json_path, logfile)
        if len(new_icons) == 0:
            sys.exit("No files need to be uploaded. Ending script...")

        print(f"There are {len(new_icons)} icons to be build. Here are they:", *new_icons, sep = "\n", file=logfile)

        print("Begin optimizing files...", file=logfile)
        optimize_svgs(new_icons, args.icons_folder_path, logfile=logfile)

        print("Updating the icomoon json...", file=logfile)
        update_icomoon_json(new_icons, args.icomoon_json_path, logfile)

        print("Start the building icons process...", file=logfile)
        icon_svgs = filehandler.get_svgs_paths(
            new_icons, args.icons_folder_path, icon_versions_only=True)
        zip_name = "devicon-v1.0.zip"
        zip_path = Path(args.download_path, zip_name)
        screenshot_folder = filehandler.create_screenshot_folder("./") 

        runner = BuildSeleniumRunner(args.download_path,
            args.geckodriver_path, args.headless, log_output=logfile)
        print("Building icons...", file=logfile)
        runner.build_icons(args.icomoon_json_path, zip_path,
            icon_svgs, screenshot_folder)

        print("Extracting files...", file=logfile)
        filehandler.extract_files(str(zip_path), args.download_path, logfile)
        print("Renaming extracted files...", file=logfile)
        filehandler.rename_extracted_files(args.download_path, logfile)

        print("Task completed!", file=logfile)
    except TimeoutException as e:
        util.exit_with_err(Exception("Selenium Time Out Error: \n" + str(e)), logfile)
    except Exception as e:
        util.exit_with_err(e, logfile)
    finally:
        print("Exiting", file=logfile)
        if runner is not None:
            runner.close() 
        logfile.close()


def get_icons_for_building(icomoon_json_path: str, devicon_json_path: str, logfile: FileIO):
    """
    Get the icons for building.
    :param icomoon_json_path - the path to the `icomoon.json`.
    :param devicon_json_path - the path to the `devicon.json`.
    :param logfile.
    :return a list of dict containing info on the icons. These are 
    from the `devicon.json`.
    """

    new_icons = []

    # get any icons that might not have been found by the API
    # sometimes happen due to the PR being opened before the latest build release
    new_icons_from_devicon_json = filehandler.find_new_icons_in_devicon_json(
        devicon_json_path, icomoon_json_path)

    for icon in new_icons_from_devicon_json:
        if icon not in new_icons:
            new_icons.append(icon)

    return new_icons


def optimize_svgs(new_icons: List[str], icons_folder_path: str, logfile: FileIO):
    """
    Optimize the newly added svgs. This is done in batches
    since the command line has a limit on characters allowed.
    :param new_icons - the new icons that need to be optimized.
    :param icons_folder_path - the path to the /icons folder.
    :param logfile - the file obj to store logging info in.
    """
    svgs = filehandler.get_svgs_paths(new_icons, icons_folder_path, icon_versions_only=False)
    start = 0
    step = 10
    for i in range(start, len(svgs), step):
        batch = svgs[i:i + step]
        print(f"Optimizing these files\n{batch}", file=logfile)
        subprocess.run(["npm", "run", "optimize-svg", "--", f"--svgFiles={json.dumps(batch)}"], shell=True)


def update_icomoon_json(new_icons: List[str], icomoon_json_path: str, logfile: FileIO):
    """
    Update the `icomoon.json` if it contains any icons
    that needed to be updated. This will remove the icons
    from the `icomoon.json` so the build script will reupload
    it later.
    """
    icomoon_json = filehandler.get_json_file_content(icomoon_json_path)
    cur_len = len(icomoon_json["icons"])
    messages = []

    wrapper_function = lambda icomoon_icon : find_icomoon_icon_not_in_new_icons(
        icomoon_icon, new_icons, messages)
    icons_to_keep = filter(wrapper_function, icomoon_json["icons"])
    icomoon_json["icons"] = list(icons_to_keep)

    new_len = len(icomoon_json["icons"])
    print(f"Update completed. Removed {cur_len - new_len} icons:", *messages, sep='\n', file=logfile)
    filehandler.write_to_file(icomoon_json_path, json.dumps(icomoon_json))
  

def find_icomoon_icon_not_in_new_icons(icomoon_icon: Dict, new_icons: List, messages: List):
    """
    Find all the icomoon icons that are not listed in the new icons.
    This also add logging for which icons were removed.
    :param icomoon_icon - a dict object from the icomoon.json's `icons` attribute.
    :param new_icons - a list of new icons. Each element is an object from the `devicon.json`.
    :param messages - an empty list where the function can attach logging on which 
    icon were removed.
    """
    for new_icon in new_icons:
        pattern = re.compile(f"^{new_icon['name']}-")
        if pattern.search(icomoon_icon["properties"]["name"]):
            message = f"-'{icomoon_icon['properties']['name']}' cause it matches '{new_icon['name']}'"
            messages.append(message)
            return False
    return True

if __name__ == "__main__":
    main()
