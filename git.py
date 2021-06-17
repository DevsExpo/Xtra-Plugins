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
    r = requests.get("https://api.github.com/search/repositories", params= f"q={args}")
    lool = r.json()
    if lool.get("total_count")==0:
        await pablo.edit(engine.get_string("F_404"))
        return
    else:
        lol = lool.get("items")
        qw = lol[0]
        txt = f"""
Name: {qw.get("name")}
Full Name: {qw.get("full_name")}
Link: {qw.get("html_url")}
Description: {qw.get("description")}
Language: {qw.get("language")}
Fork Count: {qw.get("forks_count")}
Open Issues: {qw.get("open_issues")}
"""
        await pablo.edit(txt)
