# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import aiohttp
import asyncio
import re
import random
from main_startup.config_var import Config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
    get_user,
    iter_chats,
    run_in_exc
)
from main_startup.helper_func.logger_s import LogIt
from plugins import devs_id
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

GOOGLE_CHROME_BIN = Config.CHROME_BIN_PATH
CHROME_DRIVER = Config.CHROME_DRIVER_PATH

@run_in_exc
def namso_gen(bin, no_of_result=15):
    url = "https://namso-gen.com/"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=chrome_options)
    driver.get(url)
    w = WebDriverWait(driver, 20)
    bin_xpath = '//*[@id="main"]/div/div/div[3]/div[1]/form/div[1]/label/input'
    no_of_r_xpath = '//*[@id="main"]/div/div/div[3]/div[1]/form/div[3]/div[3]/label/input'
    button_xpath = '//*[@id="main"]/div/div/div[3]/div[1]/form/div[5]/button'
    w.until(EC.visibility_of_element_located((By.XPATH, bin_xpath))).send_keys(bin)
    elem3 = w.until(EC.visibility_of_element_located((By.XPATH, no_of_r_xpath)))
    for i in range(2):
        elem3.send_keys(Keys.BACKSPACE)
    elem3 = w.until(EC.visibility_of_element_located((By.XPATH, no_of_r_xpath)))
    elem3.send_keys(no_of_result)
    w.until(EC.visibility_of_element_located((By.XPATH, button_xpath))).click()
    s = w.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="result"]'))).get_attribute("value")
    driver.quit()
    return s

@friday_on_cmd(
    ["namsogen"],
    cmd_help={
        "help": "Gen CC From Bin Using Namso-Gen",
        "example": "{ch}namsogen 48950456",
    },
)
async def ns_gen(client, message):
    msg = await edit_or_reply(message, "`Please Wait`")
    input = get_text(message)
    if not input:
        return await msg.edit("`Give Me Bin.`")
    input_ = input.split(" ")
    no_of_results = 15
    if len(input_) == 2:
        bin = input_[0]
        no_of_results = input_[1] if input_[1].isdigit() else 15
    else:
        bin = input
    s = await namso_gen(bin, no_of_results)
    if not s:
        return await msg.edit("`Invalid Bin Given Or Results Limit Reached.`")
    t = f"""
**Bin :** `{bin}`

**Results - ({no_of_results}) :**

`{s}`


**Powered By FridayUb**
"""
    await msg.edit(t, parse_mode="md")
    
def stark_finder(to_find, from_find):
    if re.search(r"( |^|[^\w])" + re.escape(to_find) + r"( |$|[^\w])", from_find, flags=re.IGNORECASE):
        return True
    return False
    
my_code = {
    400: "『! Invalid Key !』",
    200: "『 Valid Key 』",
    69: "『! Only Testing Mode Enabled !』",
    498: "『! Key Expired !』"
}

async def check_stripe_key(key_: str):
    url = "https://api.stripe.com/v1/tokens"
    check_ = {
                'card[number]': 5154620061414478,
                'card[cvc]': random.randint(552, 999),
                'card[exp_month]': random.randint(1, 12),
                'card[exp_year]': random.randint(2022, 2026),
                'key': key_,
            }
    async with aiohttp.ClientSession() as session:
      async with session.post(url, params=check_) as resp:
          response_ = await resp.text()
    if stark_finder("invalid api key provided", response_):
        return 400
    elif stark_finder("api_key_expired", response_):
        return 498
    elif stark_finder("testmode_charges_only", response_):
        return 69
    elif stark_finder("test_mode_live_card", response_):
        return 69
    elif stark_finder("invalid_request_error", response_):
        return 400
    else:
        return 200
    
@friday_on_cmd(
    ["sk"],
    cmd_help={
        "help": "Check Sk.",
        "example": "{ch}sk (key as input)",
    },
)
async def check_sk_key(client, message):
    msg = await edit_or_reply(message, "`Please Wait`")
    key_ = get_text(message)
    if not key_:
        return await msg.edit("`Give Me A Key To Check.`")
    key_result = await check_stripe_key(key_)
    _result_to_show = f"<b><u>Stripe Key Check Result</b></u> \n<b>Key :</b> <code>{key_}</code> \n<b>Response :</b> <code>{my_code[key_result]}</code> \n<b><u>Check Using FridayUB</b></u>"
    await msg.edit(_result_to_show)
