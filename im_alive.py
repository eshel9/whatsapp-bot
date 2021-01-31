#!/home/esh/Projects/Whatsapp-bot/whatsapp-venv/bin/python3
import psutil
import time
import datetime
import sys
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

desired_recipient = sys.argv[1]
message = sys.argv[2]

# first, kill all chromes, since the webdriver will not accept opening
# two instances with the same user-data-dir
chrome_process_names = ["chrome", "chromedriver"]
killed_flag = False
try:
    for proc in psutil.process_iter():
        if proc.name() in chrome_process_names:
            killed_flag = True
            proc.kill()
    if killed_flag:
        print("killed all chromes")
except Exception:
    pass

# open controlled chrome, with user's cookies
try:
    raise Exception
    user_data_dir = "/home/esh/.config/google-chrome/"
    options = ChromeOptions()
    options.add_argument(f"user-data-dir={user_data_dir}")
    executable_path = '/home/esh/Projects/Whatsapp-bot/whatsapp-venv/chrome_drive_installation/chromedriver'
    browser = Chrome(executable_path, options=options)
    browser.get('https://web.whatsapp.com')

    # find recipient
    search_box_xpath = \
        '/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]'
    wait = WebDriverWait(browser, 50)
    until_func = EC.presence_of_element_located

    wait.until(until_func((By.XPATH, search_box_xpath)))
except Exception:
    print(f"{datetime.datetime.now()}: failed!")
    # play alarm clock so that I can send manually if doesn't work
    import os
    beep_duration = 1  # seconds
    beep_times = 5  # seconds
    freq = 440  # Hz
    for _ in range(beep_times):
        os.system(f'play -nq -t alsa synth {beep_duration} sine {freq}')
    exit()

search_box = browser.find_element_by_xpath(search_box_xpath)
search_box.click()
search_box.send_keys(desired_recipient)
search_box.send_keys(Keys.RETURN)
time.sleep(3)   # For safety only

# send message
# current active element is message box
message_box = browser._switch_to.active_element
message_box.send_keys(message)
time.sleep(3)   # For safety only
message_box.send_keys(Keys.RETURN)

# output to whom we actually sent
actual_recipient_xpath = '/html/body/div[1]/div/div/div[4]/div/header/div[2]/div/div/span'
actual_recipient_element = browser.find_element_by_xpath(actual_recipient_xpath)
actual_recipient = actual_recipient_element.get_attribute("title")
print(f"{datetime.datetime.now()} | sent message: {message}\nto: {actual_recipient}")

time.sleep(10)
browser.close()
print("closing")
