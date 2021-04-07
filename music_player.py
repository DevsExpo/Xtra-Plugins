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
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from pytgcalls import GroupCall

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
    ["skipvc"],
    is_official=False,
    cmd_help={"help": "Skip Song in Playlist.", "example": "{ch}skipvc (key_len)"}
)
async def ski_p(client, message):
    m_ = await edit_or_reply(message, "`Please Wait!`")
    no_t_s = get_text(message)
    if no_t_s:
        return await m_.edit("`Give Me Valid List Key Len.`")
    group_call.client = client
    if not group_call.is_connected:
        await m_.edit("`Is Group Call Even Connected?`")
        return        
    if not s:
        return m_.edit("`There is No Playlist.`")
    if len(s) == 1:
        return m_.edit("`There is No Playlist.`")
    if not no_t_s.isdigits():
        return await m_.edit("`Give Me Valid List Key Len.`")
    if len(s) < no_t_s:
        return await m_.edit("`This Playlist Key Doesn't Exits`")
    if no_t_s == 0:
        return await m_.edit("`This Playlist Key Doesn't Exits`")
    try:
        s.pop(no_t_s)
    except:
        return await m_.edit("`This Playlist Key Doesn't Exits`")
                            
@friday_on_cmd(
    ["play", "playmusic"],
    is_official=False,
    cmd_help={"help": "Play The Song In VC!", "example": "{ch}play (reply to song)"},
)
async def play_m(client, message):
    group_call.client = client
    u_s = await edit_or_reply(message, "`Processing..`")
    if not message.reply_to_message or not message.reply_to_message.audio:
        await u_s.edit("`Reply To Audio To Play It`")
        return
    await u_s.edit_text("`Please Wait, Let Me Download This File!`")
    audio = message.reply_to_message.audio
    audio_original = await message.reply_to_message.download()
    sing_r = message.reply_to_message.audio.performer or "Unknown Artist."
    dura_ = message.reply_to_message.audio.duration
    fd = time.strftime("%Hh:%Mm:%Ss", time.gmtime(dura_))
    raw_file_name = (
        f"{audio.file_name}.raw" if not audio.title else f"{audio.title}.raw"
    )
    ffmpeg.input(audio_original).output(
        raw_file_name, format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(audio_original)
    if not group_call.is_connected:
        await u_s.edit(f"Playing [{audio.title}](message.reply_to_message.link) in {message.chat.title}!")
        try:
            await group_call.start(message.chat.id)
        except BaseException as e:
            await u_s.edit(f"**Error While Joining VC:** `{e}`")
            return
        group_call.input_filename = raw_file_name
    else:
        s.append(raw_file_name)
        f_info = {"song name": audio.title,
                  "singer": sing_r,
                  "dur": fd
                 }
        s_dict[raw_file_name] = f_info
        await u_s.edit(f"Added [{audio.title}](message.reply_to_message.link) To Position #{len(s)+1}!")


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
    group_call.pause_playout()
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
    await edit_or_reply(message, "`Re-Playing!`")


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
