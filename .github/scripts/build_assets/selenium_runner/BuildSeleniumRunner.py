from typing import List
import time
from pathlib import Path

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException as SeleniumTimeoutException

from build_assets.selenium_runner.SeleniumRunner import SeleniumRunner
from build_assets.selenium_runner.enums import IcomoonPage, IcomoonAlerts, IcomoonOptionState

class BuildSeleniumRunner(SeleniumRunner):
    def build_icons(self, icomoon_json_path: str,
        zip_path: Path, svgs: List[str], screenshot_folder: str):
        self.upload_icomoon(icomoon_json_path)
        # necessary so we can take screenshot of only the 
        # recently uploaded icons later
        self.deselect_all_icons_in_top_set()
        self.upload_svgs(svgs, screenshot_folder)
        self.take_icon_screenshot(screenshot_folder)
        self.download_icomoon_fonts(zip_path)

    def upload_icomoon(self, icomoon_json_path: str):
        """
        Upload the icomoon.json to icomoon.io.
        :param icomoon_json_path: a path to the iconmoon.json.
        :raises TimeoutException: happens when elements are not found.
        """
        print("Uploading icomoon.json file...", file=self.log_output)
        
        # find the file input and enter the file path
        import_btn = self.driver.find_element_by_css_selector(
            SeleniumRunner.GENERAL_IMPORT_BUTTON_CSS
        )
        import_btn.send_keys(icomoon_json_path)

        try:
            confirm_btn = WebDriverWait(self.driver, SeleniumRunner.MED_WAIT_IN_SEC).until(
                ec.element_to_be_clickable((By.XPATH, "//div[@class='overlay']//button[text()='Yes']"))
            )
            confirm_btn.click()
        except SeleniumTimeoutException as e:
            raise Exception("Cannot find the confirm button when uploading the icomoon.json" \
                  "Ensure that the icomoon.json is in the correct format for Icomoon.io")

        print("JSON file uploaded.", file=self.log_output)

    def upload_svgs(self, svgs: List[str], screenshot_folder: str):
        """
        Upload the SVGs provided in svgs. This will upload the 
        :param svgs: a list of svg Paths that we'll upload to icomoon.
        :param screenshot_folder: the name of the screenshot_folder. 
        """
        print("Uploading SVGs...", file=self.log_output)

        import_btn = self.driver.find_element_by_css_selector(
            SeleniumRunner.SET_IMPORT_BUTTON_CSS
        )

        # there could be at most 2 alerts when we upload an SVG.
        possible_alerts_amount = 2
        err_messages = []
        for i in range(len(svgs)):
            import_btn.send_keys(svgs[i])
            print(f"Uploading {svgs[i]}", file=self.log_output)

            # see if there are stroke messages or replacing icon message
            # there should be none of the second kind
            for j in range(possible_alerts_amount):
                alert = self.test_for_possible_alert(self.SHORT_WAIT_IN_SEC)
                if alert == None:
                    pass  # all good
                elif alert == IcomoonAlerts.STROKES_GET_IGNORED_WARNING:
                    message = f"SVG contained strokes: {svgs[i]}."
                    err_messages.append(message)
                    self.click_alert_button(self.ALERTS[alert]["buttons"]["DISMISS"])
                elif alert == IcomoonAlerts.REPLACE_OR_REIMPORT_ICON:
                    message = f"Duplicated SVG: {svgs[i]}."
                    err_messages.append(message)
                    self.click_alert_button(self.ALERTS[alert]["buttons"]["REIMPORT"])
                else:
                    raise Exception(f"Unexpected alert found: {alert}")

            self.edit_svg()
            print(f"Finished editing icon.", file=self.log_output)

        print("Finished uploading all files.", file=self.log_output)
        if err_messages != []:
            message = "BuildSeleniumRunner - Issues found when uploading SVGs:\n"
            raise Exception(message + '\n'.join(err_messages))

        # take a screenshot of the svgs that were just added
        # select the latest icons
        self.switch_toolbar_option(IcomoonOptionState.SELECT)
        self.select_all_icons_in_top_set()
        new_svgs_path = str(Path(screenshot_folder, "new_svgs.png").resolve())
        self.driver.save_screenshot(new_svgs_path)

        print("Finished uploading the svgs...", file=self.log_output)

    def take_icon_screenshot(self, screenshot_folder: str):
        """
        Take the overview icon screenshot of the uploaded icons.
        :param svgs: a list of svg Paths that we'll upload to icomoon.
        :param screenshot_folder: the name of the screenshot_folder. 
        """
        # take pictures
        print("Taking screenshot of the new icons...", file=self.log_output)
        self.go_to_generate_font_page()

        # take an overall screenshot of the icons that were just added
        # also include the glyph count
        new_icons_path = str(Path(screenshot_folder, "new_icons.png").resolve())
        main_content_xpath = "/html/body/div[4]/div[2]/div/div[1]"
        main_content = self.driver.find_element_by_xpath(main_content_xpath)

        # wait a bit for all the icons to load before we take a pic
        time.sleep(SeleniumRunner.MED_WAIT_IN_SEC)
        main_content.screenshot(new_icons_path)
        print("Saved screenshot of the new icons...", file=self.log_output)

    def go_to_generate_font_page(self):
        """
        Go to the generate font page. Also handles the "Deselect Icons 
        with Strokes" alert.
        """
        self.go_to_page(IcomoonPage.GENERATE_FONT)
        alert = self.test_for_possible_alert(self.MED_WAIT_IN_SEC)
        if alert == None:
            pass  # all good
        elif alert == IcomoonAlerts.DESELECT_ICONS_CONTAINING_STROKES:
            message = f"One of SVGs contained strokes. This should not happen."
            raise Exception(message)
        else:
            raise Exception(f"Unexpected alert found: {alert}")

    def download_icomoon_fonts(self, zip_path: Path):
        """
        Download the icomoon.zip from icomoon.io. Also take a picture of 
        what the icons look like.
        :param zip_path: the path to the zip file after it's downloaded.
        """
        print("Downloading Font files...", file=self.log_output)
        if self.current_page != IcomoonPage.SELECTION:
            self.go_to_page(IcomoonPage.SELECTION)

        self.select_all_icons_in_top_set()
        self.go_to_generate_font_page()

        download_btn = WebDriverWait(self.driver, SeleniumRunner.LONG_WAIT_IN_SEC).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "button.btn4 span"))
        )
        download_btn.click()
        if self.wait_for_zip(zip_path):
            print("Font files downloaded.", file=self.log_output)
        else:
            raise TimeoutError(f"Couldn't find {zip_path} after download button was clicked.")

    def wait_for_zip(self, zip_path: Path) -> bool:
        """
        Wait for the zip file to be downloaded by checking for its existence
        in the download path. Wait time is self.LONG_WAIT_IN_SEC and check time
        is 1 sec.
        :param zip_path: the path to the zip file after it's
        downloaded.
        :return: True if the file is found within the allotted time, else
        False.
        """
        end_time = time.time() + self.LONG_WAIT_IN_SEC
        while time.time() <= end_time:
            if zip_path.exists():
                return True
            time.sleep(1)  # wait so we don't waste sys resources
        return False
