from pathlib import Path
from selenium.common.exceptions import TimeoutException

# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets.SeleniumRunner import SeleniumRunner
from build_assets import filehandler, util


def main():
    args = util.get_commandline_args()
    new_icons = filehandler.find_new_icons(args.devicon_json_path, args.icomoon_json_path)
    if len(new_icons) == 0:
        print("No files need to be uploaded. Ending script...")
        return

    # print list of new icons
    print("List of new icons:", *new_icons, sep = "\n")
    
    runner = None
    try:
        runner = SeleniumRunner(args.download_path,
                                args.geckodriver_path, args.headless)
        runner.upload_icomoon(args.icomoon_json_path)
        svgs = filehandler.get_svgs_paths(new_icons, args.icons_folder_path)
        runner.upload_svgs(svgs)

        zip_name = "devicon-v1.0.zip"
        zip_path = Path(args.download_path, zip_name)
        runner.download_icomoon_fonts(zip_path)
        filehandler.extract_files(str(zip_path), args.download_path)
        filehandler.rename_extracted_files(args.download_path)
        print("Task completed.")
    except TimeoutException as e:
        print(e)
        print(e.stacktrace)
    finally:
        runner.close()


if __name__ == "__main__":
    main()
