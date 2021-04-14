# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.


import requests
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, edit_or_send_as_file, get_user


@friday_on_cmd(['ifsc', 'ifsc_lookup'],
               cmd_help={
                'help': 'Get ifsc Code Info.',
                'example': '{ch}ifsc SBIN0008658'})
async def geT_if(client, message):
    m_ = await edit_or_reply(message, "`Please Wait!`")
    input_str = get_text(message)
    if not input_str:
        return await m_.edit("`Give Me IFSC Code As Input.`")
    IFSC_Code = input_str
    URL = "https://ifsc.razorpay.com/"
    data = requests.get(URL + IFSC_Code)
    if "Not Found" in data.text:
        return await m_.edit("`404: IFSC CODE NOT FOUND.`") 
    try:
        data = data.json()
    except:
        return await m_.edit("`Invalid IFSC Code!`") 
    a = data["ADDRESS"]
    b = data["CENTRE"]
    c = data["BRANCH"]
    d = data["CITY"]
    e = data["STATE"]
    f = data["BANK"]
    g = data["BANKCODE"]
    h = data["IFSC"]
    await m_.edit(
        f"<b><u>INFORMATION GATHERED SUCCESSFULLY</b></u>\n\n<b>Bank Name :</b> <code>{f}</code>\n<b>Bank Address :</b> <code>{a}</code>\n<b>Centre :</b> <code>{b}</code>\n<b>Branch :</b> <code>{c}</code>\n<b>City :</b> <code>{d}</code>\n<b>State :</b> <code>{e}</code>\n<b>Bank Code :</b> <code>{g}</code>\n<b>IFSC :</b> <code>{h}</code>",
        parse_mode="html",
    )