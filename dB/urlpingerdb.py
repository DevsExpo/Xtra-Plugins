from database import db_x

server_pinger = db_x["S_PING"]


def add_ping_url(url):
    server_pinger.insert_one({"url": url})


def rm_ping_url(url):
    server_pinger.delete_one({"url": url})


def get_all_ping_urls():
    lol = list(server_pinger.find({}))
    return lol


def is_ping_url_in_db(url):
    k = server_pinger.find_one({"url": url})
    if k:
        return True
    else:
        return False
