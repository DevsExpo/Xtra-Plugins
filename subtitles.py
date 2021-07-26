# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import requests
import os
import aiohttp
import requests
from bs4 import BeautifulSoup as bs
import shutil
from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
BASE_URL = "https://isubtitles.org"

async def search_sub(query):
    BASE_URL = "https://isubtitles.org"
    final_url = f"{BASE_URL}/search?kwd={query}"
    async with aiohttp.ClientSession() as session:
      async with session.get(final_url) as resp:
          r = await resp.text()
    soup = bs(r, "lxml")
    list_search = soup.find_all("div", class_="row")
    index = []
    title = []
    keywords = []
    second_soup = bs(str(list_search), 'lxml')
    headings = second_soup.find_all("h3")
    third_soup = bs(str(headings), "lxml")
    search_links = third_soup.find_all("a")
    for i, a in enumerate(search_links, start=1):
        index.append(i)
        title.append(a.text)
        key = a.get("href").split("/")
        keywords.append(key[1])
    return index, title, keywords

async def get_lang(keyword):
    BASE_URL = "https://isubtitles.org"
    url = f"{BASE_URL}/{keyword}"
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
          request = await resp.text()
    fourth_soup = bs(request, "lxml")
    filesoup = fourth_soup.find_all("table")
    fifth_soup = bs(str(filesoup), "lxml")
    table_soup = fifth_soup.find_all("a")
    language = []
    index = []
    link = []
    i = 0
    for b in table_soup:
        if b["href"].startswith("/download/"):
            i += 1
            h = b.get("href").split("/")
            buttoname = h[3]
            if buttoname not in language:
                index.append(i)
                language.append(buttoname)
                link.append(f"{BASE_URL}{b.get('href')}")
    return index, language, link

@friday_on_cmd(
    ["subs", "substitle", "subdl"],
    cmd_help={
        "help": "Get Subtitle Of A Movie.",
        "example": "{ch}subs tenet",
    },
)
async def get_s(client, message):
    msg = await edit_or_reply(message, "`Searching For Query..`")
    input_str = get_text(message)
    if not input_str:
        return await msg.edit("`Give Movie Name As Input!`")
    index, title, keywords = await search_sub(input_str)
    if not keywords:
        return await msg.edit("`No Results Found.`")
    index, language, link = await get_lang(keywords[0])
    if os.path.exists("./subs/"):
        os.rmdir("./subs/")
    os.mkdir("./subs/")
    for (x ,y) in zip(language, link):
        r = requests.get(y)
        place = f"./subs/{x}_{keywords[0]}"
        with open(place, 'wb') as f:
            f.write(r.content)
    await msg.edit("`Zipping Subtitles.`")
    nme = f"{keywords[0]}_subs"
    shutil.make_archive(nme, "zip", "./subs/")
    file = f"{nme}.zip"
    caption = f"<b><u>Subtitle</b></u> \n<b>Query :</b> <code>{input_str}</code> \n<b>KeyWord :</b> <code>{keywords[0]}</code>"
    await msg.edit("`Uploading Subtitles As Zip.`")
    await client.send_document(
        message.chat.id,
        file,
        caption=caption
    )
    if os.path.exists(file):
        os.remove(file)
    if os.path.exists("./subs/"):
        shutil.rmtree("./subs/")
    await msg.delete()