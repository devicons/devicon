from build_assets.SeleniumRunner import SeleniumRunner
import build_assets.filehandler as filehandler
from pathlib import Path
from argparse import ArgumentParser
from build_assets.PathResolverAction import PathResolverAction


def main():
    parser = ArgumentParser(description="Upload svgs to Icomoon to create icon files.")

    parser.add_argument("--headless",
                        help="Whether to run the browser in headless/no UI mode",
                        action="store_true")

    parser.add_argument("icomoon_json_path",
                        help="The path to the icomoon_test.json aka the selection.json created by Icomoon",
                        action=PathResolverAction)

    parser.add_argument("devicon_json_path",
                        help="The path to the devicon_test.json",
                        action=PathResolverAction)

    parser.add_argument("icons_folder_path",
                        help="The path to the icons folder",
                        action=PathResolverAction)

    parser.add_argument("download_path",
                        help="The path where you'd like to download the Icomoon files to",
                        action=PathResolverAction)

    args = parser.parse_args()

    runner = SeleniumRunner(args.icomoon_json_path, args.download_path,
                            args.headless)
    runner.upload_icomoon()

    new_icons = filehandler.find_new_icons(args.devicon_json_path, args.icomoon_json_path)
    svgs = filehandler.get_svgs_paths(new_icons, args.icons_folder_path)
    runner.upload_svgs(svgs)
    runner.download_icomoon_fonts()

    zip_name = "devicon-v1.0.zip"
    zip_path = str(Path(args.download_path, zip_name))
    # filehandler.extract_files(zip_path, args.download_path)
    # filehandler.rename_extracted_files(args.download_path)
    runner.close(err=False)
    print("Task completed.")


if __name__ == "__main__":
    main()
