from database import db_x

rss = db_x["RSS"]


def add_rss(chat_id, rss_link, latest_rss):
    rss.insert_one({"chat_id": chat_id, "rss_link": rss_link, "latest_rss": latest_rss})
         

def del_rss(chat_id, rss_link):
    rss.delete_one({"chat_id": chat_id, "rss_link": rss_link})

def get_chat_rss(chat_id):
    lol = list(rss.find({"chat_id": chat_id}))
    return lol

def update_rss(chat_id, rss_link, latest_rss):
    rss.update_one({"chat_id": chat_id, "rss_link": rss_link, {"$set": {"latest_rss": latest_rss}})

def get_last_rss(chat_id, rss_link):
    lol = rss.find({"chat_id": chat_id, "rss_link": rss_link})
    return lol

def is_get_chat_rss(chat_id, rss_link):
    lol = rss.find_one({"chat_id": chat_id, "rss_link": rss_link})
    if lol:
        return True
    else:
        return False







