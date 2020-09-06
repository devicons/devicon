from pathlib import Path
from argparse import ArgumentParser
from selenium.common.exceptions import TimeoutException

# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets.SeleniumRunner import SeleniumRunner
from build_assets import filehandler
from build_assets.PathResolverAction import PathResolverAction


def main():
    parser = ArgumentParser(description="Upload svgs to Icomoon to create icon files.")

    parser.add_argument("--headless",
                        help="Whether to run the browser in headless/no UI mode",
                        action="store_true")

    parser.add_argument("geckodriver_path",
                        help="The path to the firefox executable file",
                        action=PathResolverAction)

    parser.add_argument("icomoon_json_path",
                        help="The path to the icomoon.json aka the selection.json created by Icomoon",
                        action=PathResolverAction)

    parser.add_argument("devicon_json_path",
                        help="The path to the devicon.json",
                        action=PathResolverAction)

    parser.add_argument("icons_folder_path",
                        help="The path to the icons folder",
                        action=PathResolverAction)

    parser.add_argument("download_path",
                        help="The path where you'd like to download the Icomoon files to",
                        action=PathResolverAction)

    args = parser.parse_args()

    new_icons = filehandler.find_new_icons(args.devicon_json_path, args.icomoon_json_path)
    if len(new_icons) == 0:
        print("No files need to be uploaded. Ending script...")
        return

    # print list of new icons, separated by comma
    print("List of new icons:")
    print(*new_icons, sep = "\n")
    try:
        runner = SeleniumRunner(args.icomoon_json_path, args.download_path,
                                args.geckodriver_path, args.headless)
        runner.upload_icomoon()
        svgs = filehandler.get_svgs_paths(new_icons, args.icons_folder_path)
        runner.upload_svgs(svgs)


        zip_name = "devicon-v1.0.zip"
        zip_path = Path(args.download_path, zip_name)
        runner.download_icomoon_fonts(zip_path)
        filehandler.extract_files(str(zip_path), args.download_path)
        filehandler.rename_extracted_files(args.download_path)
        runner.close()
        print("Task completed.")
    except TimeoutException as e:
        print(e)
        print(e.stacktrace)
        runner.close()


if __name__ == "__main__":
    main()
