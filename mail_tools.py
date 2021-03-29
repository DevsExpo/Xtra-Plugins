import requests
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from main_startup import Friday
from main_startup.config_var import Config
from xtraplugins.dB.mail_tools import (
    add_mail_update_mail,
    get_msg_id,
    get_mail_id,
    add_msg_update_msg,
    delete_mail_id
)


supported_domains = ["esiix.com", "1secmail.net", "wwjmp.com"]


@friday_on_cmd(
        ["add_mail"],
        is_official=False,
        cmd_help={
            "help": "Create Temporary Mail!",
            "example": "{ch}add_mail (mail-id)"
        }
    )
async def add_mail_to_db(client, message):
    pablo = await edit_or_reply(message, "`Processing.....`")
    mail_id = get_text(message)
    if not mail_id:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    lmao = mail_id.split("@", 1)
    try:
        domain = lmao[1]
    except BaseException:
        await pablo.edit(
            "`What are you providing me lmao?. Check Help Menu Idiot!`"
        )
        return
    if domain.lower() in supported_domains:
        pass
    else:
        await pablo.edit("`Oops, I don't Support that Domain! Check Help Menu To Get Supported Site List!`")
        return
    add_mail_update_mail(mail_id)
    await pablo.edit(f"`Your Mail ID {mail_id} successfully added to dB`")


@friday_on_cmd(
    ["check_mail"],
    is_official=False,
    cmd_help={
        "help": "Check Temporary Mail",
        "example": "{ch}check_mail",
    },
)
async def check_mail(client, message):
    pablo = await edit_or_reply(message, "`Processing.....`")
    email = get_mail_id()
    if not email:
        await pablo.edit("`You Sure You Added Your Mail To dB?`")
        return
    caption = ""
    mail_ = email.split("@", 1)
    login = mail_[0]
    domain = mail_[1]
    link = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
    r = requests.get(link)
    r_json = r.json()
    try:
        latest_mail = r_json[0].get('id')
    except IndexError:
        await pablo.edit("`You Don't Have Any Mails Yet ;( Ask Your Gf To Send Some Nudes!`")
        return
    kk = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={latest_mail}"
    r = requests.get(kk)
    lmao = r.json()
    is_file = False
    if lmao["attachments"] != []:
        fl_name = lmao["attachments"][0].get("filename")
        is_file = True
        lenk = f'https://www.1secmail.com/api/v1/?action=download&login={login}&domain={domain}&id={lmao.get("id")}&file={fl_name}'
        r = requests.get(lenk)
        with open(fl_name, 'wb') as f:
            f.write(r.content)
    last = f""" 
<b>Mail From :</b> <code>{lmao.get("from")}</code>
<b>Date :</b> <code>{lmao.get("date")}</code>
<b>Subject :</b> <code>{lmao.get("subject")}</code>

<b>Body :</b> <code>{lmao.get("textBody")}</code>
"""
    if not is_file:
        await pablo.edit(last, parse_mode="html")
    else:
        await client.send_document(message.chat.id, fl_name, caption = last, parse_mode="html")
        os.remove(fl_name)
        await pablo.delete()
        


@friday_on_cmd(
    ["delete_mail"],
    is_official=False,
    cmd_help={
        "help": "Delete Temporary Mail",
        "example": "{ch}delete_mail",
    },
)
async def delete_mail(client, message):
    pablo = await edit_or_reply(message, "`Processing.....`")
    email = get_mail_id()
    if not email:
        await pablo.edit("`You Sure You Added Your Mail To dB?`")
        return
    delete_mail_id()
    await pablo.edit("Successfully Deleted Your Email")


async def track_mails():
    email = get_mail_id()
    if not email:
        return
    caption = ""
    last_msg = get_msg_id(email)
    mail_ = email.split("@", 1)
    login = mail_[0]
    domain = mail_[1]
    link = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
    r = requests.get(link)
    r_json = r.json()
    try:
        latest_mail = r_json[0].get('id')
    except IndexError:
        return
    if last_msg == latest_mail:
        return
    else:
        add_msg_update_msg(latest_mail)
    
    kk = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={latest_mail}"
    r = requests.get(kk)
    lmao = r.json()
    is_file = False
    if lmao["attachments"] != []:
        fl_name = lmao["attachments"][0].get("filename")
        is_file = True
        lenk = f'https://www.1secmail.com/api/v1/?action=download&login={login}&domain={domain}&id={lmao.get("id")}&file={fl_name}'
        r = requests.get(lenk)
        with open(fl_name, 'wb') as f:
            f.write(r.content)
    last = f""" #EMAIL_RECEIVED
<b>Mail From :</b> <code>{lmao.get("from")}</code>
<b>Date :</b> <code>{lmao.get("date")}</code>
<b>Subject :</b> <code>{lmao.get("subject")}</code>

<b>Body :</b> <code>{lmao.get("textBody")}</code>
"""
    if not is_file:
        await Friday.send_message(
                Config.LOG_GRP, last, parse_mode="html")
    else:
        await Friday.send_document(message.chat.id, fl_name, caption = last, parse_mode="html")
        os.remove(fl_name)
        await pablo.delete()
        
scheduler = AsyncIOScheduler()
scheduler.add_job(track_mails, 'interval', minutes=10)
scheduler.start()
