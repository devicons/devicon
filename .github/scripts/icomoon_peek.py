from build_assets.selenium_runner.PeekSeleniumRunner import PeekSeleniumRunner
from build_assets import filehandler, arg_getters
from build_assets import util


def main():
    runner = None
    try:
        args = arg_getters.get_selenium_runner_args(peek_mode=True)
        new_icons = filehandler.get_json_file_content(args.devicon_json_path)

        # get only the icon object that has the name matching the pr title
        filtered_icon = util.find_object_added_in_pr(new_icons, args.pr_title)
        check_devicon_object(filtered_icon)
        print("Icon being checked:", filtered_icon, sep = "\n", end='\n\n')

        runner = PeekSeleniumRunner(args.download_path, args.geckodriver_path, args.headless)
        svgs = filehandler.get_svgs_paths([filtered_icon], args.icons_folder_path, True)
        screenshot_folder = filehandler.create_screenshot_folder("./") 
        svgs_with_strokes = runner.peek(svgs, screenshot_folder)
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


def check_devicon_object(icon: dict):
    """
    Check that the devicon object added is up to standard.
    :return a string containing the error messages if any.
    """
    err_msgs = []
    try:
        for tag in icon["tags"]:
            if type(tag) != str:
                raise TypeError()
    except TypeError:
        err_msgs.append("- 'tags' must be an array of strings, not: " + str(icon["tags"]))
    except KeyError:
        err_msgs.append("- missing key: 'tags'.")

    try:
        if type(icon["versions"]) != dict:
            err_msgs.append("- 'versions' must be an object.")
    except KeyError:
        err_msgs.append("- missing key: 'versions'.")

    try:
        if type(icon["versions"]["svg"]) != list or len(icon["versions"]["svg"]) == 0:
            err_msgs.append("- must contain at least 1 svg version in a list.")
    except KeyError:
        err_msgs.append("- missing key: 'svg' in 'versions'.")
    
    try:
        if type(icon["versions"]["font"]) != list or len(icon["versions"]["svg"]) == 0:
            err_msgs.append("- must contain at least 1 font version in a list.")
    except KeyError:
        err_msgs.append("- missing key: 'font' in 'versions'.")

    try:
        if type(icon["color"]) != str or "#" not in icon["color"]:
            err_msgs.append("- 'color' must be a string in the format '#abcdef'")
    except KeyError:
        err_msgs.append("- missing key: 'color'.")

    try:
        if type(icon["aliases"]) != list:
            err_msgs.append("- 'aliases' must be an array.")
    except KeyError:
        err_msgs.append("- missing key: 'aliases'.")
    
    if len(err_msgs) > 0:
        message = "Error found in 'devicon.json' for '{}' entry: \n{}".format(icon["name"], "\n".join(err_msgs))
        raise ValueError(message)
    return ""


if __name__ == "__main__":
    main()
