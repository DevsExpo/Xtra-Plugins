from database import db_x

lydia = db_x["LYDIA"]


async def add_chat(chat_id, session_id):
    stark = await lydia.find_one({"chat_id": chat_id})
    if stark:
        return False
    await lydia.insert_one({"chat_id": chat_id, "session_id": session_id})
    return True


async def remove_chat(chat_id):
    stark = await lydia.find_one({"chat_id": chat_id})
    if not stark:
        return False
    await lydia.delete_one({"chat_id": chat_id})
    return True

async def get_all_chats():
    r = [o async for o in lydia.find()]
    if r:
        return r
    else:
        return False


async def get_session(chat_id):
    stark = await lydia.find_one({"chat_id": chat_id})
    if not stark:
        return False
    else:
        return stark

async def update_session(chat_id, session_id):
    await lydia.update_one({"chat_id": chat_id}, {"$set": {"session_id": session_id}})


