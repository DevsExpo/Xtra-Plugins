from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from xtraplugins.dB.nightmodedb import is_night_chat_in_db, get_all_night_chats, rm_night_chat, add_night_chat
from pyrogram.types import ChatPermissions
from main_startup.helper_func.logger_s import LogIt
from apscheduler.schedulers.asyncio import AsyncIOScheduler






@friday_on_cmd(
    ["scgrp"],
    is_official=False,
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "Activate Nightmode In Group",
        "example": "{ch}scgrp",
    },
)
async def scgrp(client, message):
    pablo = await edit_or_reply(message, "`Processing...`")
    lol = is_night_chat_in_db(message.chat.id)
    if lol:
        await pablo.edit("This Chat is Has Already Enabled Night Mode.")
        return
    add_night_chat(message.chat.id)
    await pablo.edit(f"**Added Chat {message.chat.title} With Id {message.chat.id} To Database. This Group Will Be Closed On 12Am(IST) And Will Opened On 06Am(IST)**")


@friday_on_cmd(
    ["rsgrp"],
    is_official=False,
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "Deactivate Nightmode In Group",
        "example": "{ch}rsgrp",
    },
)
async def scgrp(client, message):
    pablo = await edit_or_reply(message, "`Searching For Anime.....`")
    lol = is_night_chat_in_db(message.chat.id)
    if not lol:
        await message.edit("This Chat is Has Not Enabled Night Mode.")
        return
    rm_night_chat(message.chat.id)
    await pablo.edit(f"**Removed Chat {message.chat.title} With Id {message.chat.id} From Database. This Group Will Be No Longer Closed On 12Am(IST) And Will Opened On 06Am(IST)**")


async def job_close():
    lol = get_all_night_chats()
    if len(lol) == 0:
        return
    for warner in ws_chats:
        try:
            await client.send_message(
              int(warner.get("chat_id")), "`12:00 Am, Group Is Closing Till 6 Am. Night Mode Started !` \n**Powered By @FRidayOT**"
            )
            await client.set_chat_permissions(warner.get("chat_id"), ChatPermissions())
            async for member in client.iter_chat_members(warner.get("chat_id")):
             if member.user.is_deleted:
                try:
                    await client.kick_chat_member(warner.get("chat_id"), member.user.id)
                except:
                    pass
        except Exception as e:
            log = LogIt(message)
            ido = warner.get("chat_id")
            await log.log_msg(client, f"[NIGHT MODE]\n\nFailed To Close The Group {ido}.\nError : {e}")


scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_close, trigger="cron", hour=16, minute=18)
scheduler.start()








