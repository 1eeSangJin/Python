from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
import time

class DriverUtils(object):
    def __init__(self, driver):
        self.driver = driver

    def focus_frame(self, explicit_wait_time, element):
        WebDriverWait(self.driver, explicit_wait_time).until(EC.frame_to_be_available_and_switch_to_it(element))

    def clipboard_input(self, user_xpath, user_input):
        temp_user_input = pyperclip.paste();

        pyperclip.copy(user_input)
        self.driver.find_element_by_xpath(user_xpath).click()
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        pyperclip.copy(temp_user_input)
        time.sleep(1)