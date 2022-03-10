# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.


import os
import asyncio
from shazamio import Shazam
from main_startup.core.startup_helpers import run_cmd
import datetime
import requests
import time
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, humanbytes

async def shazam(file):
    shazam = Shazam()
    try:
        r = await shazam.recognize_song(file)
    except:
        return None, None, None
    if not r:
        return None, None, None
    track = r.get("track")
    nt = track.get("images")
    image = nt.get("coverarthq")
    by = track.get("subtitle")
    title = track.get("title")
    return image, by, title

async def convert_to_audio(vid_path):
    stark_cmd = f"ffmpeg -i {vid_path} -map 0:a friday.mp3"
    await runcmd(stark_cmd)
    final_warner = "friday.mp3"
    if not os.path.exists(final_warner):
        return None
    return final_warner

@friday_on_cmd(
    ["shazam"],
    cmd_help={
        "help": "Recognize / Discover A Song",
        "example": "{ch}shazam (reply to music file)",
    },
)
async def shazam_(client, message):
    stime = time.time()
    msg = await edit_or_reply(message, "`Shazaming This Song.")
    if not message.reply_to_message:
        return await msg.edit("`Reply To Song File`")
    if not (message.reply_to_message.audio or message.reply_to_message.voice or message.reply_to_message.video):
        return await msg.edit("`Reply To Audio File.`")
    if message.reply_to_message.video:
        video_file = await message.reply_to_message.download()
        music_file = await convert_to_audio(video_file)
        dur = message.reply_to_message.video.duration
        if not music_file:
            return await msg.edit("`Unable To Convert To Song File. Is This A Valid File?`")
    elif (message.reply_to_message.voice or message.reply_to_message.audio):
        dur = message.reply_to_message.voice.duration if message.reply_to_message.voice else message.reply_to_message.audio.duration
        music_file = await message.reply_to_message.download()
    size_ = humanbytes(os.stat(music_file).st_size)
    dur = datetime.timedelta(seconds=dur)
    thumb, by, title = await shazam(music_file)
    if title is None:
        return await msg.edit("`No Results Found.`")
    etime = time.time()
    t_k = round(etime - stime)
    caption = f"""<b><u>Shazamed Song</b></u>
    
<b>Song Name :</b> <code>{title}</code>
<b>Singer :</b> <code>{by}</code>
<b>Duration :</b> <code>{dur}</code>
<b>Size :</b> <code>{size_}</code>
<b>Time Taken :</b> <code>{t_k} Seconds</code>

<b><u>Shazamed By FridayUB</b></u>
    """
    if thumb:
        await msg.delete()
        await message.reply_to_message.reply_photo(thumb, caption=caption, quote=True)
    else:
        await msg.edit(caption)