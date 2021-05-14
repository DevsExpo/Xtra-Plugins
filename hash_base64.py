# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import base64
from main_startup.core.decorators import friday_on_cmd
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
)
import hashlib




def hasher(string_to_hash: str):
    a = hashlib.md5(string_to_hash.encode())
    stark_md5 = a.hexdigest()
    b = hashlib.sha1(string_to_hash.encode())
    stark_sha1 = b.hexdigest()
    c = hashlib.sha256(string_to_hash.encode())
    stark_sha256 = c.hexdigest()
    d = hashlib.sha512(string_to_hash.encode())
    stark_sha512 = d.hexdigest()
    return stark_md5, stark_sha1, stark_sha256, stark_sha512




@friday_on_cmd(
    cmd=["hash_text"],
    cmd_help={"help": "Hash Message", "example": '{ch}hash_text (input)'},
)
async def get_trash(client, message):
    msg = await edit_or_reply(message, "`Please Wait..`")
    hashtxt_ = get_text(message)
    if not hashtxt_:
        return await msg.edit("`Give Input. Please?`")
    md5, sha1, sha256, sha512 = hasher(str(hashtxt_))
    ans = (
        "Text: `"
        + hashtxt_
        + "`\nMD5: `"
        + md5
        + "`SHA1: `"
        + sha1
        + "`SHA256: `"
        + sha256
        + "`SHA512: `"
        + sha512
        + "`"
    )
    await edit_or_send_as_file(ans, msg, client, "Hashed Result" , "hash-result")


en = ["en", "encode", "enc"]

@friday_on_cmd(
    cmd=["base_64"],
    cmd_help={"help": "Encode/Decode Message to base64", "example": '{ch}base_64 (replying to message)'},
)
async def _base(client, message):
    msg = await edit_or_reply(message, "`Please Wait.`")
    input_ = get_text(message) or "en"
    if not message.reply_to_message:
        return await msg.edit("`Reply To Message To base64 Encode / Decode.`")
    if not message.reply_to_message.text:
        return await msg.edit("`Reply To Message To base64 Encode / Decode.`")
    s = message.reply_to_message.text
    if input_ in en:
        en_ = base64.b64encode(s.encode())
        await msg.edit(f"**Encoded :** `{en_}`")
    else:
        de_ = base64.b64decode(s.encode())
        await msg.edit(f"**Decoded :** `{de_}`")