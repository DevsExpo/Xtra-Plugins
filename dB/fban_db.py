from database import db_x

fed = db_x["FED"]


async def add_fed(feds):
    await fed.insert_one({"fed": feds})


async def rmfed(feds):
    await fed.delete_one({"fed": feds})


async def rm_all_fed():
    await fed.delete_many({})


async def get_all_feds():
    lol = [wow async for wow in fed.find()]
    return lol


async def is_fed_in_db(feds):
    k = await fed.find_one({"fed": feds})
    if k:
        return True
    else:
        return False
