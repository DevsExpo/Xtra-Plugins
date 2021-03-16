from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.helper_func.basic_helpers import edit_or_reply, get_readable_time, delete_or_pass, progress, is_admin_or_owner, get_user, get_text, iter_chats, edit_or_send_as_file
import asyncio
from pyrogram.types import ChatPermissions
from pyrogram.errors import FloodWait
import math
import os
from asyncio import sleep
from datetime import datetime
from pyrogram import filters
from main_startup.config_var import Config
from main_startup.helper_func.logger_s import LogIt
from main_startup import Friday
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests
from xtraplugins.dB.fban_db import add_fed, rmfed, get_all_feds, is_fed_in_db, rm_all_fed

@friday_on_cmd(['fadd', 'addfed'])
async def free_fbans(client, message):
    uj = await edit_or_reply(message, "`Adding Fed To Database!`")
    f_id = get_text(message)
    if not f_id:
      await uj.edit("`Give Fed ID :/`")
      return
    if is_fed_in_db(f_id):
      await uj.edit("`Fed Already Exists In DB!`")
      return
    add_fed(f_id)
    await uj.edit(f"`Added {f_id} To dB!`")
    
@friday_on_cmd(['frm', 'rmfed'])
async def paid_fbans(client, message):
    uj = await edit_or_reply(message, "`Adding Fed To Database!`")
    f_id = get_text(message)
    if not f_id:
      await uj.edit("`Give Fed ID :/`")
      return
    if f_id == "all":
      rm_all_fed()
      await uj.edit("`Removed All Fed From DB!`")
      return
    if not is_fed_in_db(f_id):
      await uj.edit("`Fed Doesn't Exists In DB!`")
      return
    rmfed(f_id)
    await uj.edit(f"`Removed {f_id} From dB!`")
    
@friday_on_cmd(['fban', 'fedban'])
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
    fed_s = get_all_feds()
    if len(fed_s) > 1:
      await uj.edit("`You Need Atleast One Fed In Db To Use This Plugin!`")
      return
    try:
      await client.send_message(Config.FBAN_GROUP, "/start")
    except:
      await uj.edit(f"`Unable To Send Message To Fban Group! \nTraceBack : {e}`")
      return
    for i in fed_s:
      await asyncio.sleep(2)
      try:
          await client.send_message(Config.FBAN_GROUP, f"/joinfed {i}")
          await client.send_message(Config.FBAN_GROUP, f"/fban {ur}")
      except FloodWait as e:
          await asyncio.sleep(e.x)
      except:
          failed_n += 1
    good_f_msg = f"**FBANNED** \n**Affected Feds :** `{len(fed_s) - failed_n}` \n**Failed :** `{failed_n}` \n**Total Fed :** `{len(fed_s)}`"
    await uj.edit(good_f_msg)
