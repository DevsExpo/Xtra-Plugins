# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import asyncio
from main_startup import Config
import aiohttp
from bs4 import BeautifulSoup
from lxml import etree
from main_startup.core.decorators import friday_on_cmd
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, run_in_exc

GOOGLE_CHROME_BIN = Config.CHROME_BIN_PATH
CHROME_DRIVER = Config.CHROME_DRIVER_PATH
ch_ = Config.COMMAND_HANDLER

@run_in_exc
def get_url(query: str):
    url = "https://xiaomifirmwareupdater.com/miui/"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=chrome_options)
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#miui_filter > label > input"))).send_keys(query)
    try:
        bruh = driver.find_element_by_css_selector("#miui > tbody > tr:nth-child(1) > td:nth-child(8) > a")
    except NoSuchElementException:
        driver.quit()
        return None, None, None, None, None, None, None
    if not bruh:
        driver.quit()
        return None, None, None, None, None, None, None
    href = bruh.get_attribute('href')
    driver.quit()
    return href

async def fetch_data(url: str):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        b_ = BeautifulSoup(await resp.read(), 'lxml')
        device_name = b_.select("#downloads > div > ul > li:nth-child(1) > h5")[0].text.split("Device: ")[1]
        version = b_.select("#downloads > div > ul > li:nth-child(3) > h5")[0].text.split("Version: ")[1]
        size = b_.select("#downloads > div > ul > li:nth-child(6) > h5")[0].text.split("Size: ")[1]
        rs_date = b_.select("#downloads > div > ul > li:nth-child(7) > h5")[0].text.split("Release Date: ")[1]
        type_ = b_.select("#downloads > div > ul > li:nth-child(5) > h5")[0].text.split("Type: ")[1]
        package_name = b_.find("span", {"id": "filename"}).text
        url = f"https://bigota.d.miui.com/{version}/{package_name}"
        return url, device_name, version, size, rs_date, type_, package_name

    
@friday_on_cmd(
    ["mrs"],
    cmd_help={
        "help": "`Search MiUi Roms :)`",
        "example": "{ch}mrs mi 10 pro",
    },
)
async def m_(client, message):
    e_ = await edit_or_reply(message, "`Please Wait..`")
    query = get_text(message)
    if not query:
        return await e_.edit("`Please Give Me An Query.`")
    href = await get_url(query)
    if href is None:
        return await e_.edit("`No Results Matching You Query.`")
    url, device_name, version, size, rs_date, type_, package_name = await fetch_data(href)
    final_ = f"<b>MIUI Search</b> \n<b>Model :</b> <code>{device_name}</code> \n<b>Version :</b> <code>{version}</code> \n<b>Size :</b> <code>{size}</code> \n<b>Release Date :</b> <code>{rs_date}</code> \n<b>Type :</b> <code>{type_}</code> \n<b>Package Name :</b> <code>{package_name}</code> \n<b>Download :</b> <code>{ch_}udl {url}</code>"
    await message.edit(final_)