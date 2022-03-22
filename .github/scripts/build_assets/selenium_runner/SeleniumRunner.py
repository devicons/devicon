from pathlib import Path

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException as SeleniumTimeoutException

from build_assets.selenium_runner.enums import IcomoonOptionState, IcomoonPage, IcomoonAlerts


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
    SHORT_WAIT_IN_SEC = 2.5

    """
    The short wait time for the driver in seconds.
    """
    BRIEF_WAIT_IN_SEC = 0.6

    """
    The Icomoon Url.
    """
    ICOMOON_URL = "https://icomoon.io/app/#/select"

    """
    General import button CSS for Icomoon site.
    """
    GENERAL_IMPORT_BUTTON_CSS = "div#file input[type=file]"

    """
    Set import button CSS for Icomoon site.
    """
    SET_IMPORT_BUTTON_CSS = "li.file input[type=file]"

    """
    The CSS of the tool bar options. There are more but
    these are the ones that we actually use.
    """
    TOOLBAR_OPTIONS_CSS = {
        IcomoonOptionState.SELECT: "div.btnBar button i.icon-select",
        IcomoonOptionState.EDIT: "div.btnBar button i.icon-edit"
    }

    """
    The URL to go to different pages within the Icomoon domain. 
    There are more but these are the ones that we actually use.
    """
    PAGES_URL = {
        IcomoonPage.SELECTION: ICOMOON_URL,
        IcomoonPage.GENERATE_FONT: ICOMOON_URL + "/font"
    }

    """
    The different types of alerts that this workflow will encounter.
    It contains part of the text in the actual alert and buttons
    available to press. It's up to the user to know what button to 
    press for which alert.
    """
    ALERTS = {
        IcomoonAlerts.STROKES_GET_IGNORED_WARNING: {
            "text": "Strokes get ignored when generating fonts or CSH files.",
            "buttons": {
                "DISMISS": "Dismiss",
            }
        },
        IcomoonAlerts.REPLACE_OR_REIMPORT_ICON : {
            "text": "Replace existing icons?",
            "buttons": {
                "REPLACE": "Replace",
                "REIMPORT": "Reimport"
            }
        },
        IcomoonAlerts.DESELECT_ICONS_CONTAINING_STROKES: {
            "text": "Strokes get ignored when generating fonts.",
            "buttons": {
                "DESELECT": "Deselect",
                "CONTINUE": "Continue"
            }
        }
    }

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
        # default values when we open Icomoon
        self.current_option_state = IcomoonOptionState.SELECT
        self.current_page = IcomoonPage.SELECTION
        self.set_browser_options(download_path, geckodriver_path, headless)

    def set_browser_options(self, download_path: str, geckodriver_path: str,
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

        print("Activating browser client...")
        self.driver = WebDriver(options=options, executable_path=geckodriver_path)
        self.driver.get(self.ICOMOON_URL)
        assert "IcoMoon App" in self.driver.title
        # wait until the whole web page is loaded by testing the hamburger input
        WebDriverWait(self.driver, self.LONG_WAIT_IN_SEC).until(
            ec.element_to_be_clickable((By.XPATH, "(//i[@class='icon-menu'])[2]"))
        )
        print("Accessed icomoon.io")

    def switch_toolbar_option(self, option: IcomoonOptionState):
        """
        Switch the toolbar option to the option argument.
        :param option: an option from the toolbar of Icomoon.
        """
        if self.current_option_state == option:
            return

        option_btn = self.driver.find_element_by_css_selector(
            SeleniumRunner.TOOLBAR_OPTIONS_CSS[option]
        )
        option_btn.click()
        self.current_option_state = option

    def click_hamburger_input(self):
        """
        Click the hamburger input until the pop up menu appears. This
        method is needed because sometimes, we need to click the hamburger
        input two times before the menu appears.
        :return: None.
        """
        top_set_hamburger_input_xpath = '//*[@id="setH2"]/button[1]/i' 
        hamburger_input = self.driver.find_element_by_xpath(
            top_set_hamburger_input_xpath
        )

        menu_appear_callback = ec.element_to_be_clickable(
            (By.CSS_SELECTOR, "h1 ul.menuList2")
        )

        while not menu_appear_callback(self.driver):
            hamburger_input.click()

    def test_for_possible_alert(self, wait_period: float) -> IcomoonAlerts:
        """
        Test for the possible alerts that might appear. Return the 
        type of alert if one shows up.
        :param wait_period: the wait period for the possible alert
        in seconds.
        :return: an IcomoonAlerts enum representing the alert that was found.
        Else, return None.
        """
        try:
            overlay_div = WebDriverWait(self.driver, wait_period, 0.15).until(
                ec.element_to_be_clickable(
                    (By.XPATH, "//div[@class='overlay']"))
            )
            alert_message = overlay_div.text
            for alert in self.ALERTS.keys():
                if self.ALERTS[alert]["text"] in alert_message:
                    return alert

            return IcomoonAlerts.UNKNOWN
        except SeleniumTimeoutException:
            return None  # nothing found => everything is good

    def click_alert_button(self, btn_text: str):
        """
        Click the button in the alert that matches the button text.
        :param btn_text: the text that the alert's button will have.
        """
        try:
            button = WebDriverWait(self.driver, self.BRIEF_WAIT_IN_SEC, 0.15).until(
                ec.element_to_be_clickable(
                    (By.XPATH, f"//div[@class='overlay']//button[text()='{btn_text}']"))
            )
            button.click()
        except SeleniumTimeoutException:
            return None  # nothing found => everything is good

    def edit_svg(self, screenshot_folder: str=None, index: int=None):
        """
        Edit the SVG. This include removing the colors and take a
        snapshot if needed.
        :param screenshot_folder: a string or Path object. Point to 
        where we store the screenshots. If truthy, take a screenshot 
        and save it here.
        :param index: the index of the icon in its containing list. 
        Used to differentiate the screenshots. Must be truthy if 
        screenshot_folder is a truthy value.
        """
        self.switch_toolbar_option(IcomoonOptionState.EDIT)
        self.click_latest_icons_in_top_set(1)

        # strip the colors from the SVG.
        # This is because some SVG have colors in them and we don't want to
        # force contributors to remove them in case people want the colored SVGs.
        # The color removal is also necessary so that the Icomoon-generated
        # icons fit within one font symbol/ligiature.
        try:
            color_tab = WebDriverWait(self.driver, self.BRIEF_WAIT_IN_SEC).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, "div.overlayWindow i.icon-droplet"))
            )
            color_tab.click()

            remove_color_btn = self.driver \
                .find_element_by_css_selector("div.overlayWindow i.icon-droplet-cross")
            remove_color_btn.click()
        except SeleniumTimeoutException:
            pass # do nothing cause sometimes, the color tab doesn't appear in the site

        if screenshot_folder != None and index != None:
            edit_screen_selector = "div.overlay div.overlayWindow"
            screenshot_path = str(
                Path(screenshot_folder, f"new_svg_{index}.png").resolve()
            )
            edit_screen = self.driver.find_element_by_css_selector(
                edit_screen_selector)
            edit_screen.screenshot(screenshot_path)
            print("Took screenshot of svg and saved it at " + screenshot_path)

        close_btn = self.driver \
            .find_element_by_css_selector("div.overlayWindow i.icon-close")
        close_btn.click()

    def click_latest_icons_in_top_set(self, amount: int):
        """
        Click on the latest icons in the top set based on the amount passed in.
        This is state option agnostic (doesn't care if it's in SELECT or EDIT mode).
        :param amount: the amount of icons to click on from top left of the top
        set. Must be > 0.
        """
        icon_base_xpath = '//div[@id="set0"]//mi-box[{}]//div'
        for i in range(1, amount + 1):
            icon_xpath = icon_base_xpath.format(i)
            latest_icon = self.driver.find_element_by_xpath(icon_xpath)
            latest_icon.click()

    def select_all_icons_in_top_set(self):
        """
        Select all the svgs in the top most (latest) set.
        """
        self.click_hamburger_input()
        select_all_button = WebDriverWait(self.driver, self.LONG_WAIT_IN_SEC).until(
            ec.element_to_be_clickable((By.XPATH, "//button[text()='Select All']"))
        )
        select_all_button.click()

    def deselect_all_icons_in_top_set(self):
        """
        Select all the svgs in the top most (latest) set.
        """
        self.click_hamburger_input()
        select_all_button = WebDriverWait(self.driver, self.LONG_WAIT_IN_SEC).until(
            ec.element_to_be_clickable((By.XPATH, "//button[text()='Deselect']"))
        )
        select_all_button.click()

    def go_to_page(self, page: IcomoonPage):
        """
        Go to the specified page in Icomoon. This used the URL rather than UI 
        elements due to the inconsistent UI rendering.
        :param page: a valid page that can be accessed in Icomoon.
        """
        if self.current_page == page:
            return

        self.driver.get(self.PAGES_URL[page])
        self.current_page = page

    def close(self):
        """
        Close the SeleniumRunner instance.
        """
        print("Closing down SeleniumRunner...")
        self.driver.quit()
