# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.core.decorators import friday_on_cmd, Config, listen
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from main_startup import bot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import pytz
from pyrogram import filters


TAG_LOGGER = Config.TAG_LOGGER

if TAG_LOGGER:
    @listen(filters.mentioned & filters.incoming & ~filters.edited)
    async def mentioned_alert(client, message):
        if not message:
            message.continue_propagation()
            return
        if not message.from_user:
            message.continue_propagation()
            return 
        chat_name = message.chat.title
        chat_id = message.chat.id
        tagged_msg_link = message.link
        user_ = f"@{message.from_user.username}" or message.from_user.mention
        TZ = pytz.timezone(Config.TZ)
        datetime_tz = datetime.now(TZ)
        time_ =  datetime_tz.strftime("`%Y/%m/%d - %H:%M:%S`")
        final_tagged_msg = f"**🔔 You Have Been** [Tagged]({tagged_msg_link}) **in** {chat_name} **By** {user_} **At** {time_}"
        button_s = InlineKeyboardMarkup([[InlineKeyboardButton("🔔 View Message 🔔", url=tagged_msg_link)]])
        if Config.BOT_TOKEN:
            try:
                await bot.send_message(Config.LOG_GRP, final_tagged_msg, reply_markup=button_s)
            except Exception:
                await client.send_message(Config.LOG_GRP, final_tagged_msg)
        else:
            await client.send_message(Config.LOG_GRP, final_tagged_msg)
        message.continue_propagation()