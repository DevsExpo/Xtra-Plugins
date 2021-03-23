from database import db_x

lydia = db_x["LYDIA"]


def add_user(chat_id, user_id, string_id):
    stark = fed.find_one({"chat_id": chat_id, "user_id": user_id, "string_id": string_id})
    if stark:
        return False
    else:
        fed.insert_one({"chat_id": chat_id, "user_id": user_id, "string_id": string_id})
        return True


def remove_user(chat_id, user_id):
    stark = fed.find_one({"chat_id": chat_id, "user_id": user_id})
    if not stark:
        return False
    else:
        fed.delete_one({"chat_id": chat_id, "user_id": user_id, "string_id": string_id})
        return True




