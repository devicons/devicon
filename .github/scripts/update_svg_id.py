from pathlib import Path
from typing import List

from build_assets.SvgIdUpdater import SvgIdUpdater
from build_assets import filehandler, arg_getters


def main():
    # get all files
    # run the script for each file
    id_updater = SvgIdUpdater()
    # update all svgs in the repo
    print("Start iterating through folder.")
    icons_folder_path = Path("./icons")
    updated_files = []
    for icon_folder in icons_folder_path.iterdir():
        for file in icon_folder.iterdir():
            if file.suffix == ".svg":
                if id_updater.update_id(file):
                    updated_files.append(file.name)
    print("Updated the following files: \n\n", "\n".join(updated_files))


    # update only the svgs added 
    # args = arg_getters.get_check_svgs_on_pr_args()
    # svgs = filehandler.get_added_modified_svgs(args.files_added_json_path,
    #     args.files_modified_json_path)
    # print("SVGs to check: ", *svgs, sep='\n')

    # if len(svgs) == 0:
    #     print("No SVGs to check, ending script.")
    #     return
    
    # for svg_path in svgs:
    #     id_updater.update_id(svg_path)

    print("Script is done.")


if __name__ == "__main__":
    main()
