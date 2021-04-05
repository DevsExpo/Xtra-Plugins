# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, edit_or_send_as_file, get_user, get_text
import os
from main_startup.core.startup_helpers import run_cmd


@friday_on_cmd(['maigret'],
               cmd_help={
                "help": "Get A User's Whole Social Data List By Just A Name",
                "example": "{ch}maigret spechide"})
async def me_great(client, message):
    msg_ = await edit_or_reply(message, "`Searching For This User. This Can Take Upto 5 Minutes.`")
    user_n = get_text(message)
    if not user_n:
        await msg_.edit("`Give Me Username As Input.`")
        return
    maigret_cmd = f"maigret {user_n} -n 150 -a --timeout 15  --pdf"
    await run_cmd(maigret_cmd)
    file_n = f"reports/report_{user_n}.pdf"
    captio_n = f"OSINT For {user_n} By FridayUB."
    if not os.path.exists(file_n):
        await msg_.edit("`Unable To Fetch Data. Maybe This User Likes To Keep A Air Of Mystery!`")
        return
    if message.reply_to_message:
        await client.send_document(
            message.chat.id,
            file_n,
            caption=captio_n,
            reply_to_message_id=message.reply_to_message.message_id
        )
    else:
        await client.send_document(message.chat.id, file_n, caption=captio_n)
    if os.path.exists(file_n):
        os.remove(file_n)
    await msg_.delete()