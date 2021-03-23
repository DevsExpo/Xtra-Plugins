import io
import os
from tswift import Song

from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text



@friday_on_cmd(
    ["lyrics"],
    cmd_help={
        "help": "This plugin searches for song lyrics with song name",
        "example": "{ch}lyrics <song name>",
    },
)
async def _(client,message):
    query = get_text(message)
    lel = await edit_or_reply("Searching For Lyrics.....")
    if not query:
        await lel.edit("`What I am Supposed to find `")
        return

    song = ""
    song = Song.find_song(query)
    if song:
        if song.lyrics:
            reply = song.format()
        else:
            reply = "Couldn't find any lyrics for that song! try with artist name along with song if still doesnt work try `.glyrics`"
    else:
        reply = "lyrics not found! try with artist name along with song if still doesnt work try `.glyrics`"

    if len(reply) > 4095:
        with io.BytesIO(str.encode(reply)) as out_file:
            out_file.name = "lyrics.text"
            await client.send_document(
                message.chat.id,
                out_file,
                caption=query,
                reply_to_msg_id=message.message_id,
            )
            await lel.delete()
    else:
        await lel.edit(reply)
