from typing import List
from pathlib import Path
import time

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException as SeleniumTimeoutException


class SeleniumRunner:
    """
    A runner that upload and download Icomoon resources using Selenium.
    The WebDriver will use Firefox.
    """

    """
    The long wait time for the driver in seconds.
    """
    LONG_WAIT_IN_SEC = 25

    """
    The medium wait time for the driver in seconds.
    """
    MED_WAIT_IN_SEC = 6

    """
    The short wait time for the driver in seconds.
    """
    SHORT_WAIT_IN_SEC = 0.6

    """
    The Icomoon Url.
    """
    ICOMOON_URL = "https://icomoon.io/app/#/select"

    def __init__(self, download_path: str,
                 geckodriver_path: str, headless: bool):
        """
        Create a SeleniumRunner object.
        :param download_path: the location where you want to download
        the icomoon.zip to.
        :param geckodriver_path: the path to the firefox executable.
        :param headless: whether to run browser in headless (no UI) mode.
        """
        self.driver = None
        self.set_options(download_path, geckodriver_path, headless)

    def set_options(self, download_path: str, geckodriver_path: str,
        headless: bool):
        """
        Build the WebDriver with Firefox Options allowing downloads and
        set download to download_path.
        :param download_path: the location where you want to download
        :param geckodriver_path: the path to the firefox executable.
        the icomoon.zip to.
        :param headless: whether to run browser in headless (no UI) mode.

        :raises AssertionError: if the page title does not contain
        "IcoMoon App".
        """
        options = Options()
        allowed_mime_types = "application/zip, application/gzip, application/octet-stream"
        # disable prompt to download from Firefox
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", allowed_mime_types)
        options.set_preference("browser.helperApps.neverAsk.openFile", allowed_mime_types)

        # set the default download path to downloadPath
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", download_path)
        options.headless = headless

        self.driver = WebDriver(options=options, executable_path=geckodriver_path)
        self.driver.get(self.ICOMOON_URL)
        assert "IcoMoon App" in self.driver.title
        # wait until the whole web page is loaded by testing the hamburger input
        WebDriverWait(self.driver, self.LONG_WAIT_IN_SEC).until(
            ec.element_to_be_clickable((By.XPATH, "(//i[@class='icon-menu'])[2]"))
        )
        print("Accessed icomoon.io")
        

    def upload_icomoon(self, icomoon_json_path: str):
        """
        Upload the icomoon.json to icomoon.io.
        :param icomoon_json_path: a path to the iconmoon.json.
        :raises TimeoutException: happens when elements are not found.
        """
        print("Uploading icomoon.json file...")
        self.click_hamburger_input()
        
        # find the file input and enter the file path
        import_btn = self.driver.find_element(By.XPATH, "(//li[@class='file'])[1]//input")
        import_btn.send_keys(icomoon_json_path)

        try:
            confirm_btn = WebDriverWait(self.driver, SeleniumRunner.MED_WAIT_IN_SEC).until(
                ec.element_to_be_clickable((By.XPATH, "//div[@class='overlay']//button[text()='Yes']"))
            )
            confirm_btn.click()
        except SeleniumTimeoutException as e:
            raise Exception("Cannot find the confirm button when uploading the icomoon.json" \
                  "Ensure that the icomoon.json is in the correct format for Icomoon.io")

        print("JSON file uploaded.")

    def upload_svgs(self, svgs: List[str], screenshot_folder: str=""):
        """
        Upload the SVGs provided in folder_info
        :param svgs: a list of svg Paths that we'll upload to icomoon.
        :param screenshot_folder: the name of the screenshot_folder. If
        the value is provided, it means the user want to take a screenshot
        of each icon.
        """
        print("Uploading SVGs...")

        edit_mode_btn = self.driver.find_element_by_css_selector(
            "div.btnBar button i.icon-edit"
        )
        edit_mode_btn.click()

        self.click_hamburger_input()

        for i in range(len(svgs)):
            import_btn = self.driver.find_element_by_css_selector(
                "li.file input[type=file]"
            )
            import_btn.send_keys(svgs[i])
            print(f"Uploaded {svgs[i]}")
            self.test_for_possible_alert(self.SHORT_WAIT_IN_SEC, "Dismiss")
            self.click_on_just_added_icon(screenshot_folder, i)

        # take a screenshot of the icons that were just added
        new_icons_path = str(Path(screenshot_folder, "new_icons.png").resolve())
        self.driver.save_screenshot(new_icons_path);

        print("Finished uploading the svgs...")

    def click_hamburger_input(self):
        """
        Click the hamburger input until the pop up menu appears. This
        method is needed because sometimes, we need to click the hamburger
        input two times before the menu appears.
        :return: None.
        """
        hamburger_input = self.driver.find_element_by_xpath(
            "(//i[@class='icon-menu'])[2]"
        )

        menu_appear_callback = ec.element_to_be_clickable(
            (By.CSS_SELECTOR, "h1 ul.menuList2")
        )

        while not menu_appear_callback(self.driver):
            hamburger_input.click()

    def test_for_possible_alert(self, wait_period: float, btn_text: str):
        """
        Test for the possible alert when we upload the svgs.
        :param wait_period: the wait period for the possible alert
        in seconds.
        :param btn_text: the text that the alert's button will have.
        :return: None.
        """
        try:
            dismiss_btn = WebDriverWait(self.driver, wait_period, 0.15).until(
                ec.element_to_be_clickable(
                    (By.XPATH, f"//div[@class='overlay']//button[text()='{btn_text}']"))
            )
            dismiss_btn.click()
        except SeleniumTimeoutException:
            pass  # nothing found => everything is good

    def click_on_just_added_icon(self, screenshot_folder: str, index: int):
        """
        Click on the most recently added icon so we can remove the colors
        and take a snapshot if needed.
        """
        recently_uploaded_icon = WebDriverWait(self.driver, self.LONG_WAIT_IN_SEC).until(
            ec.element_to_be_clickable((By.XPATH, "//div[@id='set0']//mi-box[1]//div"))
        )
        recently_uploaded_icon.click()

        self.remove_color_from_icon()

        if screenshot_folder:
            screenshot_path = str(Path(screenshot_folder, f"screenshot_{index}.png").resolve())
            self.driver.save_screenshot(screenshot_path)
            print("Took screenshot and saved it at " + screenshot_path)

        close_btn = self.driver \
            .find_element_by_css_selector("div.overlayWindow i.icon-close")
        close_btn.click()

    def remove_color_from_icon(self):
        """
        Remove the color from the most recent uploaded icon.
        This is because some SVG have colors in them and we don't want to
        force contributors to remove them in case people want the colored SVGs.
        The color removal is also necessary so that the Icomoon-generated
        icons fit within one font symbol/ligiature.
        """
        try:
            color_tab = WebDriverWait(self.driver, self.SHORT_WAIT_IN_SEC).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, "div.overlayWindow i.icon-droplet"))
            )
            color_tab.click()

            remove_color_btn = self.driver \
                .find_element_by_css_selector("div.overlayWindow i.icon-droplet-cross")
            remove_color_btn.click()
        except SeleniumTimeoutException:
            pass # do nothing cause sometimes, the color tab doesn't appear in the site

    def download_icomoon_fonts(self, zip_path: Path):
        """
        Download the icomoon.zip from icomoon.io.
        :param zip_path: the path to the zip file after it's downloaded.
        """
        # select all the svgs so that the newly added svg are part of the collection
        self.click_hamburger_input()
        select_all_button = WebDriverWait(self.driver, self.LONG_WAIT_IN_SEC).until(
            ec.element_to_be_clickable((By.XPATH, "//button[text()='Select All']"))
        )
        select_all_button.click()

        print("Downloading Font files...")
        font_tab = self.driver.find_element_by_css_selector(
            "a[href='#/select/font']"
        )
        font_tab.click()

        self.test_for_possible_alert(self.MED_WAIT_IN_SEC, "Continue")
        download_btn = WebDriverWait(self.driver, SeleniumRunner.LONG_WAIT_IN_SEC).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "button.btn4 span"))
        )
        download_btn.click()
        if self.wait_for_zip(zip_path):
            print("Font files downloaded.")
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
            time.sleep(1)    
        return False

    def close(self):
        """
        Close the SeleniumRunner instance.
        """
        print("Closing down SeleniumRunner...")
        self.driver.quit()
