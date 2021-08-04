from typing import List
from pathlib import Path

from build_assets.selenium_runner.SeleniumRunner import SeleniumRunner

class PeekSeleniumRunner(SeleniumRunner):
    def peek(self, svgs: List[str], screenshot_folder: str):
        """
        Upload the SVGs and peek at how Icomoon interpret its SVGs and
        font versions.
        :param svgs: a list of svg Paths that we'll upload to icomoon.
        :param screenshot_folder: the name of the screenshot_folder. 
        """
        # enforce ordering
        self.peek_svgs(svgs, screenshot_folder)        
        self.peek_icons(screenshot_folder)

    def peek_svgs(self, svgs: List[str], screenshot_folder: str):
        """
        Peek at the SVGs provided in svgs. This will look at how Icomoon
        interprets the SVGs as a font.
        :param svgs: a list of svg Paths that we'll upload to icomoon.
        :param screenshot_folder: the name of the screenshot_folder. 
        """
        print("Peeking SVGs...")

        import_btn = self.driver.find_element_by_css_selector(
            SeleniumRunner.GENERAL_IMPORT_BUTTON_CSS
        )

        for i in range(len(svgs)):
            import_btn.send_keys(svgs[i])
            print(f"Uploaded {svgs[i]}")
            self.test_for_possible_alert(self.SHORT_WAIT_IN_SEC, "Dismiss")
            self.edit_svg(screenshot_folder, i)

        # take a screenshot of the svgs that were just added
        self.select_all_icons_in_top_set()
        new_icons_path = str(Path(screenshot_folder, "new_svgs.png").resolve())
        self.driver.save_screenshot(new_icons_path);

        print("Finished uploading the svgs...")

    def peek_icons(self, screenshot_folder: str):
        """
        Peek at the icon versions of the SVGs that were uploaded.
        :param screenshot_folder: the name of the screenshot_folder. 
        """
        # ensure all icons in the set is selected.
        self.select_all_icons_in_top_set()
        self.go_to_font_tab()

        # take a screenshot of the icons that were just added
        new_icons_path = str(Path(screenshot_folder, "new_icons.png").resolve())
        self.driver.save_screenshot(new_icons_path);
