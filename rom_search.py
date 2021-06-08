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
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text

GOOGLE_CHROME_BIN = Config.CHROME_BIN_PATH
CHROME_DRIVER = Config.CHROME_DRIVER_PATH
ch_ = Config.COMMAND_HANDLER

async def get_url(query: str):
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
    await asyncio.sleep(5)
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
    return await fetch_data(href)

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

async def realme_rom_search(query: str):
    url = "https://realmeupdater.com/"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=chrome_options)
    driver.get(url)
    await asyncio.sleep(5)
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)
    driver.get("https://realmeupdater.com/")
    driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
    wait.until(EC.visibility_of_element_located((By.ID, "select2-device-container"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/span/span/span[1]/input"))).send_keys(query)
    try:
        all_options = driver.find_elements(By.CSS_SELECTOR, "#select2-device-results li")
    except NoSuchElementException:
        driver.quit()
        return None, None, None, None, None
    if not all_options:
        driver.quit()
        return None, None, None, None, None
    all_options[0].click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div[1]/div[2]/div/div/div[2]/div/div[1]/form/div/div[3]/button"))).click()
    device = wait.until(EC.visibility_of_element_located((By.XPATH, "//h5[./b[text()='Device: ']]"))).text.split(maxsplit=1)[1]
    system = wait.until(EC.visibility_of_element_located((By.XPATH, "//h5[./b[text()='System: ']]"))).text.split(maxsplit=1)[1]
    size = wait.until(EC.visibility_of_element_located((By.XPATH, "//h5[./b[text()='Size: ']]"))).text.split(maxsplit=1)[1]
    rdate = wait.until(EC.visibility_of_element_located((By.XPATH, "//h5[./b[text()='Release Date: ']]"))).text.split(": ", maxsplit=1)[1]
    file_name = wait.until(EC.visibility_of_element_located((By.ID, "filename"))).text
    file_url = f"https://download.c.realme.com/osupdate/{file_name}"
    driver.quit()
    return file_url, rdate, size, system, device
    
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
    url, device_name, version, size, rs_date, type_, package_name = await get_url(query)
    if url == None:
        return await e_.edit("`No Results Matching You Query.`")
    final_ = f"<b>MIUI Search</b> \n<b>Model :</b> <code>{device_name}</code> \n<b>Version :</b> <code>{version}</code> \n<b>Size :</b> <code>{size}</code> \n<b>Release Date :</b> <code>{rs_date}</code> \n<b>Type :</b> <code>{type_}</code> \nPackage Name :</b> <code>{package_name}</code> \n<b>Download :</b> <code>{ch_}udl {url}</code>"
    await message.edit(final_)
    
@friday_on_cmd(
    ["rms"],
    cmd_help={
        "help": "`Search Realme Roms :)`",
        "example": "{ch}rms pro",
    },
)
async def rm_s(client, message):
    e_ = await edit_or_reply(message, "`Please Wait..`")
    query = get_text(message)
    if not query:
        return await e_.edit("`Please Give Me An Query.`")
    file_url, r_date, size, system, device = await realme_rom_search(query)
    if file_url == None:
        return await e_.edit("`No Results Matching You Query.`")
    final_ = f"<b>RealMeRom Search</b> \n<b>Device :</b> <code>{device}</code> \n<b>System :</b> <code>{system}</code> \n<b>Size :</b> <code>{size}</code> \n<b>Release Date :</b> <code>{r_date}</code> \n<b>Download :</b> <code>{ch_}udl {file_url}</code>"
    await message.edit(final_)