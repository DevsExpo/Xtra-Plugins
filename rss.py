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
    try:
        rss_d = feedparser.parse(lenk)
        rss_d.entries[0].title
    except:
        await pablo.edit("ERROR: The link does not seem to be a RSS feed or is not supported")
        return
    lol = is_get_chat_rss(message.chat.id, lemk)
    if lol:
        await pablo.edit("This Link Already Added")
        return
    content = ""
    content += rss_d.entries[0].title
    content += f"\n\n{rss_d.entries[0].link}"
    try:
        content += f"\n{rss_d.entries[0].description}"
    except:
        pass
    await client.send_message(message.chat.id, content)
    add_rss(message.chat.id, lenk, rss_d.entries[0].link)
