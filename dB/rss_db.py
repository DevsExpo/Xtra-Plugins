from database import db_x

rss = db_x["RSS"]


def add_rss(chat_id, rss_link, latest_rss):
    rss.insert_one({"chat_id": chat_id, "rss_link": rss_link, "latest_rss": latest_rss})
         

def del_rss(chat_id, rss_link):
    rss.delete_one({"chat_id": chat_id, "rss_link": rss_link})

def get_chat_rss(chat_id):
    lol = list(amazon_url.find({"chat_id": chat_id}))
    return lol


def get_last_rss(chat_id, rss_link):
    lol = amazon_url.find({"chat_id": chat_id, "rss_link": rss_link})
    return lol









