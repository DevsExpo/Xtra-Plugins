from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_readable_time, delete_or_pass, progress, get_text, edit_or_send_as_file
import asyncio
import math
import time
from pyrogram import filters
from main_startup.config_var import Config


@friday_on_cmd(["spam", "ultraspam"], 
is_official=False,
cmd_help = {
               'help': 'Spam Message Multiple Times!',
               'example': '{ch}spam (number of times to spam) (reply to message)'
               },)
async def spam(client, message):
    pablo = await edit_or_reply(message, "Processing....")
    count = get_text(message)
    if not count:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    if not count.isdigit():
        await pablo.edit("`Give Digits Idiot!`")
        return
    if not message.reply_to_message:
        await pablo.edit("`Reply To Message, Idiot!`")
        return
    count = int(count)
    x = 0
    for x in range(count):
       await client.copy_message(from_chat_id=message.chat.id, chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
       x+=1
