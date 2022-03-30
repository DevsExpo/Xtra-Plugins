# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
import aiohttp
from bs4 import BeautifulSoup
import json
import re

async def get_content(url):
    async with aiohttp.ClientSession() as session:
        r = await session.get(url)
        return await r.read()

@friday_on_cmd(
    ["imdb"],
    cmd_help={
        "help": "it provides details and ratings about given movie/show",
        "example": "{ch}imdb joker",
    }
)
async def _(client,message):
    query = get_text(message)
    msg = await edit_or_reply(message, "`Searching For Movie..`")
    reply = message.reply_to_message or message
    if not query:
        await msg.edit("`Please Give Me An Input.`")
        return
    url = f"https://www.imdb.com/find?ref_=nv_sr_fn&q={query}&s=all"
    r = await get_content(url)
    soup = BeautifulSoup(r, "lxml")
    o_ = soup.find("td", {"class": "result_text"})
    if not o_:
        return await msg.edit("`No Results Found, Matching Your Query.`")
    url = "https://www.imdb.com" + o_.find('a').get('href')
    resp = await get_content(url)
    b = BeautifulSoup(resp, "lxml")
    r_json = json.loads(b.find("script", attrs={"type": "application/ld+json"}).contents[0])
    res_str = "<b>IMDB SEARCH RESULT</b>"
    if r_json.get("@type"):
        res_str += f"\n<b>Type :</b> <code>{r_json['@type']}</code> \n"
    if r_json.get("name"):
        res_str += f"<b>Name :</b> {r_json['name']} \n"
    if r_json.get("contentRating"):
        res_str += f"<b>Content Rating :</b> <code>{r_json['contentRating']}</code> \n"
    if r_json.get("genre"):
        all_genre = r_json['genre']
        genre = "".join(f"{i}, " for i in all_genre)
        genre = genre[:-2]
        res_str += f"<b>Genre :</b> <code>{genre}</code> \n"
    if r_json.get("actor"):
        all_actors = r_json['actor']
        actors = "".join(f"{i['name']}, " for i in all_actors)
        actors = actors[:-2]
        res_str += f"<b>Actors :</b> <code>{actors}</code> \n"
    if r_json.get("trailer"):
        trailer_url = "https://imdb.com" + r_json['trailer']['embedUrl']
        res_str += f"<b>Trailer :</b> {trailer_url} \n"
    if r_json.get("description"):
        res_str += f"<b>Description :</b> <code>{r_json['description']}</code> \n"
    if r_json.get("keywords"):
        keywords = r_json['keywords'].split(",")
        key_ = ""
        for i in keywords:
            i = i.replace(" ", "_")
            key_ += f"#{i}, "
        key_ = key_[:-2]
        res_str += f"<b>Keywords / Tags :</b> {key_} \n"
    if r_json.get("datePublished"):
        res_str += f"<b>Date Published :</b> <code>{r_json['datePublished']}</code> \n"
    if r_json.get("aggregateRating"):
        res_str += f"<b>Rating Count :</b> <code>{r_json['aggregateRating']['ratingCount']}</code> \n<b>Rating Value :</b> <code>{r_json['aggregateRating']['ratingValue']}</code> \n"
    res_str += f"<b>URL :</b> {url}"
    if thumb := r_json.get('image'):
        await msg.delete()
        return await reply.reply_photo(thumb, caption=res_str)
    await msg.edit(res_str)  
