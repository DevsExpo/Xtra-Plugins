import logging
import os
import requests
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["git", "github"],
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
    
