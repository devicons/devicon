from pathlib import Path
import subprocess
import json

from build_assets import filehandler, arg_getters


def main():
    # get all files
    # run the script for each file
    # update all svgs in the repo
    print("Start iterating through folder.")
    icons_folder_path = Path("./icons")
    for icon_folder in icons_folder_path.iterdir():
        # run the subscript for every folder cause can't run all at once
        files = []
        for file in icon_folder.iterdir():
            if file.suffix == ".svg":
                files.append(str(file.resolve()))
        subprocess.run(["npm", "run", "update-svg", "--", json.dumps(files)], shell=True)


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
