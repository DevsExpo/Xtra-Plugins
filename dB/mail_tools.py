from database import db_x

mail = db_x["MAIL"]


async def add_mail_update_mail(mail_id, last_msg_id=""):
    midhun = await mail.find_one({"_id": "MAIL_DETAILS"})
    if midhun:
        await mail.update_one({"_id": "MAIL_DETAILS"}, {"$set": {"last_msg_id": last_msg_id, "mail_id": mail_id}})
    else:
        await mail.insert_one({"_id": "MAIL_DETAILS", "mail_id": mail_id, "last_msg_id": last_msg_id})

async def add_msg_update_msg(last_msg_id):
    midhun = await mail.find_one({"_id": "MAIL_DETAILS"})
    if midhun:
       await mail.update_one({"_id": "MAIL_DETAILS"}, {"$set": {"last_msg_id": last_msg_id}})
    else:
       return False


async def get_msg_id(mail_id):
    midhun = await mail.find_one({"_id": "MAIL_DETAILS"})
    if midhun:
        return midhun["last_msg_id"]
    else:
        return False


async def get_mail_id():
    midhun = await mail.find_one({"_id": "MAIL_DETAILS"})
    if midhun:
        return midhun["mail_id"]
    else:
        return False

async def delete_mail_id():
    midhun = await mail.find_one({"_id": "MAIL_DETAILS"})
    if midhun:
        await mail.delete_one({"_id": "MAIL_DETAILS"})
        return True
    else:
        return False
