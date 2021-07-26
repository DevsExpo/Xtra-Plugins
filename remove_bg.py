# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.core.decorators import friday_on_cmd, listen
from pyrogram import filters
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from main_startup.config_var import Config
import logging
from functools import wraps
import io
import os
from datetime import datetime
import requests
from main_startup.helper_func.plugin_helpers import convert_to_image


key = Config.REM_BG_API_KEY or None

def _check_rmbg(func):
    @wraps(func)
    async def check_rmbg(client, message):
        if not key:
            await edit_or_reply(message, "`Is Your RMBG Api Key Valid Or You Didn't Add It??`")
        else:
            await func(client, message)
    return check_rmbg

@friday_on_cmd(
        ["rmbg"],
        is_official=False,
        cmd_help={
            "help": "Remove Background Of Image!",
            "example": "{ch}rmbg (reply to image)"
        }
    )
@_check_rmbg
async def rmbg(client, message):
    pablo = await edit_or_reply(message, "`Processing...`")
    if not message.reply_to_message:
        await pablo.edit("`Reply To A Image Please!`")
        return
    cool = await convert_to_image(message, client)
    if not cool:
        await pablo.edit("`Reply to a valid media first.`")
        return
    start = datetime.now()
    await pablo.edit("sending to ReMove.BG")
    input_file_name = cool
    headers = {
        "X-API-Key": key,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )
    os.remove(cool)
    output_file_name = r
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "BG_less.png"
            await client.send_document(
                message.chat.id,
                remove_bg_image)
        end = datetime.now()
        ms = (end - start).seconds
        await pablo.edit(
            "Removed image's Background in {} seconds, powered by @FridayOT".format(ms)
        )
    else:
        await pablo.edit(
            "ReMove.BG API returned Errors. Please report to @FridayOT\n`{}".format(
                output_file_name.content.decode("UTF-8")
            )
        )

