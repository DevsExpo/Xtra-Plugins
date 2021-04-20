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
from main_startup.helper_func.plugin_helpers import convert_to_image
import requests
import os

headers = {
    'authority': 'api8.ocr.space',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'apikey': '5a64d478-9c89-43d8-88e3-c65de9999580',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.39',
    'origin': 'https://ocr.space',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://ocr.space/',
    'accept-language': 'en-US,en;q=0.9',
}

async def read_ocr_(img_path):
    path_ = {"file": (img_path, open(img_path, "rb"))}
    response = requests.post('https://api8.ocr.space/parse/image', headers=headers, files=path_)
    return response.json()["ParsedResults"][0]['ParsedText']


@friday_on_cmd(
    ["ocr"],
    cmd_help={
        "help": "Ocr Images.",
        "example": "{ch}ocr (replying to image with texts)",
    },
)
async def idontknowhowtospell(client, message):
    msg_ = await edit_or_reply(message, "<code>Reading Please..</code>", parse_mode="html")
    if not message.reply_to_message:
        return await msg_.edit("<code>Please Reply To A Image.</code>", parse_mode="html")
    cool = await convert_to_image(message, client)
    if not cool:
        await msg_.edit("<code>Reply to a valid media first.</code>", parse_mode="html")
        return
    if not os.path.exists(cool):
        await msg_.edit("<code>Invalid Media!</code>", parse_mode="html")
        return
    text_ = await read_ocr_(cool)
    if not text_:
        return await msg_.edit("`No Text Found in Image.`")
    await msg_.edit(f"<u><b>OCR RESULT</u></b> \n\n<code>{text_}</code>", parse_mode="html")