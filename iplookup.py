# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
import aiohttp

@friday_on_cmd(
    ["ip"],
    cmd_help={
        "help": "Get Info About IP.",
        "example": "{ch}ip (ip)",
    },
)
async def cool_ip(client, message):
    input_str = get_text(message)
    msg = await edit_or_reply(message, "`Please Wait.`")
    if not input_str:
        return await msg.edit("`Give Me IP As Input.`")
    url = f"https://ipapi.com/ip_api.php?ip={input_str}"    
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
          r = await resp.json()
    if not r.get("hostname"):
        return await msg.edit("<code>Invalid IP. Please Check Hostname.</code>")
    ok = f"""<b>IP :</b> <code>{r.get("ip")}</code> \n<b>Hostname :</b> <code>{r.get("hostname")}</code> \n<b>Type :</b> <code>{r.get("type")}</code> \n<b>Country Name :</b> <code>{r.get("country_name")} {r.get("location").get("country_flag_emoji")}</code> \n<b>Region Name :</b> <code>{r.get("region_name")}</code> \n<b>City :</b> <code>{r.get("city")}</code> \n<b>Zip :</b> <code>{r.get("zip")}</code> \n<b>Latitude :</b> <code>{r.get("latitude")}</code> \n<b>Longitude :</b> <code>{r.get("longitude")}</code> \n<b>Current Time :</b> <code>{r.get("time_zone").get("current_time")}</code> \n<b>Currency :</b> <code>{r.get("currency").get("name")}</code> \n<b>ISP :</b> <code>{r.get("connection").get("isp")}</code> \n<b>Is Proxy :</b> <code>{bool_to_emoji(r.get("security").get("is_proxy"))}</code> \n<b>Is Crawler :</b> <code>{bool_to_emoji(r.get("security").get("is_crawler"))}</code> \n<b>Treat Level :</b> <code>{r.get("security").get("threat_level")}</code>"""
    await msg.edit(ok)
     


def bool_to_emoji(bool_: bool):
    return "✅" if bool_ else "❌"
