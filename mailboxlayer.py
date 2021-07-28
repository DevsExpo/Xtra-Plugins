# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from bs4 import BeautifulSoup
from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from hashlib import md5
import aiohttp

async def email_info(email_: str):
  """Use AioHttp For Faster Session."""
  async with aiohttp.ClientSession() as session:
      async with session.get('https://mailboxlayer.com') as resp:
          text_ = await resp.text()
  soup = BeautifulSoup(text_, features="html.parser")
  scl_secret = soup.findAll('input')[1]['value']
  key = md5((str(email_) + scl_secret).encode()).hexdigest()
  url = f'https://mailboxlayer.com/php_helper_scripts/email_api_n.php?secret_key={key}&email_address={email_}'
  async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
          info = await resp.json()
  return info
  
@friday_on_cmd(
    ["iev"],
    cmd_help={
        "help": "Check if Mail is Valid Or Not.",
        "example": "{ch}iev idiot@gmail.com",
    },
)
async def get_info_by_email(client, message):
    m_ = await edit_or_reply(message, "<code>Processing...</code>", parse_mode="html")
    emai_l = get_text(message)
    if not emai_l:
      return await m_.edit("<code>Give Me Email As Input.</code>")
    js_n_r = await email_info(str(emai_l))
    if not js_n_r.get("format_valid"):
      return await m_.edit("<code>Invalid Email Format!</code>")
    mx_found = await bool_to_emoji(js_n_r.get("mx_found"))
    smtp_check = await bool_to_emoji(js_n_r.get("smtp_check"))
    disposable = await bool_to_emoji(js_n_r.get("disposable"))
    free = await bool_to_emoji(js_n_r.get("free"))
    score = js_n_r.get("score")
    final_text = f"<b><u>Email Info For {emai_l}</b></u> \n<b>MX :</b> <code>{mx_found}</code> \n<b>SMTP :</b> <code>{smtp_check}</code> \n<b>DISPOSABLE :</b> <code>{disposable}</code> \n<b>IS FREE :</b> <code>{free}</code> \n<b>Mail Score :</b> <code>{score}</code>"
    await m_.edit(final_text, parse_mode='html')
    
async def bool_to_emoji(bool_: bool):
  return "✅" if bool_ else "❌"