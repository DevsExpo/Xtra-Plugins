# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import aiohttp
from pyrogram import filters
from xtraplugins.dB.harem_heckdb import add_chat, is_chat_in_db, rm_chat
from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
    get_user,
    iter_chats,
)
from main_startup.helper_func.logger_s import LogIt
from plugins import devs_id
import io
import os
import asyncio
import re
import urllib
import shutil
from re import findall
import requests
from bs4 import BeautifulSoup


u_ = """Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36"""

headers_ = [("User-agent", u_)]

async def ParseSauce(googleurl):
    """Parse/Scrape the HTML code for the info we want."""
    async with aiohttp.ClientSession(headers=headers_) as session:
      async with session.get(googleurl) as resp:
          source = await resp.read()
    soup = BeautifulSoup(source, "html.parser")
    results = {"similar_images": "", "best_guess": ""}
    try:
        for similar_image in soup.findAll("input", {"class": "gLFyf"}):
            url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
                similar_image.get("value")
            )
            results["similar_images"] = url
    except BaseException:
        pass
    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()
    return results

@friday_on_cmd(
    ["ahc"],
    cmd_help={
        "help": "Add A Chat To Harem List.",
        "example": "{ch}ahc (current chat will be taken)",
    },
)
async def add_harem_hc(client, message):
    pablo = await edit_or_reply(message, "`Processing..`")
    if await is_chat_in_db(int(message.chat.id)):
        await pablo.edit("`This Chat is Already In My DB`")
        return
    await add_chat(int(message.chat.id))
    await pablo.edit("`Successfully Added Chat To Harem Watch.`")


@friday_on_cmd(
    ["rmhc"],
    group_only=True,
    cmd_help={"help": "Remove Chat From Harem List.", "example": "{ch}rmhc"},
)
async def remove_nsfw(client, message):
    pablo = await edit_or_reply(message, "`Processing..`")
    if not await is_chat_in_db(int(message.chat.id)):
        await pablo.edit("`This Chat is Not in dB.`")
        return
    await rm_chat(int(message.chat.id))
    await pablo.edit("`Successfully Removed Chat From Harem Watch.`")

async def is_harem_enabled(f, client, message):
    if Config.ENABLE_WAIFU_FOR_ALL_CHATS:
        return bool(True)
    if await is_chat_in_db(int(message.chat.id)):
        return bool(True)
    else:
        return bool(False)

async def harem_event(f, client, message):
    if not message:
        return bool(False)
    if not message.photo:
        return bool(False)
    if not message.caption:
        return bool(False)
    if "add" in message.caption.lower():
            return bool(True)
    return bool(False)


harem_event = filters.create(func=harem_event, name="harem_event")
is_harem_enabled = filters.create(func=is_harem_enabled, name="is_harem_enabled")



@listen(filters.user([int(792028928)]) & ~filters.edited & is_harem_enabled & harem_event & filters.group)
async def harem_catcher(client, message):
    img = await message.download()
    searchUrl = "https://www.google.com/searchbyimage/upload"
    file_img = {"encoded_image": (img, open(img, "rb")), "image_content": ""}
    response = requests.post(searchUrl, files=file_img, allow_redirects=False)
    if os.path.exists(img):
        os.remove(img)
    if response.status_code == 400:
        return logging.info("(Waifu Catch Failed) - [Invalid Response]")
    fetchUrl = response.headers["Location"]
    match = await ParseSauce(fetchUrl + "&preferences?hl=en&fg=1#languages")
    guessp = match["best_guess"]
    if not guessp:
       return logging.info("(Waifu Catch Failed.) \nERROR : 404: Waifu Not Found.")
    guess = guessp.replace("Results for", "").replace(" ", "")
    kek = await message.reply_text(message.chat.id, f"/protecc {guess}")
    await asyncio.sleep(5)
    await kek.delete()
    log = LogIt(message)
    msg_to_log = f"[{guess}] - New Waifu Appeared - ({message.chat.title}) - Sucessfully Tried To Protecc"
    await log.log_msg(client, msg_to_log)
