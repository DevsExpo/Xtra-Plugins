# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
import asyncio
import time
@friday_on_cmd(
    ["mask"],
    is_official=False,
    cmd_help={
        "help": "Mask The Images",
        "example": "{ch}mask (Reply To Image)",
    },
)
async def mask(client, message):
    pablo = await edit_or_reply(message, "`Processing...`")
    if not message.reply_to_message:
        await pablo.edit("Please Reply To A Image")
        return
    if (
        message.reply_to_message.sticker
        and message.reply_to_message.sticker.mime_type != "image/webp"
    ):
        return
    await message.reply_to_message.copy("hazmat_suit_bot")
    time.sleep(1.5)
    try:
       messi = (await client.get_history("hazmat_suit_bot", 1))[0]
    except:
       print(messi)
    await message.reply_photo(messi.photo.file_id)
    await pablo.delete()
