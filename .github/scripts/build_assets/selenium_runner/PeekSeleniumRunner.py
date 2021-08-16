from typing import List
from pathlib import Path

from build_assets.selenium_runner.SeleniumRunner import SeleniumRunner
from build_assets.selenium_runner.enums import IcomoonPage, IcomoonAlerts

class PeekSeleniumRunner(SeleniumRunner):
    def peek(self, svgs: List[str], screenshot_folder: str):
        """
        Upload the SVGs and peek at how Icomoon interpret its SVGs and
        font versions.
        :param svgs: a list of svg Paths that we'll upload to icomoon.
        :param screenshot_folder: the name of the screenshot_folder. 
        :return an array of svgs with strokes as strings. These show which icon
        contains stroke.
        """
        messages = self.peek_svgs(svgs, screenshot_folder)        
        self.peek_icons(svgs, screenshot_folder)
        return messages

    def peek_svgs(self, svgs: List[str], screenshot_folder: str):
        """
        Peek at the SVGs provided in svgs. This will look at how Icomoon
        interprets the SVGs as a font.
        :param svgs: a list of svg Paths that we'll upload to icomoon.
        :param screenshot_folder: the name of the screenshot_folder. 
        :return an array of svgs with strokes as strings. These show which icon
        contains stroke.
        """
        print("Peeking SVGs...")

        import_btn = self.driver.find_element_by_css_selector(
            SeleniumRunner.GENERAL_IMPORT_BUTTON_CSS
        )

        svgs_with_strokes = []
        for i in range(len(svgs)):
            import_btn.send_keys(svgs[i])
            print(f"Uploaded {svgs[i]}")

            alert = self.test_for_possible_alert(self.SHORT_WAIT_IN_SEC)
            if alert == None:
                pass  # all good
            elif alert == IcomoonAlerts.STROKES_GET_IGNORED_WARNING:
                print(f"- This icon contains strokes: {svgs[i]}")
                svg = Path(svgs[i])
                svgs_with_strokes.append(f"- {svg.name}")
                self.click_alert_button(self.ALERTS[alert]["buttons"]["DISMISS"])
            else:
                raise Exception(f"Unexpected alert found: {alert}")

            self.edit_svg(screenshot_folder, i)

        # take a screenshot of the svgs that were just added
        self.select_all_icons_in_top_set()
        new_svgs_path = str(Path(screenshot_folder, "new_svgs.png").resolve())
        icon_set_xpath = "/html/body/div[4]/div[1]/div[2]/div[1]"
        icon_set = self.driver.find_element_by_xpath(icon_set_xpath)
        icon_set.screenshot(new_svgs_path);

        print("Finished peeking the svgs...")
        return svgs_with_strokes

    def peek_icons(self, svgs: List[str], screenshot_folder: str):
        """
        Peek at the icon versions of the SVGs that were uploaded.
        :param screenshot_folder: the name of the screenshot_folder. 
        """
        print("Begin peeking at the icons...")
        # ensure all icons in the set is selected.
        self.select_all_icons_in_top_set()
        self.go_to_page(IcomoonPage.GENERATE_FONT)
        alert = self.test_for_possible_alert(self.MED_WAIT_IN_SEC)
        if alert == None:
            pass  # all good
        elif alert == IcomoonAlerts.DESELECT_ICONS_CONTAINING_STROKES:
            self.click_alert_button(self.ALERTS[alert]["buttons"]["CONTINUE"])
        else:
            raise Exception(f"Unexpected alert found: {alert}")

        # take an overall screenshot of the icons that were just added
        # also include the glyph count
        new_icons_path = str(Path(screenshot_folder, "new_icons.png").resolve())
        main_content_xpath = "/html/body/div[4]/div[2]/div/div[1]"
        main_content = self.driver.find_element_by_xpath(main_content_xpath)
        main_content.screenshot(new_icons_path);

        # go downward so we get the oldest icon first
        len_ = len(svgs)
        for i in range(len_, 0, -1):
            xpath = f'//*[@id="glyphSet0"]/div[{i}]'
            icon_div = self.driver.find_element_by_xpath(xpath)

            # crop the div out from the screenshot
            icon_screenshot = str(
                Path(screenshot_folder, f"new_icon_{len_ - i}.png").resolve()
            )
            icon_div.screenshot(icon_screenshot)

        print("Finished peeking the icons...")
