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
import calender
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from pytgcalls import GroupCall
import signal
import asyncio
import os
import time
import requests
import datetime
from youtube_dl import YoutubeDL
from youtubesearchpython import SearchVideos

s = []
s_dict = {}
group_call = GroupCall(None, play_on_repeat=False)


@friday_on_cmd(
    ["playlist"],
    is_official=False,
    cmd_help={"help": "Get Current Chat Playlist!", "example": "{ch}playlist"},
)
async def pl(client, message):
    group_call.client = client
    play = await edit_or_reply(message, "`Please Wait!`")
    song = f"**PlayList in {message.chat.title}** \n"
    sno = 0
    if not s:
        if group_call.is_connected:
            await play.edit(f"**Currently Playing :** `{str(group_call.input_filename).replace('.raw', '')}`")
        else:
            await play.edit("`Playlist is Empty Sar And Nothing is Playing Also :(!`")
            return
    if group_call.is_connected:
        song += f"**Currently Playing :** `{str(group_call.input_filename).replace('.raw', '')}` \n\n"
    for i in s:
        sno += 1
        song += f"**{sno} ▶** `{i.replace('.raw', '')} | {s_dict[i]['singer']} | {s_dict[i]['dur']}` \n\n" 
    await play.edit(song)

@group_call.on_playout_ended
async def playout_ended_handler(group_call, filename):
    global s
    client_ = group_call.client
    if os.path.exists(group_call.input_filename):
        os.remove(group_call.input_filename)
    if not s:
        await client_.send_message(
            int(f"-100{group_call.full_chat.id}"),
            f"`Finished Playing. Nothing Left Play! Left VC.`",
        )
        await group_call.stop()
        return
    await client_.send_message(
        int(f"-100{group_call.full_chat.id}"), f"**Now Playing :** `{str(s[0]).replace('.raw', '')} | {s_dict[s[0]]['singer']} | {s_dict[s[0]]['dur']}` \n\n"
    )
    holi = s[0]
    s.pop(0)
    logging.info("Now Playing " + str(holi).replace(".raw", ""))
    group_call.input_filename = holi

@friday_on_cmd(
    ["skip_vc"],
    is_official=False,
    cmd_help={"help": "Skip Song in Playlist.", "example": "{ch}skip_vc (key_len)"}
)
async def ski_p(client, message):
    group_call.client = client
    if not group_call.is_connected:
        await m_.edit("`Is Group Call Even Connected?`")
        return 
    m_ = await edit_or_reply(message, "`Please Wait!`")
    no_t_s = get_text(message)
    if not no_t_s:
        return await m_.edit("`Give Me Valid List Key Len.`")
    if no_t_s == "current":
        if not s:
            return await m_.edit("`No Song in List. So Stopping Song is A Smarter Way.`")
        next_s = s[0]
        s.pop(0)
        name = str(next_s).replace(".raw", "")
        prev = group_call.input_filename
        group_call.input_filename = next_s
        return await m_.edit(f"`Skipped {prev}. Now Playing {name}!`")       
    else:
        if not s:
            return await m_.edit("`There is No Playlist.`")
        if not no_t_s.isdigit():
            return await m_.edit("`Input Should Be In Digits.`")
        no_t_s = int(no_t_s)
        if int(no_t_s) == 0:
            return await m_.edit("`0? What?`")
        no_t_s = int(no_t_s - 1)
        try:
            s_ = s[no_t_s]
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
    global s
    global s_dict
    group_call.client = client
    u_s = await edit_or_reply(message, "`Processing..`")
    if message.reply_to_message:
         if message.reply_to_message.audio:
             await u_s.edit_text("`Please Wait, Let Me Download This File!`")
             audio = message.reply_to_message.audio
             audio_original = await message.reply_to_message.download()
             vid_title = audio.title or audio.file_name
             uploade_r = message.reply_to_message.audio.performer or "Unknown Artist."
             dura_ = message.reply_to_message.audio.duration
             dur = datetime.timedelta(seconds=dura_)
             raw_file_name = f"{audio.file_name}.raw" if audio.file_name else f"{audio.title}.raw"
         else:
             return await u_s.edit("`Reply To A File To PLay It.`")
    else:
         input_str = get_text(message)
         if not input_str:
             return await u_s.edit("`Give Me A Song Name. Like Why we lose or Alone.`")
         search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
         rt = search.result()
         try:
             result_s = rt["search_result"]
         except:
             return await u_s.edit(f"`Song Not Found With Name {input_str}, Please Try Giving Some Other Name.`")
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
                     "preferredcodec": "mp3",
                     "preferredquality": "720",
                 }
             ],
             "outtmpl": "%(id)s.mp3",
             "quiet": True,
             "logtostderr": False,
         }
         try:
             with YoutubeDL(opts) as ytdl:
                 ytdl_data = ytdl.extract_info(url, download=True)
         except Exception as e:
             await u_s.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
             return
         audio_original = f"{ytdl_data['id']}.mp3"
         raw_file_name = f"{vid_title}.raw"
    raw_file_name = await convert_to_raw(audio_original, raw_file_name)
    if not raw_file_name:
         return await u_s.edit("`FFmpeg Failed To Convert Song To raw Format. Please Give Valid File.`")
    os.remove(audio_original)
    if not group_call.is_connected:
        try:
            await group_call.start(message.chat.id)
        except BaseException as e:
            return await u_s.edit(f"**Error While Joining VC:** `{e}`")
        group_call.input_filename = raw_file_name
        return await u_s.edit(f"Playing `{vid_title}` in `{message.chat.title}`!")
    else:
        s.append(raw_file_name)
        f_info = {"song name": vid_title,
                  "singer": uploade_r,
                  "dur": dur
                 }
        s_dict[raw_file_name] = f_info
        return await u_s.edit(f"Added `{vid_title}` To Position `#{len(s)+1}`!")
    

      
async def convert_to_raw(audio_original, raw_file_name):
    try:
         ffmpeg.input(audio_original).output(
              raw_file_name, format="s16le", acodec="pcm_s16le", ac=2, ar="48k").overwrite_output().run()
    except:
         return None
    return raw_file_name


RD_ = {}
FFMPEG_PROCESSES = {}


@friday_on_cmd(
    ["radio_vc"],
    is_official=False,
    cmd_help={"help": "Play Radio.", "example": "{ch}radio_vc (radio url)"},
)
async def radio_s(client, message):
    s = await edit_or_reply(message, "`Please Wait.`") 
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    input_filename = f"{message.chat.id}_{ts}.raw"
    radio_url = get_text(message)
    if not radio_url:
         return await s.edit("`Invalid Radio URL...`")
    group_call = RD_.get((message.chat.id, client))
    if not group_call:
        group_call = GroupCall(client, input_filename, path_to_log_file='')
        RD_[(message.chat.id, client)] = group_call
    process = FFMPEG_PROCESSES.get((message.chat.id, client))
    if process:
        process.send_signal(signal.SIGTERM)
    await group_call.start(message.chat.id)
    process = ffmpeg.input(radio_url).output(
        input_filename,
        format='s16le',
        acodec='pcm_s16le',
        ac=2,
        ar='48k'
    ).overwrite_output().run_async()
    FFMPEG_PROCESSES[(message.chat.id, client)] = process
    await s.edit(f"**📻 Playing :** `{radio_url}`")

@friday_on_cmd(
    ["stop_radio"],
    is_official=False,
    cmd_help={"help": "Stop Radio.", "example": "{ch}stop_radio"},
)
async def stop_radio(client, message: Message):
    msg = await edit_or_reply(message, "`Please Wait.`")
    group_call = GROUP_CALLS.get((message.chat.id, client))
    if group_call:
        if group_call.is_connected:
            await group_call.stop()
        else:
            return await msg.edit("`Is Vc is Connected?`")
    else:
        return await msg.edit("`Is Vc is Connected?`")
    process = FFMPEG_PROCESSES.get((message.chat.id, client))
    if process:
        process.send_signal(signal.SIGTERM)
    await msg.edit("`Radio Stopped : 📻`")

 
@friday_on_cmd(
    ["pause"],
    is_official=False,
    cmd_help={"help": "Pause Currently Playing Song.", "example": "{ch}pause"},
)
async def no_song_play(client, message):
    group_call.client = client
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
    group_call.client = client
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
    group_call.client = client
    if not group_call.is_connected:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return
    if os.path.exists(group_call.input_filename):
        os.remove(group_call.input_filename)
    group_call.stop_playout()
    await edit_or_reply(message, "`Stopped Playing Songs!`")


@friday_on_cmd(
    ["rvc"],
    is_official=False,
    cmd_help={"help": "Replay Song In VC!", "example": "{ch}rvc"},
)
async def replay(client, message):
    group_call.client = client
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
    group_call.client = client
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
    group_call.client = client
    if not group_call.is_connected:
        await edit_or_reply(message, "`Is Group Call Even Connected?`")
        return
    if os.path.exists(group_call.input_filename):
        os.remove(group_call.input_filename)
    await group_call.stop()
    await edit_or_reply(message, f"`Left : {message.chat.title} - Vc`")


@friday_on_cmd(
    ["setvolvc"],
    is_official=False,
    cmd_help={
        "help": "Set Voice Call Volume!",
        "example": "{ch}setvolvc (Specifically Volume Between 2-100)",
    },
)
async def set_vol(client, message):
    group_call.client = client
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
