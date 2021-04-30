from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply
from quotefancy import get_quote


@friday_on_cmd(
    ['quotefancy'],
    is_official=False,
    cmd_help={
    "help": "Get Random Quote from QuoteFancy.com",
    "example": "{ch}quotefancy"
    })
async def quotefancy(client, message):
    msg = await edit_or_reply(message, "`Please Wait !`")
    try:
        imglink = get_quote("image")
        await message.reply_photo(imglink) # Dont Download
    except Exception as e:
        await msg.edit(f"**Error** - {str(e)}")
