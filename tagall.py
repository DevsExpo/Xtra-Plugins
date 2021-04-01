# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["tagall"],
    is_official=False,
    cmd_help={
        "help": "Tag Everyone In The Group.",
        "example": "{ch}tagall Hello",
    },
)
async def tagall(client, message):
    pablo = await edit_or_reply(message, "`Processing.....`")
    sh = get_text(message)
    if not sh:
        sh = "Hi!"
    mentions =""
    async for member in client.iter_chat_members(message.chat.id):
        mentions += member.user.mention + " "
    n = 4096
    kk = [mentions[i:i+n] for i in range(0, len(mentions), n)]
    for i in kk:
        j = f"<b>{sh}</b> \n{i}"
        await client.send_message(message.chat.id, j, parse_mode="html")



