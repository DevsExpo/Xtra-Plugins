# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import glob
import os
import random
import shutil
from PIL import Image
import logging
import pathlib
from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


async def create_s_collage(file_path, filename, width, stark_h):
    """Create Image Collage"""
    img_stark = [filepath for filepath in pathlib.Path(file_path).glob("**/*")]
    margin_size = 2
    while True:
        img_stark_list = list(img_stark)
        ujwal_liness = []
        img_stark_line = []
        x = 0
        while img_stark_list:
            img_path = img_stark_list.pop(0)
            img = Image.open(img_path)
            img.thumbnail((width, stark_h))
            if x > width:
                ujwal_liness.append((float(x) / width, img_stark_line))
                img_stark_line = []
                x = 0
            x += img.size[0] + margin_size
            img_stark_line.append(img_path)
        ujwal_liness.append((float(x) / width, img_stark_line))
        if len(ujwal_liness) <= 1:
            break
        if any(map(lambda c: len(c[1]) <= 1, ujwal_liness)):
            stark_h -= 10
        else:
            break
    out_lol_h = sum(
        int(stark_h / meisnub) + margin_size
        for meisnub, sedlife in ujwal_liness
        if sedlife
    )

    if not out_lol_h:
        return None
    final_image = Image.new('RGB', (width, int(out_lol_h)), (35, 35, 35))
    y = 0
    for meisnub, sedlife in ujwal_liness:
        if sedlife:
            x = 0
            for img_path in sedlife:
                img = Image.open(img_path)
                k = (stark_h / meisnub) / img.size[1]
                if k > 1:
                    img = img.resize((int(img.size[0] * k), int(img.size[1] * k)), Image.ANTIALIAS)
                else:
                    img.thumbnail((int(width / meisnub), int(stark_h / meisnub)), Image.ANTIALIAS)
                if final_image:
                    final_image.paste(img, (int(x), int(y)))
                x += img.size[0] + margin_size
            y += int(stark_h / meisnub) + margin_size
    final_image.save(filename)
    shutil.rmtree(file_path)
    return filename



@friday_on_cmd(
    ["collage"],
    cmd_help={
        "help": "Create Collage From All Images in A Chat.",
        "example": "{ch}collage (input or current chat will be taken)",
    },
)
async def wow_collage(client, message):
    owo = await edit_or_reply(message, "`Making Collage Please Wait.`")
    hmm = get_text(message) or " "
    width = 800
    stark_h = 250
    limit = 15
    img_ = 0
    final_input = hmm.split(" ")
    chat = message.chat.id
    if hmm == " ":
        limit = 15
    elif len(final_input) == 1:
        limit = hmm
    elif len(final_input) == 2:
        limit = final_input[0]
        width = int(final_input[1])
    elif len(final_input) >= 3:
        limit = final_input[0]
        width = int(final_input[1])
        stark_h = int(final_input[2])
    try:
        limit_ = int(limit)
    except ValueError:
        return await owo.edit("`Limit Should Be In Digits.`")
    file_path = "./to_collage/"
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
    os.mkdir(file_path)
    async for msg in client.iter_history(chat, limit=limit_):
        if msg.photo:
            img_ += 1
            try:
                await msg.download(file_path)
            except Exception as e:
                logging.error(e)
    if img_ == 0:
        await owo.edit("`No Images Found.`")
        shutil.rmtree(file_path)
        return
    elif img_ == 1:
        shutil.rmtree(file_path) 
        await owo.edit("`How Am I Supposed To Make Collage With One Image?`")
        return
    await owo.edit("`Creating Collage....`")
    imgpath = await create_s_collage(file_path=file_path, filename="Collage_by_FridayUB.jpg", width=width, stark_h=stark_h)
    if not imgpath:
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
        await owo.edit("`[Collage] - Failed To Make A Proper Collage`")
        return
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            imgpath,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_photo(message.chat.id, imgpath)
    if os.path.exists(imgpath):
        os.remove(imgpath)
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
    await owo.delete()
