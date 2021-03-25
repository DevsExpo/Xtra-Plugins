from database import db_x

night_mode = db_x["NIGHT_MODE"]


def add_night_chat(chat_id):
    night_mode.insert_one({"chat_id": chat_id})


def rm_night_chat(chat_id):
    night_mode.delete_one({"chat_id": chat_id})


def get_all_night_chats():
    lol = list(night_mode.find({}))
    return lol


def is_night_chat_in_db(chat_id):
    k = night_mode.find_one({"chat_id": chat_id})
    if k:
        return True
    else:
        return False
