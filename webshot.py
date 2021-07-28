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
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, humanbytes
from hashlib import md5
import aiofiles
import os
import aiohttp
import urllib
import validators

async def check_if_url_is_valid(url):
    valid = validators.url(url)
    return bool(valid)

async def screen_shot_(url_s: str):
    """Use AioHttp For Faster Session."""
    async with aiohttp.ClientSession() as session:
        async with session.get('https://screenshotlayer.com') as resp:
            text_ = await resp.text()
    soup = BeautifulSoup(text_, features="html.parser")
    scl_secret = soup.findAll('input')[1]['value']
    print(scl_secret)
    key = md5((str(url_s) + scl_secret).encode()).hexdigest()
    return f'https://screenshotlayer.com/php_helper_scripts/scl_api.php?secret_key={key}&url={url_s}'


async def download_img(url):
    """Download Images Using AioFiles."""
    file_path = None
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                file_path = f"Webshot_FridayUB.png"
                f = await aiofiles.open(file_path, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return file_path

  
@friday_on_cmd(
    ["webshot", "ws"],
    cmd_help={
        "help": "Take A Screen Shot Of A Website.",
        "example": "{ch}webshot https://www.google.com/",
    }
)
async def fetch_webshoot(client, message):
    msg_ = await edit_or_reply(message, "<code>Please Wait Until I Capture This Clear Shot!</code>", parse_mode="html")
    url_ = get_text(message)
    if not url_:
        await msg_.edit("<code>Give Me Url To Fetch A Screen Shot.</code>", parse_mode="html")
        return
    if not await check_if_url_is_valid(url_):
        return await msg_.edit("<code>This is An Invalid Url.</code>", parse_mode="html")
    screen_shot_image = await screen_shot_(url_)
    img_ = await download_img(screen_shot_image)
    img_size = humanbytes(os.stat(img_).st_size)
    if not img_:
        return await msg_.edit("<code>Something Isn't Right. Did You Give Me Valid Url?</code>", parse_mode="html")
    capt_ = f"<b><u>WebShot Captured</b></u> \n<b>URL :</b> <code>{url_}</code> \n<b>SIZE :</b> <code>{img_size}</code> \n\n<b>Powered By FridayUB</b>"
    if message.reply_to_message:
        await client.send_document(
            message.chat.id,
            img_,
            caption=capt_,
            parse_mode="html",
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_document(message.chat.id, img_, parse_mode="html", caption=capt_)
    if os.path.exists(img_):
        os.remove(img_)
    await msg_.delete()