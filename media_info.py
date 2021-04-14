"""
(C) @DeletedUser420
All rights Reserved.
"""

from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from main_startup.helper_func.logger_s import LogIt
import os
from telegraph import Telegraph

telegraph = Telegraph()
page_ = telegraph.create_account(short_name="Friday 🇮🇳")



@friday_on_cmd(['mediainfo', 'mediadata'],
               cmd_help={
               "help": "Get Full Info Of A Media.",
               "example": "{ch}mediainfo (replying to file)"
})    
async def get_mediainfo(client, message):
    m_ = await edit_or_reply(message, "`Please Wait!`")
    if not message.reply_to_message:
        return await m_.edit("`Reply To Media!`")
    if not message.reply_to_message.media:
        return await m_.edit("`Reply To Media!`")
    file_path = await message.reply_to_message.download()
    out, err, ret, pid = await run_cmd(f"mediainfo '{file_path}'")
    if not out:
        return await m_.edit("`No Media Results Found!`")
    resul_t = out.replace("\n", "<br>")
    media_info = f"""
    <code>           
    {resul_t}                  
    </code>"""
    title_of_page = "Media Info By FridayUB."
    response = telegraph.create_page(title_of_page, html_content=media_info)
    km = response["path"]
    await m_.edit(f"**MediaInfo Can Be Found** [Here](https://telegra.ph/{km})", disable_web_page_preview=True)
    if os.path.exists(file_path):
        os.remove(file_path)
