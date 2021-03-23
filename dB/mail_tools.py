from database import db_x

mail = db_x["MAIL"]


def add_mail_update_mail(mail_id, last_msg_id=""):
    midhun = mail.find_one({"_id": "MAIL_DETAILS")
    if midhun:
        mail.update_one({"_id": "MAIL_DETAILS"}, {"$set": {"mail_id": mail_id}})
        mail.update_one({"_id": "MAIL_DETAILS"}, {"$set": {"last_msg_id": last_msg_id}})
    else:
        mail.insert_one({"_id": "MAIL_DETAILS", "mail_id": mail_id, "last_msg_id": last_msg_id})


