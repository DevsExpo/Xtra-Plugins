import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from main_startup import Friday
from main_startup.config_var import Config
from xtraplugins.dB.mail_tools import (
    add_mail_update_mail,
    get_msg_id,
    get_mail_id,
    add_msg_update_msg
)


supported_domains = ["esiix.com", "1secmail.net", "wwjmp.com"]


@friday_on_cmd(
    ["add_mail"],
    is_official=False,
    cmd_help={
        "help": "Create Temporary Mail",
        "example": "{ch}add_mail (mail-id)",
    },
)
async def add_mail_to_db(client, message):
    pablo = await edit_or_reply(message, "`Processing.....`")
    mail_id = get_text(message)
    if not mail_id:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    lmao = anime.split("@", 1)
    try:
        domain = lmao[1]
    except BaseException:
        await pablo.edit(
            "What are you providing me lmao?."
        )
        return
    if domain.lower() in supported_domains:
        pass
    else:
        await pablo.edit("oops, I don't own that domain.")
        return
    add_mail_update_mail(mail_id)
    await pablo.edit(f"Your Mail ID {mail_id} successfully added to dB")


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
        await pablo.edit("You Sure You Added Your Mail To dB?")
        return
    caption = ""
    lmao = anime.split("@", 1)
    login = lmao[0]
    domain = lmao[1]
    link = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
    r = requests.get(domain)
    lmao = r.json()
    kk = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={lmao[0].get('id')}"
    r = requests.get(kk)
    lmao = r.json()
    last = f""" Mail From : {lmao.get("from")}

Subject : {lmao.get("subject")}

Body : {lmao.get("textBody")}
"""
    await pablo.edit(last)


