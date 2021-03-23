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
)


supported_domains = ["esiix.com", "1secmail.net", "wwjmp.com"]


@friday_on_cmd(
    ["add_mail"],
    is_official=False,
    cmd_help={
        "help": "Create Temporary Mail",
        "example": "{ch}mail (mail-id)",
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
