from database import db_x

amazon_url = db_x["amazontracker"]


def add_amazon_tracker(amazon_link, price):
    amazon_url.insert_one({"amazon_link": amazon_link, "price": price})


def rmamazon_tracker(amazon_link):
    amazon_url.delete_one({"amazon_link": amazon_link})


def get_all_amazon_trackers():
    lol = list(amazon_url.find({}))
    return lol


def is_amazon_tracker_in_db(amazon_link):
    k = amazon_url.find_one({"amazon_link": amazon_link})
    if k:
        return True
    else:
        return False
