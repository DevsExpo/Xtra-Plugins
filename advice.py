from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
import requests

@friday_on_cmd(
    ["advice"],
    cmd_help={
        "help": "Gives You Simple Advice",
        "example": "{ch}advice",
    },
)
async def advice(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    r = requests.get("https://api.adviceslip.com/advice")
    await pablo.edit(r.json()["slip"]["advice"])



