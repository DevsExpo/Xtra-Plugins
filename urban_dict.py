# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.


import requests
import os
import requests
from bs4 import BeautifulSoup as bs
import shutil
from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, humanbytes, edit_or_send_as_file
from main_startup.helper_func.logger_s import LogIt
import os

import asyncurban

@friday_on_cmd(['ud', 'urban'],
               cmd_help={
               "help": "Get Meaning Of A Work From Query",
               "example": "{ch}ud hello"
})
async def u_d_(client, message):
    ms_ = await edit_or_reply(message, "`Please Wait.`")
    ud = asyncurban.UrbanDictionary()
    query_ = get_text(message)
    if not query_:
        return await ms_.edit("`Please Give Me Query As Input.`")
    try:
        u_d_ = await ud.get_word(query_)
    except asyncurban.UrbanException as exc:
        return await ms_.edit(f"`[UrbanDict - Async] : {exc}`")
    nice_t = f"<b>Query :</b> <code>{u_d_.word}</code> \n<b>Definition :</b> <i>{u_d_.definition}</i> \n<b>Example :</b> <i>{u_d_.example}</i>"
    await edit_or_send_as_file(nice_t, ms_, client, f"`[URBAN_DICT] - {query_}`", f"{query_}_ud", parse_mode="html")
    await ud.close()
