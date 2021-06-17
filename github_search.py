# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.


import logging
import os
import requests
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["git"],
    cmd_help={
        "help": "Search In GitHub",
        "example": "{ch}git <text>",
    },
)
async def git(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    args = get_text(message)
    if not args:
        await pablo.edit(engine.get_string("INPUT_REQ").format("Search Text"))
        return
    r = requests.get("https://api.github.com/search/repositories", params={"q": args})
    lool = r.json()
    if lool.get("total_count") == 0:
        await pablo.edit(engine.get_string("F_404"))
        return
    else:
        lol = lool.get("items")
        qw = lol[0]
        txt = f"""
<b>Name :</b> <i>{qw.get("name")}</i>
<b>Full Name :</b> <i>{qw.get("full_name")}</i>
<b>Link :</b> {qw.get("html_url")}
<b>Fork Count :</b> <i>{qw.get("forks_count")}</i>
<b>Open Issues :</b> <i>{qw.get("open_issues")}</i>
"""
        if qw.get("description"):
            txt += f'<b>Description :</b> <code>{qw.get("description")}</code>'
        if qw.get("language"):
            txt += f'<b>Language :</b> <code>{qw.get("language")}</code>'
        if qw.get("size"):
            txt += f'<b>Size :</b> <code>{qw.get("size")}</code>'
        if qw.get("score"):
            txt += f'<b>Score :</b> <code>{qw.get("score")}</code>'
        if qw.get("created_at"):
            txt += f'<b>Created At :</b> <code>{qw.get("created_at")}</code>'
        if qw.get("archived") == True:
            txt += f"<b>This Project is Archived</b>"
        await pablo.edit(txt, disable_web_page_preview=True)
