from pathlib import Path
import json


# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets import filehandler


if __name__ == "__main__":
    """
    Use as a cmd line script to check all the icons of the devicon.json.
    """
    devicon_json_path = str(Path("./devicon.json").resolve())
    icons_folder_path = str(Path("./icons").resolve())
    with open(devicon_json_path) as json_file:
        devicon_json = json.load(json_file)
        svgs = filehandler.get_svgs_paths(devicon_json, icons_folder_path)