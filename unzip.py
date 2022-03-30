# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import logging
import os
import pathlib
import time
import time as t
import zipfile
from datetime import datetime

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, humanbytes

extracted = "./downloads/extracted/"


@friday_on_cmd(
    ["unzip"],
    cmd_help={
        "help": "Unzip the Zip File!",
        "example": "{ch}unzip (reply to zip file)",
    },
)
async def test(client, message):
    Pablo = await edit_or_reply(message, "`Processing...`")
    if not message.reply_to_message:
        await Pablo.edit("`Reply To Zip File To Unzip!`")
        return
    if not message.reply_to_message.document:
        await Pablo.edit("`Reply To Zip File To Unzip!`")
        return
    if message.reply_to_message.document.mime_type != "application/zip":
        await Pablo.edit("`Is That Even A Zip?`")
        return
    if not os.path.isdir(extracted):
        os.makedirs(extracted)
    start = datetime.now()
    downloaded_file_name = await message.reply_to_message.download()
    end = datetime.now()
    ms = (end - start).seconds
    await Pablo.edit(
        f"Stored the zip to `{downloaded_file_name}` in {ms} seconds."
    )

    try:
        with zipfile.ZipFile(downloaded_file_name, "r") as zip_ref:
            zip_ref.extractall(extracted)
    except Exception as e:
        await Pablo.edit(f"`Error! Zip Couldn't Extarct Zip. \nTraceBack : {e}`")
        return
    filename = []
    list(file_list(extracted, filename))
    total_files = len(filename)
    failed_s = 0
    await Pablo.edit("`Unzipping, Please Wait!`")
    for single_file in filename:
        if os.path.exists(single_file):
            caption_rts = os.path.basename(single_file)
            size = os.stat(single_file).st_size
            capt = f"<< **{caption_rts}** [`{humanbytes(size)}`] >>"
            try:
                await client.send_document(
                    message.chat.id, single_file, caption=capt, force_document=False
                )
            except Exception as e:
                logging.info(e)
                failed_s += 1
            os.remove(single_file)
    await Pablo.edit(
        f"`Unzipped And Uploaded {total_files-failed_s} File Out Of {total_files}!`"
    )
    os.remove(downloaded_file_name)


def file_list(path, lisT):
    pathlib.Path(path)
    for filepath in pathlib.Path(path).glob("**/*"):
        if os.path.isdir(filepath):
            file_list(filepath, lisT)
        else:
            lisT.append(filepath.absolute())
    return lisT