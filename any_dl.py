# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import time
import aiohttp
from main_startup.helper_func.basic_helpers import edit_or_reply, humanbytes, time_formatter
from .helper_files.dl_ import AnyDL
from fsplit.filesplit import Filesplit
import os
import re
import pathlib
import uuid
from pyrogram.errors import FloodWait, MessageNotModified
import math
from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, progress

async def download_file(message, url, file_name, show_progress=True):
    c_ = time.time()
    with open(file_name, mode='wb') as f:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                total_length = r.headers.get('content-length') or r.headers.get("Content-Length")
                dl = 0
                if total_length is None:
                    await message.edit(f"<b><u>Downloading This File</b></u> \n<b>File :</b> <code>{file_name}</code> \n<b>File Size :</b> <code>Unknown</code>")
                    f.write(await r.read())
                else:
                    total_length = int(total_length)
                    if not show_progress:
                        await message.edit(f"<b><u>Downloading This File</b></u> \n<b>File :</b> <code>{file_name}</code> \n<b>File Size :</b> <code>{humanbytes(total_length)}</code>")
                        f.write(await r.read())
                        return file_name
                    async for chunk in r.content.iter_chunked(max(int(total_length/500), (1024*1024)*2)):
                        dl += len(chunk)
                        e_ = time.time()
                        diff = e_ - c_
                        percentage = dl * 100 / total_length
                        speed = dl / diff
                        elapsed_time = round(diff) * 1000
                        time_to_completion = round((total_length - dl) / speed) * 1000
                        estimated_total_time = elapsed_time + time_to_completion
                        f.write(chunk)
                        progress_str = "{0}{1} {2}%\n".format(
            "".join(["▰" for i in range(math.floor(percentage / 10))]),
            "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2))
                        r_ = f"<b><u>Downloading This File</b></u> \n<b>File :</b> <code>{file_name}</code> \n<b>File Size :</b> <code>{humanbytes(total_length)}</code> \n<b>Downloaded :</b> <code>{humanbytes(dl)}</code> \n{progress_str} \n\n<b>Speed :</b> <code>{humanbytes(round(speed))}/ps</code> \n<b>ETA :</b> <code>{time_formatter(estimated_total_time)}</code>"
                        try:
                            await message.edit(r_)
                        except MessageNotModified:
                            pass
    return file_name

image_ext = tuple([".jpg", ".png", ".jpeg"])
vid_ext = tuple([".mp4", ".mkv"])
sticker_ext = tuple([".wepb", ".tgs"])
song_ext = tuple([".mp3", ".wav", ".m4a"])


async def upload_file(client, reply_message, message, file_path, caption):
    rndm = uuid.uuid4().hex
    siz_e = os.stat(file_path).st_size
    if siz_e > 2040108421:
        list_ = []
        await message.edit("`File Size More Than 2GB. Telegram Won't Allow This. Splitting Files.`")
        fs = Filesplit()
        if not os.path.exists(f"./splitted_{rndm}"):
            os.makedirs(f"./splitted_{rndm}")
        fs.split(
            file=file_path,
            split_size=2040108421,
            output_dir=f"./splitted_{rndm}",
        )
        file_list(f"./splitted_{rndm}", list_)
        for oof in list_:
            if oof == "fs_manifest.csv":
                return
            await send_file(client, reply_message, oof, caption, message)
    else:
        await send_file(client, reply_message, file_path, caption, message)
    return await message.delete()
    
async def send_file(client, r_msg, file, capt, e_msg):
    c_time = time.time()
    file_name = os.path.basename(file)
    send_as_thumb = False
    if os.path.exists("./main_startup/Cache/thumb.jpg"):
        send_as_thumb = True
    if file.endswith(image_ext):
        await r_msg.reply_video(
            file,
            quote=True,
            caption=capt,
            progress=progress,
            progress_args=(e_msg, c_time, f"`Uploading {file_name}!`", file_name),
        )
    elif file.endswith(vid_ext):
        if send_as_thumb:
            await r_msg.reply_video(
                file,
                quote=True,
                thumb="./main_startup/Cache/thumb.jpg",
                caption=capt,
                progress=progress,
                progress_args=(e_msg, c_time, f"`Uploading {file_name}!`", file_name),
            )
        else:
            await r_msg.reply_video(
                file,
                quote=True,
                caption=capt,
                progress=progress,
                progress_args=(e_msg, c_time, f"`Uploading {file_name}!`", file_name),
            )
    elif file.endswith(".gif"):
        if send_as_thumb:
            await r_msg.reply_animation(
                file,
                quote=True,
                thumb="./main_startup/Cache/thumb.jpg",
                caption=capt,
                progress=progress,
                progress_args=(e_msg, c_time, f"`Uploading {file_name}!`", file_name),
            )
        else:
            await r_msg.reply_animation(
                file,
                quote=True,
                caption=capt,
                progress=progress,
                progress_args=(e_msg, c_time, f"`Uploading {file_name}!`", file_name),
            )
    elif file.endswith(song_ext):
        if send_as_thumb:
            await r_msg.reply_audio(
                file,
                quote=True,
                thumb="./main_startup/Cache/thumb.jpg",
                caption=capt,
                progress=progress,
                progress_args=(e_msg, c_time, f"`Uploading {file_name}!`", file_name),
            )
        else:
            await r_msg.reply_audio(
                file,
                quote=True,
                caption=capt,
                progress=progress,
                progress_args=(e_msg, c_time, f"`Uploading {file_name}!`", file_name),
            )
    elif file.endswith(sticker_ext):
        await r_msg.reply_sticker(
            file,
            quote=True,
            progress=progress,
            progress_args=(e_msg, c_time, f"`Uploading {file_name}!`", file_name),
        )
    else:
        if send_as_thumb:
            await r_msg.reply_document(
                file,
                quote=True,
                thumb="./main_startup/Cache/thumb.jpg",
                caption=capt,
                progress=progress,
                progress_args=(e_msg, c_time, f"`Uploading {file_name}!`", file_name),
            )
        else:
            await r_msg.reply_document(
                file,
                quote=True,
                caption=capt,
                progress=progress,
                progress_args=(e_msg, c_time, f"`Uploading {file_name}!`", file_name),
            )
    
def file_list(path, lisT):
    pathlib.Path(path)
    for filepath in pathlib.Path(path).glob("**/*"):
        lisT.append(filepath.absolute())
    return lisT
                    
@friday_on_cmd(
    ["udl", "any_dl"],
    cmd_help={
        "help": "Download Files From Anonfiles, Mega, MediaFire. If Its Direct Link Make Sure To Give File Name",
        "example": "{ch}udl (file url as input) if url in supported sites else {ch}udl (file url|file name)",
    }
)
async def download_(client, message):
    s = await edit_or_reply(message, "`Trying To Downloading..`")
    dl_client = AnyDL()
    url = get_text(message)
    msg = message.reply_to_message or message
    show_progress = True if url.endswith("--np") else False
    if 'drive.google.com' in url:
        try:
            link = re.findall(r'\bhttps?://drive\.google\.com\S+', url)[0]
        except IndexError:
            return await s.edit("`No Drive Url Links Found!`")
        try:
            file_url, file_name = await dl_client.gdrive(url)
        except BaseException as e:
            return await s.edit(f"**Failed To GET Direct Link ::** `{e}`")
        if file_url == None:
            return await s.edit(f"**Failed To GET Direct Link**")
        file = await download_file(s, file_url, file_name, show_progress)
        caption = f"<b><u>File Downloaded & Uploaded</b></u> \n<b>File Name :</b> <code>{file_name}</code>"
        await upload_file(client, msg, s, file, caption)
        return os.remove(file)
    if "mediafire.com" in url:
        try:
            link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
        except IndexError:
            return await s.edit("`No Media File Url Links Found!`")
        try:
            file_url, file_name, file_size, file_upload_date, caption_, scan_result = await dl_client.media_fire_dl(url)
        except BaseException as e:
            return await s.edit(f"**Failed To GET Direct Link ::** `{e}`")
        if file_url == None:
            return await s.edit(f"**Failed To GET Direct Link**")
        file = await download_file(s, file_url, file_name, show_progress)
        caption = f"<b><u>File Downloaded & Uploaded</b></u> \n<b>File Name :</b> <code>{file_name}</code> \n<b>File Size :</b> <code>{file_size}</code> \n<b>File Upload Date :</b> <code>{file_upload_date}</code> \n<b>File Scan Result :</b> <code>{scan_result}</code> \n<code>{caption_}</code>"
        await upload_file(client, msg, s, file, caption)
        return os.remove(file)
    if "mega.nz" in url:
        try:
            link = re.findall(r'\bhttps?://.*mega\.nz\S+', url)[0]
        except IndexError:
            return await s.edit("`No Mega Url Links Found!`")
        if "folder" in link:
            return await s.edit("`What? Download A Folder? Are You Nutes?")
        try:
            file_url, file_name, file_size = await dl_client.mega_dl(link)
        except BaseException as e:
            return await s.edit(f"**Failed To GET Direct Link ::** `{e}`")
        if file_url == None:
            return await s.edit(f"**Failed To GET Direct Link**")
        file = await download_file(s, file_url, file_name, show_progress)
        file_size = humanbytes(file_size)
        caption = f"<b><u>File Downloaded & Uploaded</b></u> \n<b>File Name :</b> <code>{file_name}</code> \n<b>File Size :</b> <code>{file_size}</code>"
        await upload_file(client, msg, s, file, caption)
        return os.remove(file)
    if "anonfiles" in url:
        try:
            link = re.findall(r"\bhttps?://.*anonfiles\.com\S+", url)[0]
        except IndexError:
            return await s.edit("`No Anon Files Link Found.`")
        try:
            file_url, file_size, file_name = await dl_client.anon_files_dl(link)
        except BaseException as e:
            return await s.edit(f"**Failed To GET Direct Link ::** `{e}`")
        if file_url == None:
            return await s.edit(f"**Failed To GET Direct Link**")
        file = await download_file(s, file_url, file_name, show_progress)
        caption = f"<b><u>File Downloaded & Uploaded</b></u> \n<b>File Name :</b> <code>{file_name}</code> \n<b>File Size :</b> <code>{file_size}</code>"
        await upload_file(client, msg, s, file, caption)
        return os.remove(file)
    else:
        url_ = url.split('|')
        if len(url_) not in [2, 3]:
            return await s.edit("`You Have To Give Me File Name & Url. Please Check Help Menu.`")
        url = url_[0]
        file_name = url_[1]
        try:
            file = await download_file(s, url, file_name, show_progress)    
        except BaseException as e:
            return await s.edit(f"**Failed To Download ::** `{e}`")
        file_size = humanbytes(os.stat(file).st_size)
        caption = f"<b><u>File Downloaded & Uploaded</b></u> \n<b>File Name :</b> <code>{file_name}</code> \n<b>File Size :</b> <code>{file_size}</code>"
        await upload_file(client, msg, s, file, caption)
        return os.remove(file)
    
