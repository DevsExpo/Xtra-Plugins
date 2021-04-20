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

async def phone_info(phone_number: int):
  """Use AioHttp For Faster Session."""
  async with aiohttp.ClientSession() as session:
      async with session.get('https://numverify.com/') as resp:
          text_ = await resp.text()
  soup = BeautifulSoup(text_, features="html.parser")
  scl_secret = soup.findAll('input')[1]['value']
  key = md5((str(phone_number) + scl_secret).encode()).hexdigest()
  url = f'https://numverify.com/php_helper_scripts/phone_api.php?secret_key={key}&number={phone_number}'
  async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
          info = await resp.json()
  return info
  
@friday_on_cmd(
    ["phone"],
    cmd_help={
        "help": "Get Basic Details About A Phone Number.",
        "example": "{ch}phone +919581988792",
    },
)
async def get_info_by_number(client, message):
    m_ = await edit_or_reply(message, "<code>Processing...</code>", parse_mode="html")
    numbe_r = get_text(message)
    if not numbe_r:
      return await m_.edit("<code>Give Me Phone Number As Input.</code>")
    try:
      numbe_r = int(numbe_r)
    except ValueError:
      return await m_.edit("<code>Invalid Phone Number.</code>")
    js_n_r = await phone_info(int(numbe_r))
    if not js_n_r.get("valid"):
      return await m_.edit("<code>Invalid Phone Number!</code>")
    final_text = f"<b><u>Phone Info For {numbe_r}</b></u> \n<b>Country :</b> {js_n_r.get('country_name')} \n<b>Location :</b> {js_n_r.get('location')} \n<b>Carrier :</b> {js_n_r.get('carrier')} \n<b>Line Type :</b> {js_n_r.get('line_type').title()}"
    await m_.edit(final_text, parse_mode='html')