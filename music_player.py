import os
import logging
import ffmpeg
from main_startup import Friday
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply
from pytgcalls import GroupCall

s = []
group_call = GroupCall(Friday, play_on_repeat=False)


@friday_on_cmd(
    ["playlist"],
    is_official=False,
    cmd_help={"help": "Get Current Chat Playlist!", "example": "{ch}playlist"},
)
async def pl(client, message):
    play = await edit_or_reply(message, "`Please Wait!`")
    song = f"**PlayList in {message.chat.title}** \n"
    sno = 0
    if not s:
        if group_call.is_connected:
            await play.edit(f"**Currently Playing :** `{group_call.input_filename}`")
        else:
            await play.edit("`Playlist is Empty Sar And Nothing is Playing Also :(!`")
            return
    if group_call.is_connected:
        song += f"**Currently Playing :** `{group_call.input_filename}` \n\n"
    for i in s:
        sno += 1
        song += f"**{sno})** `{i}` \n"
    await play.edit(song)


@group_call.on_playout_ended
async def playout_ended_handler(group_call, filename):
    global s
    if not s:
        await Friday.send_message(
            int(f"-100{group_call.full_chat.id}"),
            f"`Finished Playing, No More Playlist Left! :( Leaving VC!`",
        )
        await group_call.stop()
        return
    await Friday.send_message(
        int(f"-100{group_call.full_chat.id}"), f"**Now Playing :** `{s[0]}`."
    )
    holi = s[0]
    s.pop(0)
    logging.info("Now Playing " + str(holi))
    group_call.input_filename = holi


@friday_on_cmd(
    ["play", "playmusic"],
    is_official=False,
    cmd_help={"help": "Play The Song In VC!", "example": "{ch}play (reply to song)"},
)
async def test(client, message):
    u_s = await edit_or_reply(message, "`Processing..`")
    if not message.reply_to_message or not message.reply_to_message.audio:
        await u_s.edit("`Reply To Audio To Play It`")
        return
    await u_s.edit_text("`Please Wait, Let Me Download This File!`")
    audio = message.reply_to_message.audio
    audio_original = await message.reply_to_message.download()
    raw_file_name = (
        f"{audio.file_name}.raw" if not audio.title else f"{audio.title}.raw"
    )
    ffmpeg.input(audio_original).output(
        raw_file_name, format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(audio_original)
    if not group_call.is_connected:
        await u_s.edit(f"Playing `{audio.title}...` in {message.chat.title}!")
        try:
            await group_call.start(message.chat.id, False)
        except BaseException as e:
            await u_s.edit(f"**Error While Joining VC:** `{e}`")
            return
        group_call.input_filename = raw_file_name
    else:
        s.append(raw_file_name)
        await u_s.edit(f"Added To Position #{len(s)+1}!")


@friday_on_cmd(
    ["stopvc"],
    is_official=False,
    cmd_help={"help": "Stop VoiceChat!", "example": "{ch}stopvc"},
)
async def kill_vc_test(client, message):
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
