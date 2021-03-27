from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
import feedparser
from xtraplugins.dB.rss_db import (
    add_rss,
    is_get_chat_rss,
    del_rss,
    get_chat_rss,
    get_last_rss,
    update_rss
)


@friday_on_cmd(
    ["add_rss"],
    is_official=False,
    cmd_help={
        "help": "Add RSS To The Chat",
        "example": "{ch}add_rss (rss link)",
    },
)
async def addrss(client, message):
    pablo = await edit_or_reply(message, "`Processing....`")
    lenk = get_text(message)
    if not lenk:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    
