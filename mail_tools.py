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

