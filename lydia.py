from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from main_startup.config_var import Config
from xtraplugins.dB.lydia import (
    remove_chat,
    add_chat,
    get_all_chats
)

if Config.LYDIA_API_KEY:
    api_key = Config.LYDIA_API_KEY
    lydia = LydiaAI(api_key)

@friday_on_cmd(
        ["addcf"],
        is_official=False,
        cmd_help={
            "help": "Activate Lydia In The Chat!",
            "example": "{ch}addcf"
        }
    )
async def addcf(client, message):
    pablo = await edit_or_reply(message, "`Processing...`")
    session = lydia.create_session()
    session_id = session.id
    lol = add_chat(message.chat.id, session_id)
    if not lol:
        await pablo.edit("Lydia Already Activated In This Chat")
        return
    
#todo
