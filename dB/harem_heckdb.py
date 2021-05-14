# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from database import db_x

harem_heck = db_x["HAREM_HECK"]


async def add_chat(chat_id):
    await harem_heck.insert_one({"chat_id": chat_id})


async def rm_chat(chat_id):
    await harem_heck.delete_one({"chat_id": chat_id})


async def get_all_harem_heck_chats():
    lol = [kek async for kek in harem_heck.find({})]
    return lol


async def is_chat_in_db(chat_id):
    k = await harem_heck.find_one({"chat_id": chat_id})
    if k:
        return True
    else:
        return False