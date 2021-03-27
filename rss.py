from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
import feedparser
from xtraplugins.dB.rss_db import (
    add_rss,
    is_get_chat_rss,
    del_rss,
    get_chat_rss,
    get_last_rss,
    update_rss,
    basic_check
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
    lol = is_get_chat_rss(message.chat.id, lenk)
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
    await pablo.edit("Successfully Added Link To RSS Watch")

@friday_on_cmd(
    ["test_rss"],
    is_official=False,
    cmd_help={
        "help": "Test RSS Of The Chat",
        "example": "{ch}test_rss",
    },
)
async def testrss(client, message):
    pablo = await edit_or_reply(message, "`Processing....`")
    damn = basic_check(message.chat.id)
    if not damn:
        
        URL = "https://www.reddit.com/r/funny/new/.rss"
        rss_d = feedparser.parse(url)
        Content = (rss_d.entries[0]['title'] + "\n\n" + rss_d.entries[0]['link'])
        await client.send_message(message.chat.id, Content)
        await pablo.edit("This Chat Has No RSS So Sent Reddit RSS")
    else:
        all = get_chat_rss(message.chat.id)
        
        for x in all:
            link = x.get("rss_link")
            rss_d = feedparser.parse(lenk)
            rss_d.entries[0].title
            content = ""
            content += rss_d.entries[0].title
            content += f"\n\nLink : {rss_d.entries[0].link}"
            try:
                content += f"\n{rss_d.entries[0].description}"
            except:
                pass
            await client.send_message(message.chat.id, content)





