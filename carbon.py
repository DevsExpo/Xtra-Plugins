# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

#Credits to @WilliamButcherBot


from io import BytesIO
from aiohttp import ClientSession
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


aiosession = ClientSession()

async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "Friday_Carbon.png"
    return image


async def image_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "Friday_Carbon.jpg"
    return image


@friday_on_cmd(['carbon'],
    cmd_help={
    "help": "Carbonize Codes In A Cool Way.",
    "example": "{ch}karbon <text or replied message will be taken>",
    })
async def carb(client, message):
    ok = await edit_or_reply(message, "`Making Karbon...`")
    code = get_text(message)
    if not code:
        if not message.reply_to_message:
           return await ok.edit("`Nothing To Karbonize..`")
        if not message.reply_to_message.text:
           return await ok.edit("`Nothing To Karbonize...`")
    code = code or message.reply_to_message.text
    
    carbon = await make_carbon(code)
    cap = f"__Carbonized By {message.from_user.mention}__\n\n__**By @FridayUB**"
    await client.send_document(message.chat.id, carbon, caption=cap)
    carbon.close()
    await ok.delete()


@friday_on_cmd(['icarbon'],
    cmd_help={
    "help": "Carbonize Codes In A Cool Way In Image format.",
    "example": "{ch}ikarbon <text or replied message will be taken>",
    })
async def image_karb(client, message):
    ok = await edit_or_reply(message, "`Making Karbon...`")
    code = get_text(message)
    if not code:
        if not message.reply_to_message:
           return await ok.edit("`Nothing To Karbonize..`")
        if not message.reply_to_message.text:
           return await ok.edit("`Nothing To Karbonize...`")
    code = code or message.reply_to_message.text
    
    carbon = await image_carbon(code)
    cap = f"__Carbonized By {message.from_user.mention}__\n\n__**By @FridayUB**"
    await client.send_photo(message.chat.id, carbon, caption=cap)
    carbon.close()
    await ok.delete()
