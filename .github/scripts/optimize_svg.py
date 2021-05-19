import json
import subprocess

from build_assets import filehandler, arg_getters, util

def main():
    try:
        args = arg_getters.get_selenium_runner_args(True)
        new_icons = filehandler.find_new_icons(args.devicon_json_path, args.icomoon_json_path)

        if len(new_icons) == 0:
            raise Exception("No files need to be uploaded. Ending script...")

        # get only the icon object that has the name matching the pr title
        filtered_icon = util.find_object_added_in_this_pr(new_icons, args.pr_title)
        print("Icon being checked:", filtered_icon, sep = "\n", end='\n\n')

        svgs = filehandler.get_svgs_paths([filtered_icon], args.icons_folder_path, as_str=True)
        subprocess.run(["npm", "run", "optimize-svg", "--", f"--svgFiles={json.dumps(svgs)}"], shell=True)
        print("Task completed.")
    except Exception as e:
        filehandler.write_to_file("./err_messages.txt", str(e))
        util.exit_with_err(e)


if __name__ == "__main__":
    main()
