from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_readable_time, delete_or_pass, progress, get_text, edit_or_send_as_file
import asyncio
import math
import time
from pyrogram import filters
from main_startup.config_var import Config
import requests


@friday_on_cmd(["ekart"], 
is_official=False,
cmd_help={
        "help": "Get Ekart Details!",
        "example": "{ch}ekart (ekart id)",
    },)
async def ekart(client, message):
    pablo = await edit_or_reply(message, "`Processing.....`")
    input_str = get_text(message)
    if not input_str:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    urlo = "https://track.aftership.com/trackings?courier=ekart&tracking-numbers=" + str(input_str)
    
    url = "https://ekart-api-chi.vercel.app/check?id=" + str(input_str)
    r = requests.get(url)
    h = r.json()
    merchant = h.get("merchant_name")
    order_status = h.get("order_status")
    kk = h.get("updates")
    oqwz = kk[0]
    aq = oqwz.get("Date")
    ar = oqwz.get("Time")
    place = oqwz.get("Place")
    status = oqwz.get("Status")
    
    
    caption = f""" <b>Ekart Tracking </b>
Merchant Name:- {merchant}
Order Status:- {order_status}
Tracking Id:- {input_str}
Latest Update
Date:- {aq}
Time:- {ar}
Place:- {place}
Status:- {status}
Detailed link:- {urlo}
<u><b>Ekart Search Completed By Friday.
Get Your Own Friday From @FRIDAYCHAT.</b></u>
"""
    await pablo.edit(caption, parse_mode="HTML")
