# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import os
import logging
from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from pyrogram.errors import FloodWait
from xtraplugins.dB.fban_db import (
    add_fed,
    get_all_feds,
    is_fed_in_db,
    rm_all_fed,
    rmfed,
)


@friday_on_cmd(
    ["fadd", "addfed"],
    is_official=False,
    cmd_help={
        "help": "Add Feds To dB!",
        "example": "{ch}fadd (enter your FED ID OR mention 'all' to add all)",
    },
)
async def free_fbans(client, message):
    uj = await edit_or_reply(message, "`Adding Fed To Database!`")
    f_id = get_text(message)
    if not f_id:
        await uj.edit("`Give Fed ID :/`")
        return
    if f_id == "all":
        fed_l = await fetch_all_fed(client, message)
        if not fed_l:
            await uj.edit("`Either My Logic Broke Or You Are Not Admin in Any Fed!`")
            return
        e = 0
        for ujwal in fed_l:
            if not await is_fed_in_db(ujwal):
                await add_fed(ujwal)
            else:
                e += 1
        await uj.edit(
            f"`Added {len(fed_l) - e} Feds To Database! Failed To Add {e} Feds!`"
        )
        return
    if await is_fed_in_db(f_id):
        await uj.edit("`Fed Already Exists In DB!`")
        return
    await add_fed(f_id)
    await uj.edit(f"`Added {f_id} To dB!`")


@friday_on_cmd(
    ["frm", "rmfed"],
    cmd_help={
        "help": "Remove Feds From dB!",
        "example": "{ch}frm (enter your FED ID OR mention 'all' to Remove all)",
    },
)
async def paid_fbans(client, message):
    uj = await edit_or_reply(message, "`Removing Fed From Database!`")
    f_id = get_text(message)
    if not f_id:
        await uj.edit("`Give Fed ID :/`")
        return
    if f_id == "all":
        await rm_all_fed()
        await uj.edit("`Removed All Fed From DB!`")
        return
    if not await is_fed_in_db(f_id):
        await uj.edit("`Fed Doesn't Exists In DB!`")
        return
    await rmfed(f_id)
    await uj.edit(f"`Removed {f_id} From dB!`")


@friday_on_cmd(
    ["fban", "fedban"],
    is_official=False,
    cmd_help={
        "help": "Fban a user!",
        "example": "{ch}fban (enter username or id)",
    },
)
async def fban_s(client, message):
    uj = await edit_or_reply(message, "`Fbanning!`")
    failed_n = 0
    ur = get_text(message)
    if not ur:
        await uj.edit("`Who Should I Fban? You?`")
        return
    if not Config.FBAN_GROUP:
        await uj.edit("`Please Setup Fban Group!`")
        return
    fed_s = await get_all_feds()
    if len(fed_s) == 0:
        await uj.edit("`You Need Atleast One Fed In Db To Use This Plugin!`")
        return
    await uj.edit(f"`Fbanning In {len(fed_s)} Feds!`")
    try:
        await client.send_message(Config.FBAN_GROUP, "/start")
    except BaseException:
        await uj.edit(f"`Unable To Send Message To Fban Group! \nTraceBack : {e}`")
        return
    for i in fed_s:
        await asyncio.sleep(2)
        try:
            await client.send_message(Config.FBAN_GROUP, f"/joinfed {i['fed_s']}")
            await client.send_message(Config.FBAN_GROUP, f"/fban {ur}")
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except BaseException as eb:
            logging.error(eb)
            failed_n += 1
    good_f_msg = f"**FBANNED** \n**Affected Feds :** `{len(fed_s) - failed_n}` \n**Failed :** `{failed_n}` \n**Total Fed :** `{len(fed_s)}`"
    await uj.edit(good_f_msg)

@friday_on_cmd(
    ["unfban", "unfedban"],
    is_official=False,
    cmd_help={
        "help": "Un-Fban a user!",
        "example": "{ch}unfban (enter username or id)",
    },
)
async def un_fban_s(client, message):
    uj = await edit_or_reply(message, "`Fbanning!`")
    failed_n = 0
    ur = get_text(message)
    if not ur:
        await uj.edit("`Who Should I Un-Fban? You?`")
        return
    if not Config.FBAN_GROUP:
        await uj.edit("`Please Setup Fban Group!`")
        return
    fed_s = await get_all_feds()
    if len(fed_s) == 0:
        await uj.edit("`You Need Atleast One Fed In Db To Use This Plugin!`")
        return
    await uj.edit(f"`Un-Fbanning In {len(fed_s)} Feds!`")
    try:
        await client.send_message(Config.FBAN_GROUP, "/start")
    except BaseException:
        await uj.edit(f"`Unable To Send Message To Fban Group! \nTraceBack : {e}`")
        return
    for i in fed_s:
        await asyncio.sleep(2)
        try:
            await client.send_message(Config.FBAN_GROUP, f"/joinfed {i['fed_s']}")
            await client.send_message(Config.FBAN_GROUP, f"/unfban {ur}")
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except BaseException as eb:
            logging.error(eb)
            failed_n += 1
    good_f_msg = f"**UN-FBANNED** \n**Affected Feds :** `{len(fed_s) - failed_n}` \n**Failed :** `{failed_n}` \n**Total Fed :** `{len(fed_s)}`"
    await uj.edit(good_f_msg)


async def fetch_all_fed(client, message):
    fed_list = []
    await client.send_message("@MissRose_bot", "/myfeds")
    await asyncio.sleep(3)
    ok = (await client.get_history("@MissRose_bot", 1))[0]
    if "5 minutes" in ok.text:
        return None
    if "file to list" in ok.text.lower():
        try:
            await ok.click(0)
        except TimeoutError:
            pass
        await asyncio.sleep(7)
        sed = (await client.get_history("@MissRose_bot", 1))[0]
        if not sed.media:
            return None
        fed_file = await sed.download()
        file = open(fed_file, "r")
        lines = file.readlines()
        for line in lines:
            try:
                fed_list.append(line[:36])
            except BaseException:
                pass
        os.remove(fed_file)
    else:
        X = ok.text
        lol = X.splitlines()
        if "you are the owner" in X.lower():
            for lo in lol:
                if (
                    "you are the owner" not in lo.lower()
                    and "you are admin" not in lo.lower()
                    and lo[:36] != ""
                ):
                    if not lo.startswith("-"):
                        fed_list.append(lo[:36])
                    else:
                        fed_list.append(lo[2:38])
        else:
            Y = X[44:].splitlines()
            for lol in Y:
               fed_list.append(lol[2:38])
    return fed_list
