# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, edit_or_send_as_file
import calendar
from datetime import datetime


@friday_on_cmd(['time'],
               cmd_help={
                   "help": "Check Current Date , Time & Calender.",
                   "example": "{ch}time"
              }
)
async def _d(client, message):
    year_ = datetime.now().year
    date_ = datetime.now().day
    month_ = datetime.now().month
    mydate = datetime.now()
    da = mydate.strftime("Date : %d \nMonth : %B \nYear : %Y")
    dt = mydate.strftime("Hour : %H \nMinute : %M")
    cal_ = calendar.month(year_, month_)
    f_d = f"<code>{cal_}\n{da} \n\n{dt}</code>"
    await edit_or_reply(message, f_d, parse_mode="html")
