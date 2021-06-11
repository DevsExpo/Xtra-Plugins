# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import os
import logging
import ffmpeg
from main_startup import Friday
import time
import calendar
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, humanbytes
from pytgcalls import GroupCall, GroupCallAction
import signal
import random
import string
import asyncio
import os
import time
import requests
import datetime
from youtube_dl import YoutubeDL
from youtubesearchpython import SearchVideos

s_dict = {}
GPC = {}

@friday_on_cmd(
    ["playlist"],
    is_official=False,
    cmd_help={"help": "Get Current Chat Playlist!", "example": "{ch}playlist"},
)
async def pl(client, message):
    group_call = GPC.get((message.chat.id, client.me.id))
    play = await edit_or_reply(message, "`Please Wait!`")
    song = f"**PlayList in {message.chat.title}** \n"
    sno = 0
    s = s_dict.get((message.chat.id, client.me.id))
    if not group_call:
        return await play.edit("`Voice Chat Not Connected. So How Am i Supposed To Give You Playlist?`")
    if not s:
        if group_call.is_connected:
            return await play.edit(f"**Currently Playing :** `{str(group_call.input_filename).replace('.raw', '')}`")
        else:
            return await play.edit("`Voice Chat Not Connected. So How Am i Supposed To Give You Playlist?`")
    if group_call.is_connected:
        song += f"**Currently Playing :** `{str(group_call.input_filename).replace('.raw', '')}` \n\n"
    for i in s:
        sno += 1
        song += f"**{sno} ▶** `{i['song_name']} | {i['singer']} | {i['dur']}` \n\n" 
    await play.edit(song)
    
async def get_chat_(client, chat_):
    chat_ = str(chat_)
    if chat_.startswith("-100"):
        try:
            return (await client.get_chat(int(chat_))).id
        except ValueError:
            chat_ = chat_.split("-100")[1]
            chat_ = '-' + str(chat_)
            return int(chat_)
        
async def playout_ended_handler(group_call, filename):
    client_ = group_call.client
    chat_ = await get_chat_(client_, f"-100{group_call.full_chat.id}")
    chat_ = int(chat_)
    s = s_dict.get((chat_, client_.me.id))
    if os.path.exists(group_call.input_filename):
        os.remove(group_call.input_filename)
    if not s:
        await group_call.stop()
        return
    name_ = s[0]['song_name']
    singer_ = s[0]['singer']
    dur_ = s[0]['dur']
    holi = s[0]['raw']
    link = s[0]['url']
    file_size = humanbytes(os.stat(holi).st_size)
    song_info = f'<u><b>🎼 Now Playing 🎼</b></u> \n<b>🎵 Song :</b> <a href="{link}">{name_}</a> \n<b>🎸 Singer :</b> <code>{singer_}</code> \n<b>⏲️ Duration :</b> <code>{dur_}</code> \n<b>📂 Size :</b> <code>{file_size}</code>'
    await client_.send_message(
        chat_, 
        song_info
    )
    s.pop(0)
    logging.debug(song_info)
    group_call.input_filename = holi

@friday_on_cmd(
    ["skip_vc"],
    is_official=False,
    cmd_help={"help": "Skip Song in Playlist.", "example": "{ch}skip_vc (key_len)"}
)
async def ski_p(client, message):
    m_ = await edit_or_reply(message, "`Please Wait!`")
    no_t_s = get_text(message)
    group_call = GPC.get((message.chat.id, client.me.id))
    s = s_dict.get((message.chat.id, client.me.id))
    if not group_call:
        await m_.edit("`Is Group Call Even Connected?`")
        return 
    if not group_call.is_connected:
        await m_.edit("`Is Group Call Even Connected?`")
        return 
    if not no_t_s:
        return await m_.edit("`Give Me Valid List Key Len.`")
    if no_t_s == "current":
        if not s:
            return await m_.edit("`No Song in List. So Stopping Song is A Smarter Way.`")
        next_s = s[0]['raw']
        s.pop(0)
        name = str(s[0]['song_name'])
        prev = group_call.input_filename
        group_call.input_filename = next_s
        return await m_.edit(f"`Skipped {prev}. Now Playing {name}!`")       
    else:
        if not s:
            return await m_.edit("`There is No Playlist!`")
        if not no_t_s.isdigit():
            return await m_.edit("`Input Should Be In Digits.`")
        no_t_s = int(no_t_s)
        if int(no_t_s) == 0:
            return await m_.edit("`0? What?`")
        no_t_s = int(no_t_s - 1)
        try:
            s_ = s[no_t_s]['song_name']
            s.pop(no_t_s)
        except:
            return await m_.edit("`Invalid Key.`")
        return await m_.edit(f"`Skipped : {s_} At Position #{no_t_s}`")
                            
    
@friday_on_cmd(
    ["play_vc"],
    is_official=False,
    cmd_help={"help": "Play The Song In VC Directly From Youtube Or Telegram!", "example": "{ch}play_vc (song query)"},
)
async def play_m(client, message):
    group_call = GPC.get((message.chat.id, client.me.id))
    u_s = await edit_or_reply(message, "`Processing..`")
    input_str = get_text(message)
    if not input_str:
         if not message.reply_to_message:
             return await u_s.edit_text("`Reply To A File To PLay It.`")
         if message.reply_to_message.audio:
             await u_s.edit_text("`Please Wait, Let Me Download This File!`")
             audio = message.reply_to_message.audio
             audio_original = await message.reply_to_message.download()
             vid_title = audio.title or audio.file_name
             uploade_r = message.reply_to_message.audio.performer or "Unknown Artist."
             dura_ = message.reply_to_message.audio.duration
             dur = datetime.timedelta(seconds=dura_)
             raw_file_name = ''.join([random.choice(string.ascii_lowercase) for i in range(5)]) + ".raw"
             #raw_file_name = f"{audio.file_name}.raw" if audio.file_name else f"{audio.title}.raw"
             url = message.reply_to_message.link
         else:
             return await u_s.edit("`Reply To A File To PLay It.`")
    else:
         search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
         rt = search.result()
         result_s = rt.get("search_result")
         if not result_s:
            return await u_s.edit(f"`No Song Found Matching With Query - {input_str}, Please Try Giving Some Other Name.`")
         url = result_s[0]["link"]
         dur = result_s[0]["duration"]
         vid_title = result_s[0]["title"]
         yt_id = result_s[0]["id"]
         uploade_r = result_s[0]["channel"]
         opts = {
             "format": "bestaudio",
             "addmetadata": True,
             "key": "FFmpegMetadata",
             "writethumbnail": True,
             "prefer_ffmpeg": True,
             "geo_bypass": True,
             "nocheckcertificate": True,
             "postprocessors": [
                 {
                     "key": "FFmpegExtractAudio",
                     "preferredcodec": "mp3"
                 }
             ],
             "outtmpl": "%(id)s.mp3",
             "quiet": True,
             "logtostderr": False,
         }
         try:
             with YoutubeDL(opts) as ytdl:
                 ytdl_data = ytdl.extract_info(url, download=True)
         except BaseException as e:
             return await u_s.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
         audio_original = f"{ytdl_data['id']}.mp3"
         raw_file_name = ''.join([random.choice(string.ascii_lowercase) for i in range(5)]) + ".raw"
         #raw_file_name = f"{vid_title}.raw"
    raw_file_name = await convert_to_raw(audio_original, raw_file_name)
    if not os.path.exists(raw_file_name):
        return await u_s.edit(f"`FFmpeg Failed To Convert Song To raw Format.` \n**Error :** `{raw_file_name}`")
    if os.path.exists(audio_original):
        os.remove(audio_original)
    if not group_call:
        group_call = GroupCall(client, play_on_repeat=False)
        GPC[(message.chat.id, client.me.id)] = group_call
        try:
            await group_call.start(message.chat.id)
        except BaseException as e:
            return await u_s.edit(f"**Error While Joining VC:** `{e}`")
        group_call.add_handler(playout_ended_handler, GroupCallAction.PLAYOUT_ENDED)
        group_call.input_filename = raw_file_name
        return await u_s.edit(f"Playing `{vid_title}` in `{message.chat.title}`!")
    elif not group_call.is_connected:
        try:
            await group_call.start(message.chat.id)
        except BaseException as e:
            return await u_s.edit(f"**Error While Joining VC:** `{e}`")
        group_call.add_handler(playout_ended_handler, GroupCallAction.PLAYOUT_ENDED)
        group_call.input_filename = raw_file_name
        return await u_s.edit(f"Playing `{vid_title}` in `{message.chat.title}`!")
    else:
        s_d = s_dict.get((message.chat.id, client.me.id))
        f_info = {"song_name": vid_title,
                  "raw": raw_file_name,
                  "singer": uploade_r,
                  "dur": dur,
                  "url": url
                 }
        if s_d:
            s_d.append(f_info)
        else:
            s_dict[(message.chat.id, client.me.id)] = [f_info]
        s_d = s_dict.get((message.chat.id, client.me.id))
        return await u_s.edit(f"Added `{vid_title}` To Position `#{len(s_d)+1}`!")
    
      
async def convert_to_raw(audio_original, raw_file_name):
    try:
         ffmpeg.input(audio_original).output(
              raw_file_name, format="s16le", acodec="pcm_s16le", ac=2, ar="48k", loglevel="error").overwrite_output().run()
    except BaseException as e:
         return str(e)
    return raw_file_name


RD_ = {}
FFMPEG_PROCESSES = {}


@friday_on_cmd(
    ["pradio"],
    is_official=False,
    cmd_help={"help": "Play Radio.", "example": "{ch}pradio (radio url)"},
)
async def radio_s(client, message):
    g_s_ = GPC.get((message.chat.id, client.me.id))
    if g_s_:
        if g_s_.is_connected:
            await g_s_.stop()
        del GPC[(message.chat.id, client.me.id)]
    s = await edit_or_reply(message, "`Please Wait.`") 
    input_filename = f"radio_{message.chat.id}.raw"
    radio_url = get_text(message)
    if not radio_url:
         return await s.edit("`Invalid Radio URL...`")
    group_call = RD_.get((message.chat.id, client.me.id))
    if not group_call:
        group_call = GroupCall(client, input_filename, path_to_log_file='')
        RD_[(message.chat.id, client.me.id)] = group_call
    process = FFMPEG_PROCESSES.get((message.chat.id, client.me.id))
    if process:
        process.send_signal(signal.SIGTERM)
    await group_call.start(message.chat.id)
    process = ffmpeg.input(radio_url).output(
        input_filename,
        format='s16le',
        acodec='pcm_s16le',
        ac=2,
        ar='48k',
        loglevel='error'
    ).overwrite_output().run_async()
    FFMPEG_PROCESSES[(message.chat.id, client.me.id)] = process
    await s.edit(f"**📻 Playing :** `{radio_url}`")

@friday_on_cmd(
    ["sradio"],
    is_official=False,
    cmd_help={"help": "Stop Radio.", "example": "{ch}stop_radio"},
)
async def stop_radio(client, message):
    msg = await edit_or_reply(message, "`Please Wait.`")
    group_call = RD_.get((message.chat.id, client.me.id))
    if group_call:
        if group_call.is_connected:
            await group_call.stop()
        else:
            return await msg.edit("`Is Vc is Connected?`")
    else:
        return await msg.edit("`Is Vc is Connected?`")
    process = FFMPEG_PROCESSES.get((message.chat.id, client.me.id))
    await msg.edit("`Radio Stopped : 📻`")
    if process:
        process.send_signal(signal.SIGTERM)

 
@friday_on_cmd(
    ["pause"],
    is_official=False,
    cmd_help={"help": "Pause Currently Playing Song.", "example": "{ch}pause"},
)
async def no_song_play(client, message):
    group_call = GPC.get((message.chat.id, client.me.id))
    if not group_call:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return
    if not group_call.is_connected:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return    
    await edit_or_reply(message, f"`⏸ Paused {str(group_call.input_filename).replace('.raw', '')}.`")
    group_call.pause_playout()
    
    
@friday_on_cmd(
    ["resume"],
    is_official=False,
    cmd_help={"help": "Resume Paused Song.", "example": "{ch}resume"},
)
async def wow_dont_stop_songs(client, message):
    group_call = GPC.get((message.chat.id, client.me.id))
    if not group_call:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return    
    if not group_call.is_connected:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return    
    group_call.resume_playout()
    await edit_or_reply(message, f"`▶️ Resumed.`")
        
        
@friday_on_cmd(
    ["stopvc"],
    is_official=False,
    cmd_help={"help": "Stop VoiceChat!", "example": "{ch}stopvc"},
)
async def kill_vc_(client, message):
    group_call = GPC.get((message.chat.id, client.me.id))
    if not group_call:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return
    if not group_call.is_connected:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return
    if os.path.exists(group_call.input_filename):
        os.remove(group_call.input_filename)
    group_call.stop_playout()
    await edit_or_reply(message, "`Stopped Playing Songs!`")
    del GPC[(message.chat.id, client.me.id)]


@friday_on_cmd(
    ["rvc"],
    is_official=False,
    cmd_help={"help": "Replay Song In VC!", "example": "{ch}rvc"},
)
async def replay(client, message):
    group_call = GPC.get((message.chat.id, client.me.id))
    if not group_call:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return
    if not group_call.is_connected:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return
    group_call.restart_playout()
    await edit_or_reply(message, f"`Re-Playing : {group_call.input_filename}`")


@friday_on_cmd(
    ["rjvc"],
    is_official=False,
    cmd_help={"help": "Rejoin Voice Chat!", "example": "{ch}rjvc"},
)
async def rejoinvcpls(client, message):
    group_call = GPC.get((message.chat.id, client.me.id))
    if not group_call:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return
    if not group_call.is_connected:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return
    await group_call.reconnect()
    await edit_or_reply(message, f"`Rejoined! - Vc`")


@friday_on_cmd(
    ["leavevc"],
    is_official=False,
    cmd_help={"help": "Leave Voice Call!", "example": "{ch}leavevc"},
)
async def leave_vc_test(client, message):
    group_call = GPC.get((message.chat.id, client.me.id))
    if not group_call:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return
    if not group_call.is_connected:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return
    if os.path.exists(group_call.input_filename):
        os.remove(group_call.input_filename)
    await group_call.stop()
    await edit_or_reply(message, f"`Left : {message.chat.title} - Vc`")
    del GPC[(message.chat.id, client.me.id)]


@friday_on_cmd(
    ["setvolvc"],
    is_official=False,
    cmd_help={
        "help": "Set Voice Call Volume!",
        "example": "{ch}setvolvc (Specifically Volume Between 2-100)",
    },
)
async def set_vol(client, message):
    group_call = GPC.get((message.chat.id, client.me.id))
    if not group_call:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return
    if not group_call.is_connected:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return
    volume = get_text(message)
    if not volume:
        await edit_or_reply(message, "Volume Should Be Integer!")
        return
    if not volume.isdigit():
        await edit_or_reply(message, "Volume Should Be Integer!")
        return
    if int(volume) < 2:
        await edit_or_reply(message, "Volume Should Be Above 2")
        return
    if int(volume) >= 100:
        await edit_or_reply(message, "Volume Should Be Below 100")
        return
    await group_call.set_my_volume(volume)
    await edit_or_reply(message, f"**Volume :** `{volume}`")
