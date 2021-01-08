import traceback
import sys

# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets import filehandler, arg_getters
from build_assets import util


def main():
    """
    Check the quality of the svgs of the whole icons folder.
    """
    args = arg_getters.get_check_svgs_monthly_args()

    try:
        devicon_json = filehandler.get_json_file_content(args.devicon_json_path)
        svgs = filehandler.get_svgs_paths(devicon_json, args.icons_folder_path)
        util.check_svgs(svgs)
        print("All SVGs found were good. Task completed.")
    except Exception as e:
        util.exit_with_err(e)


if __name__ == "__main__":
    main()