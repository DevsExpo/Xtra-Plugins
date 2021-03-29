from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from database.nightmodedb import is_night_chat_in_db, get_all_night_chats, rm_night_chat, add_night_chat


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
        "help": "Activate Nightmode In Group",
        "example": "{ch}scgrp",
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




