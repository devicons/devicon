from argparse import ArgumentParser
from build_assets.PathResolverAction import PathResolverAction

def get_selenium_runner_args(peek_mode=False):
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
                        help="The download destination of the Icomoon files",
                        action=PathResolverAction)

    if peek_mode:
        parser.add_argument("--pr_title",
                            help="The title of the PR that we are peeking at")

    return parser.parse_args()


def get_generate_markdown_args():
    parser = ArgumentParser(description="Generate markdown for the image urls passed in.")

    parser.add_argument("img_urls",
                        help="The urls of the images. Must be the string/JSON form of an array. Ex: '[1,2,3]'")

    return parser.parse_args()