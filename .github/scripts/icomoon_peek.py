from build_assets.selenium_runner.PeekSeleniumRunner import PeekSeleniumRunner
from build_assets import filehandler, arg_getters, util


def main():
    runner = None
    try:
        args = arg_getters.get_selenium_runner_args(has_token=False)
        all_icons = filehandler.get_json_file_content(args.devicon_json_path)

        # get only the icons that were changed in this PR
        filtered_icons = util.find_changed_icons(all_icons, args.changed_files)
        svgs = filehandler.get_svgs_paths(filtered_icons, args.icons_folder_path, True)
        screenshot_folder = filehandler.create_screenshot_folder("./")

        runner = PeekSeleniumRunner(args.download_path, args.geckodriver_path, args.headless)
        message = ""
        for filtered_icon in filtered_icons:
            svgs_with_strokes = runner.peek(svgs, screenshot_folder, filtered_icon)
            print(f"Task completed for {filtered_icon}.")

            if svgs_with_strokes:
                svgs_str = "\n\n".join(svgs_with_strokes)
                message += "\n### WARNING -- Strokes detected in the following SVGs:\n" + svgs_str + "\n"

        filehandler.write_to_file("./err_messages.txt", message)
    except Exception as e:
        filehandler.write_to_file("./err_messages.txt", str(e))
        util.exit_with_err(e)
    finally:
        if runner is not None:
            runner.close()


if __name__ == "__main__":
    main()
