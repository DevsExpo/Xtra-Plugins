from database import db_x

mail = db_x["MAIL"]


def add_mail_update_mail(mail_id, last_msg_id=""):
    midhun = mail.find_one({"_id": "MAIL_DETAILS"})
    if midhun:
        mail.update_one({"_id": "MAIL_DETAILS"}, {"$set": {"last_msg_id": last_msg_id, "mail_id": mail_id}})
    else:
        mail.insert_one({"_id": "MAIL_DETAILS", "mail_id": mail_id, "last_msg_id": last_msg_id})

def add_msg_update_msg(last_msg_id):
    midhun = mail.find_one({"_id": "MAIL_DETAILS")
    if midhun:
        mail.update_one({"_id": "MAIL_DETAILS"}, {"$set": {"last_msg_id": last_msg_id}})
    else:
       return False


def get_msg_id(mail_id):
midhun = mail.find_one({"_id": "MAIL_DETAILS")
    if midhun:
        return midhun["last_msg_id"]
    else:
        return False


def get_mail_id():
    midhun = mail.find_one({"_id": "MAIL_DETAILS")
    if midhun:
        return midhun["mail_id"]
    else:
        return False
