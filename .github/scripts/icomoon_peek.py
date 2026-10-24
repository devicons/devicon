from build_assets.selenium_runner.PeekSeleniumRunner import PeekSeleniumRunner
from build_assets import filehandler, arg_getters, util


def main():
    runner = None
    try:
        args = arg_getters.get_selenium_runner_args(has_token=False, peek_mode=True)
        all_icons = filehandler.get_json_file_content(args.devicon_json_path)

        # peek at the icon whose SVGs this PR adds/changes
        changes = util.get_pr_icon_changes(all_icons, args.base)
        svg_icons = sorted(changes["svgs"])
        if len(svg_icons) == 0:
            # e.g. a devicon.json-only change: nothing to peek, no screenshots
            print("No icon SVGs changed in this PR, nothing to peek.")
            filehandler.write_to_file("./err_messages.txt", "")
            return
        if len(svg_icons) > 1:
            raise Exception(f"This PR changes the SVGs of several icons ({', '.join(svg_icons)}). Please open a separate PR for each icon.")
        filtered_icon = next((icon for icon in all_icons if icon["name"] == svg_icons[0]), None)
        if filtered_icon is None:
            raise Exception(f"`icons/{svg_icons[0]}/` was changed, but `devicon.json` has no entry named \"{svg_icons[0]}\".")

        svgs = filehandler.get_svgs_paths([filtered_icon], args.icons_folder_path, True)
        screenshot_folder = filehandler.create_screenshot_folder("./") 

        runner = PeekSeleniumRunner(args.download_path, args.geckodriver_path, args.headless)
        svgs_with_strokes = runner.peek(svgs, screenshot_folder, filtered_icon)
        print("Task completed.")

        message = ""
        if svgs_with_strokes != []:
            svgs_str = "\n\n".join(svgs_with_strokes)
            message = "\n### WARNING -- Strokes detected in the following SVGs:\n" + svgs_str + "\n"
        filehandler.write_to_file("./err_messages.txt", message)
    except Exception as e:
        filehandler.write_to_file("./err_messages.txt", str(e))
        util.exit_with_err(e)
    finally:
        if runner is not None:
            runner.close() 


if __name__ == "__main__":
    main()
