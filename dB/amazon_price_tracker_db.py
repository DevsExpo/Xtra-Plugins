from database import db_x

amazon_url = db_x["amazontracker"]


async def add_amazon_tracker(amazon_link, price):
    await amazon_url.insert_one({"amazon_link": amazon_link, "price": price})


async def rmamazon_tracker(amazon_link):
    await amazon_url.delete_one({"amazon_link": amazon_link})


async def get_all_amazon_trackers():
    lol = [lakhac async for lakhac in amazon_url.find({})]
    return lol


async def is_amazon_tracker_in_db(amazon_link):
    k = await amazon_url.find_one({"amazon_link": amazon_link})
    if k:
        return True
    else:
        return False
