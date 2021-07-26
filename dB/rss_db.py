from database import db_x

rss = db_x["RSS"]


async def add_rss(chat_id, rss_link, latest_rss):
    await rss.insert_one({"chat_id": chat_id, "rss_link": rss_link, "latest_rss": latest_rss})
         

async def del_rss(chat_id, rss_link):
    await rss.delete_one({"chat_id": chat_id, "rss_link": rss_link})

async def get_chat_rss(chat_id):
    return [m async for m in rss.find({"chat_id": chat_id})]

async def update_rss(chat_id, rss_link, latest_rss):
    await rss.update_one({"chat_id": chat_id, "rss_link": rss_link}, {"$set": {"latest_rss": latest_rss}})



async def is_get_chat_rss(chat_id, rss_link):
    lol = await rss.find_one({"chat_id": chat_id, "rss_link": rss_link})
    return bool(lol)

async def basic_check(chat_id):
    lol = await rss.find_one({"chat_id": chat_id})
    return bool(lol)


async def overall_check():
    lol = await rss.find_one()
    return bool(lol)


async def get_all():
    return [rrrs async for rrrs in rss.find()]

async def delete_all():
    lol = await rss.delete_many({})
    


