# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
import requests

@friday_on_cmd(
    ["advice"],
    cmd_help={
        "help": "Gives You Simple Advice",
        "example": "{ch}advice",
    },
)
async def advice(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    r = requests.get("https://api.adviceslip.com/advice")
    await pablo.edit(r.json()["slip"]["advice"])
