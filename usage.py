"""
Copyright (C) 2020 Adek Maulana.
All rights reserved.
"""

import asyncio
import math
import os
import requests
import asyncio
from functools import wraps
import time
from asyncio import sleep
from pyrogram.types import ChatPermissions
import os
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
    get_user,
    is_admin_or_owner,
)
import heroku3
from main_startup.config_var import Config

heroku_client = None
if Config.HEROKU_API_KEY:
    heroku_client = heroku3.from_key(Config.HEROKU_API_KEY)
    
def _check_heroku(func):
    @wraps(func)
    async def heroku_cli(client, message):
        if not heroku_client:
            await edit_or_reply(message, "`Please Add Heroku API Key For This To Function To Work!`")
        elif heroku_client:
            await func(client, message, heroku_client)
    return heroku_cli
    
@friday_on_cmd(
    ['usage'],
    cmd_help={
        "help": "Check Your App Usage!",
        "example": "{ch}usage"})
@_check_heroku
async def gib_usage(client, message, hc):
  msg_ = await edit_or_reply(message, "`[HEROKU] - Please Wait.`")
  useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
  acc_id = hc.account().id  
  headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {Config.HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
  heroku_api = "https://api.heroku.com"
  path = "/accounts/" + acc_id + "/actions/get-quota"
  r = requests.get(heroku_api + path, headers=headers)
  if r.status_code != 200:
        return await msg_.edit(f"`[{r.status_code}] - Something Isn't Right. Please Try Again Later.`")
  result = r.json()
  quota = result["account_quota"]
  quota_used = result["quota_used"]
  remaining_quota = quota - quota_used
  percentage = math.floor(remaining_quota / quota * 100)
  minutes_remaining = remaining_quota / 60
  hours = math.floor(minutes_remaining / 60)
  minutes = math.floor(minutes_remaining % 60)
  App = result["apps"]
  try:
      App[0]["quota_used"]
  except IndexError:
      AppQuotaUsed = 0
      AppPercentage = 0
  else:
      AppQuotaUsed = App[0]["quota_used"] / 60
      AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
  AppHours = math.floor(AppQuotaUsed / 60)
  AppMinutes = math.floor(AppQuotaUsed % 60)
  app_name = Config.HEROKU_APP_NAME or "Not Specified."
  return await msg_.edit(
        "<b><u>Dyno Usage Data</b></u>:\n\n"
        f"<b>✗ APP NAME :</b> <code>{app_name}</code> \n"
        f"<b>✗ Usage in Hours And Minutes :</b> <code>{AppHours}h {AppMinutes}m</code> \n"
        f"<b>✗ Usage Percentage :</b> <code>[{AppPercentage} %]</code> \n\n\n"
        "<b>✗ Dyno Remaining This Months 📆: </b>\n"
        f"<code>{hours}h {minutes}m</code> \n"
        f"<b>✗ Percentage :</b> <code>[{percentage}%]</code>",
    )