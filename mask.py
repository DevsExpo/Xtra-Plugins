from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["mask"],
    is_official=False,
    cmd_help={
        "help": "Mask The Images",
        "example": "{ch}mask (Reply To Image)",
    },
)
async def mask(client, message):
    pablo = await edit_or_reply(message, "`Processing...`")
    if not message.reply_to_message:
        await pablo.edit("Please Reply To A Image")
        return
    if message.reply_to_message.sticker:
        if message.reply_to_message.sticker.mime_type == "image/webp":
           pass
        else:
           return
    message.reply_to_message.copy("hazmat_suit_bot")
    messi = (await client.get_history("hazmat_suit_bot", 1))[0]
    await message.reply_photo(messi.photo.file_id)
