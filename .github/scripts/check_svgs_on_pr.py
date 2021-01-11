import sys
import time


# pycharm complains that build_assets is an unresolved ref
# don't worry about it, the script still runs
from build_assets import filehandler, arg_getters
from build_assets import util


def main():
    """
    Check the quality of the svgs.
    If any svg error is found, create a json file called 'svg_err_messages.json'
    in the root folder that will contains the error messages.
    """
    args = arg_getters.get_check_svgs_on_pr_args()
    try:
        # check the svgs
        svgs = filehandler.get_added_modified_svgs(args.files_added_json_path,
            args.files_modified_json_path)
        print("SVGs to check: ", *svgs, sep='\n')

        if len(svgs) == 0:
            print("No SVGs to check, ending script.")
            return

        err_messages = util.check_svgs(svgs)
        filehandler.write_to_file("./svg_err_messages.txt", err_messages)
        print("Task completed.")
    except Exception as e:
        util.exit_with_err(e)


if __name__ == "__main__":
    main()
