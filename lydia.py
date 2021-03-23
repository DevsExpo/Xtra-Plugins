from main_startup.core.decorators import friday_on_cmd, listen
from pyrogram import filters
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from main_startup.config_var import Config
from xtraplugins.dB.lydia import (
    remove_chat,
    add_chat,
    get_all_chats,
    get_session
)

import asyncio, coffeehouse

from coffeehouse.lydia import LydiaAI

if Config.LYDIA_API_KEY:
    api_key = Config.LYDIA_API_KEY
    lydia = LydiaAI(api_key)

@friday_on_cmd(
        ["addcf"],
        is_official=False,
        cmd_help={
            "help": "Activate Lydia In The Chat!",
            "example": "{ch}addcf"
        }
    )
async def addcf(client, message):
    pablo = await edit_or_reply(message, "`Processing...`")
    session = lydia.create_session()
    session_id = session.id
    lol = add_chat(int(message.chat.id), session_id)
    if not lol:
        await pablo.edit("Lydia Already Activated In This Chat")
        return
    await pablo.edit(f"Lydia AI Successfully Added For Users In The Chat {message.chat.id}")

    
@friday_on_cmd(
        ["remcf"],
        is_official=False,
        cmd_help={
            "help": "Deactivate Lydia In The Chat!",
            "example": "{ch}remcf"
        }
    )
async def remcf(client, message):
    pablo = await edit_or_reply(message, "`Processing...`")
    Escobar = remove_chat(int(message.chat.id))
    if not Escobar:
        await pablo.edit("Lydia Was Not Activated In This Chat")
        return
    await pablo.edit(f"Lydia AI Successfully Deactivated For Users In The Chat {message.chat.id}")

@listen(~filters.edited & filters.incoming & filters.group & filters.text)
async def live_lydia(client, message):
    if not message.text:
        message.continue_propagation()
    if not get_session(int(message.chat.id)):
        print("#1")
        message.continue_propagation()
    print("#2")
    session = get_session(int(message.chat.id))
    print("#3")
    session_id = session.get("session_id")
    text_rep = session.think_thought(session_id, message.text)
    print(text_rep)
    print("#4")
    await client.send_chat_action(message.chat.id, "typing")
    await message.reply(text_rep)
    await client.send_chat_action(message.chat.id, "cancel")
    print("Done!")
    message.continue_propagation()
