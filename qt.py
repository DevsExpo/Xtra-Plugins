# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["qbot", "qt"],
    cmd_help={
        "help": "Create A Quote Using Bot",
        "example": "{ch}qbot (input of no:of msgs to be fetched or just reply to a message)",
    },
)
async def nice_qbot(client, message):
    m = await edit_or_reply(message, "`Making A Quote.`")
    query = get_text(message)
    msg_ids = []
    if not query:
        if not message.reply_to_message:
            return await m.edit("`Reply To Message To Make A Quote.`")
        msg_ids.append(message.reply_to_message.message_id)   
    else:
        if not query.isdigit():
            return await m.edit("`Uh? Only Digits My Friend.`")
        if int(query) == 0:
            return await m.edit("`Uh?, You Are Zero.`")
        async for msg in client.iter_history(chat_id=message.chat.id, reverse=True, limit=int(query)):
            if message.message_id != msg.message_id:
                msg_ids.append(msg.message_id)
    if not msg_ids:
        return await m.edit("`Uh?, You Are Zero.`")
    await client.forward_messages("@QuotLyBot", message.chat.id, msg_ids) 
    await asyncio.sleep(7)
    histor_ = await check_history("@QuotLyBot", client)
    if not histor_:
        return await m.edit("`Invalid or No Response Recieved.`")
    if message.reply_to_message:
        await histor_.copy(message.chat.id, reply_to_message_id=message.reply_to_message.message_id)
    else:
        await histor_.copy(message.chat.id)
    await m.delete()
    
         
       
async def check_history(bot, client):
    its_history = (await client.get_history(bot, 1))[0]
    if its_history.from_user.id == client.me.id:
        return None
    if not its_history.sticker:
        return None
    return its_history