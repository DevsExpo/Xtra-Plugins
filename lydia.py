# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.core.decorators import friday_on_cmd, listen
from pyrogram import filters
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from main_startup.config_var import Config
from functools import wraps
from xtraplugins.dB.lydia import (
    remove_chat,
    add_chat,
    get_all_chats,
    get_session,
    update_session
)

import asyncio, coffeehouse
import logging
from coffeehouse.lydia import LydiaAI

if Config.LYDIA_API_KEY:
    api_key = Config.LYDIA_API_KEY
    try:
        lydia = LydiaAI(api_key)
    except Exception as e:
        logging.error(f"Unable To Start Lydia Client \nTraceBack : {e}")
        lydia = None
else:
    lydia = None


def _check_lydia(func):
    @wraps(func)
    async def check_lydia(client, message):
        if not lydia:
            await edit_or_reply(message, "`Is Your Lydia Api Key Valid Or You Didn't Add It??`")
        elif lydia:
            await func(client, message)
    return check_lydia
    

@friday_on_cmd(
        ["addcf"],
        is_official=False,
        cmd_help={
            "help": "Activate Lydia In The Chat!",
            "example": "{ch}addcf"
        }
    )
@_check_lydia
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
@_check_lydia
async def remcf(client, message):
    pablo = await edit_or_reply(message, "`Processing...`")
    Escobar = remove_chat(int(message.chat.id))
    if not Escobar:
        await pablo.edit("Lydia Was Not Activated In This Chat")
        return
    await pablo.edit(f"Lydia AI Successfully Deactivated For Users In The Chat {message.chat.id}")
    
if lydia:
    @listen(~filters.edited & filters.incoming & filters.group & filters.text)
    async def live_lydia(client, message):
        if not message.text:
            message.continue_propagation()
        if not get_session(int(message.chat.id)):
            message.continue_propagation()
        await client.send_chat_action(message.chat.id, "typing")
        session = get_session(int(message.chat.id))
        try:
            session_id = session.get("session_id")
            text_rep = lydia.think_thought(session_id, message.text)
        except:
             session = lydia.create_session()
             session_id = session.id
             text_rep = lydia.think_thought(session_id, message.text)
             update_session(message.chat.id, session_id)
        await message.reply(text_rep)
        await client.send_chat_action(message.chat.id, "cancel")
        message.continue_propagation()
