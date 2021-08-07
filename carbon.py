# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import asyncio
import logging
from selenium.common.exceptions import NoSuchElementException
from main_startup import Config
import random
import os
from urllib.parse import urlencode, quote_plus
from main_startup.core.decorators import friday_on_cmd
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, run_in_exc


GOOGLE_CHROME_BIN = Config.CHROME_BIN_PATH
CHROME_DRIVER = Config.CHROME_DRIVER_PATH

@run_in_exc
def make_carbon(code, driver, lang="auto"):
    code = urlencode(code)
    url = f'https://carbon.now.sh/?l={lang}&code={code}'
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': './'}}
    command_result = driver.execute("send_command", params)
    driver.get(url)
    type_ = '//*[@id="__next"]/main/div[2]/div[2]/div[1]/div[1]/div/span[2]'
    em = "export-menu"
    png_xpath = '//*[@id="export-png"]'
    four_x_path = '//*[@id="__next"]/main/div[2]/div[2]/div[1]/div[3]/div[4]/div[3]/div[2]/div[3]/div/button[3]' 
    color_used_xpath = '/html/body/div[1]/main/div[2]/div[2]/div[1]/div[1]/div/span[2]/input'
    random_int = random.randint(1, 29)
    value_ = "downshift-0-item-" + str(random_int)
    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.XPATH, type_))).click()
    wait.until(EC.visibility_of_element_located((By.ID, value_))).click()
    wait.until(EC.visibility_of_element_located((By.ID, em))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, four_x_path))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, png_xpath))).click()
    file_ = "./carbon.png"
    color_used = wait.until(EC.visibility_of_element_located((By.XPATH, color_used_xpath))).get_attribute("value")
    return file_, color_used


@friday_on_cmd(
    ["carbon", "karb"],
    cmd_help={
        "help": "`Carbonize Codes In A Cool Way.`",
        "example": "{ch}carbon (input or reply_message will be taken)",
    },
)
async def karb(client, message):
    e_ = await edit_or_reply(message, "`Carbonzing Code...`")
    code = get_text(message)
    if not code:
        if not message.reply_to_message:
           return await message.edit("`Nothing To Carbonize..`")
        if not message.reply_to_message.text:
           return await message.edit("`Nothing To Carbonize...`")
    code = code or message.reply_to_message.text
    reply_ = message.reply_to_message or message
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {'download.default_directory' : './'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=chrome_options)
    try:
        carbon_file, value_ = await make_carbon(code, driver)
        await asyncio.sleep(5)
    except BaseException as e:
        await e_.edit(f"[Selenium] - [Chrome - Driver] - [Carbon] >> {e}")
        return driver.quit()
    driver.quit()
    await reply_.reply_photo(carbon_file, caption=f"<b>Code Carbonized Using Friday</b> \n<b>Style Used :</b> <code>{value_}</code>")
    await e_.delete()
