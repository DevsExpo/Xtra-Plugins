from database import db_x

lydia = db_x["LYDIA"]


def add_user(chat_id, user_id, string_id):
    stark = lydia.find_one({"chat_id": chat_id, "user_id": user_id, "string_id": string_id})
    if stark:
        return False
    else:
        lydia.insert_one({"chat_id": chat_id, "user_id": user_id, "string_id": string_id})
        return True


def remove_user(chat_id, user_id):
    stark = lydia.find_one({"chat_id": chat_id, "user_id": user_id})
    if not stark:
        return False
    else:
        lydia.delete_one({"chat_id": chat_id, "user_id": user_id, "string_id": string_id})
        return True

def get_all_users(chat_id):
    r = list(lydia.find({"chat_id": chat_id}))
    if r:
        return r
    else:
        return False


