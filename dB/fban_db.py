from database import db_x

fed = db_x["FED"]


def add_fed(feds):
    fed.insert_one({"fed": feds})


def rmfed(feds):
    fed.delete_one({"fed": feds})


def get_all_feds():
    lol = list(fed.find())
    return lol


def is_fed_in_db(feds):
    k = fed.find_one({"fed": feds})
    if k:
        return True
    else:
        return False
