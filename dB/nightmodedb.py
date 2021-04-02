from database import db_x

night_mode = db_x["NIGHT_MODE"]


async def add_night_chat(chat_id):
    await night_mode.insert_one({"chat_id": chat_id})


async def rm_night_chat(chat_id):
    await night_mode.delete_one({"chat_id": chat_id})


async def get_all_night_chats():
    lol = [ujwal async for ujwal in night_mode.find({})]
    return lol


async def is_night_chat_in_db(chat_id):
    k = await night_mode.find_one({"chat_id": chat_id})
    if k:
        return True
    else:
        return False
