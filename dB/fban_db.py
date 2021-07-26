from database import db_x

fed_s = db_x["FEDS"]

async def add_fed(feds):
    await fed_s.insert_one({"fed_s": feds})

async def rmfed(feds):
    await fed_s.delete_one({"fed_s": feds})

async def rm_all_fed():
    await fed_s.delete_many({})

async def get_all_feds():
    return [n async for n in fed_s.find({})]

async def is_fed_in_db(feds):
    k = await fed_s.find_one({"fed_s": feds})
    return bool(k)
