# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import os

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply
from main_startup.helper_func.plugin_helpers import convert_to_image
from PIL import Image


@friday_on_cmd(
    ["boycott"],
    is_official=False,
    cmd_help={
        "help": "Creates Boycott Image!",
        "example": "{ch}boycott (reply to image)",
    },
)
async def boycott_kangs(client, message):
    tgi = await edit_or_reply(message, "`Applying BoyCott Magic!`")
    if not message.reply_to_message:
        await tgi.edit("`Please, Reply To Media To Add Boycott Magic!`")
        return
    img = await convert_to_image(message, client)
    if not img:
        await tgi.edit("`Reply to a valid media first.`")
        return
    if not os.path.exists(img):
        await tgi.edit("`Invalid Media!`")
        return
    background = Image.open(img).convert("RGBA")
    foreground = Image.open("./xtraplugins/helper_files/x-cross.png").convert("RGBA")
    x, y = foreground.size
    foreground = foreground.resize(background.size)
    background.paste(foreground, (0, 0), foreground)
    file_name = "bcig.webp"
    background.save(file_name, "WebP")
    if message.reply_to_message:
        await client.send_sticker(
            message.chat.id,
            sticker=file_name,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_sticker(message.chat.id, sticker=file_name)
    await tgi.delete()
    for files in (file_name, img):
        if files and os.path.exists(files):
            os.remove(files)
