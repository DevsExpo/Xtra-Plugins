from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
import requests


@friday_on_cmd(
    ["ua", "user_agent"],
    cmd_help={
        "help": "Get Info From user agent",
        "example": "{ch}ua (user agent)",
    },
)
async def useragenti(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    tex_t = get_text(message)
    if not tex_t:
        await stark.edit(engine.get_string("INPUT_REQ").format("User Agent"))
        return
    ue = tex_t
    data = {"ua" : ue}
    r = requests.post("https://api.apicagent.com", data = data)
    Lol = r.json()
    await pablo.edit(f"""
Browser: {Lol["client"]["name"]}
Browser Version: {Lol["client"]["version"]}
device Brand: {Lol["device"]["brand"]}
device Model: {Lol["device"]["model"]}
OS: {Lol["os"]["name"]}
OS version: {Lol["os"]["version"]}
""")
