from pathlib import Path
import sys
from selenium.common.exceptions import TimeoutException
import subprocess
import json

# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets.SeleniumRunner import SeleniumRunner
from build_assets import filehandler, arg_getters, util, api_handler


def main():
    args = arg_getters.get_selenium_runner_args()
    all_icons = filehandler.get_json_file_content(args.devicon_json_path)

    pull_reqs = api_handler.get_merged_pull_reqs_since_last_release(args.token)
    new_icons = []
    try:
        for pull_req in pull_reqs:
            if api_handler.is_feature_icon(pull_req):
                filtered_icon = util.find_object_added_in_this_pr(all_icons, pull_req["title"])
                new_icons.append(filtered_icon)
    except Exception as e:
        util.exit_with_err(e)
        

    if len(new_icons) == 0:
        sys.exit("No files need to be uploaded. Ending script...")

    # print list of new icons
    print(f"There are {len(new_icons)} icons to be build. Here are they:", *new_icons, sep = "\n")
    
    runner = None
    try:
        svgs = filehandler.get_svgs_paths(new_icons, args.icons_folder_path, icon_versions_only=False)
        # optimizes the files
        # do in each batch in case the command 
        # line complains there's too many characters
        start = 0
        step = 10
        for i in range(start, len(svgs), step):
            batch = svgs[i:i + step]
            subprocess.run(["npm", "run", "optimize-svg", "--", f"--svgFiles={json.dumps(batch)}"], shell=True)

        icon_svgs = filehandler.get_svgs_paths(
            new_icons, args.icons_folder_path, icon_versions_only=True)
        runner = SeleniumRunner(args.download_path,
                                args.geckodriver_path, args.headless)
        runner.upload_icomoon(args.icomoon_json_path)
        runner.upload_svgs(icon_svgs)

        zip_name = "devicon-v1.0.zip"
        zip_path = Path(args.download_path, zip_name)
        runner.download_icomoon_fonts(zip_path)
        filehandler.extract_files(str(zip_path), args.download_path)
        filehandler.rename_extracted_files(args.download_path)
        print("Task completed.")
    except TimeoutException as e:
        util.exit_with_err("Selenium Time Out Error: \n" + str(e))
    except Exception as e:
        util.exit_with_err(e)
    finally:
        runner.close() 


if __name__ == "__main__":
    main()
