# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.


import aiohttp
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from bs4 import BeautifulSoup
from pyrogram import filters
from main_startup.core.decorators import friday_on_cmd


@friday_on_cmd(
    ["cs"],
    cmd_help={
        "help": "Get live cricket score info",
        "example": "{ch}cs",
    },
)
async def _(client, message):
    score_page = "http://static.cricinfo.com/rss/livescores.xml"
    async with aiohttp.ClientSession() as session:
      async with session.get(score_page) as resp:
          page = await resp.text()
    soup = BeautifulSoup(page, "html.parser")
    result = soup.find_all("description")
    Sed = "".join(match.get_text() + "\n\n" for match in result)
    await edit_or_reply(
        message,
        f"<b><u>Match information Gathered Successfully</b></u>\n\n\n<code>{Sed}</code>",
        parse_mode="html",
    )

