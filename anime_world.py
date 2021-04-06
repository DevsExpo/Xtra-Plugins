# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from anime_downloader.sites import get_anime_class
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from mal import Anime, AnimeSearch, Manga, MangaSearch


@friday_on_cmd(
    ["anime", "animes"],
    is_official=False,
    cmd_help={
        "help": "Automatically Gets Streaming Link Of The Anime. Get Site names list from Here : https://devsexpoanime.netlify.app",
        "example": "{ch}anime (anime name:site name)",
    },
)
async def anime(client, message):
    pablo = await edit_or_reply(message, "`Searching For Anime.....`")
    anime = get_text(message)
    if not anime:
        await pablo.edit("`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`")
        return
    lmao = anime.split(":", 1)
    try:
        site = lmao[1]
    except BaseException:
        site = "animeonline360"
        await pablo.edit(
            "Please Provide Site Name From Next Time. Now Continuing With Default Site."
        )

    lol = lmao[0]
    why = site.lower()
    Twist = get_anime_class(why)
    try:
        search = Twist.search(lol)
    except BaseException:
        await ommhg.edit("Please Try Different Site. Given Site Is Down.")

    title1 = search[0].title
    url1 = search[0].url
    title2 = search[1].title
    url2 = search[1].url
    title3 = search[2].title
    url3 = search[2].url
    title4 = search[3].title
    url4 = search[3].url
    title5 = search[4].title
    url5 = search[4].url
    NopZ = f"<b><u>Anime Search Complete</b></u> \n\n\n<b>Title</b>:-  <code>{title1}</code> \n<b>URL Link</b>:- {url1}\n\n<b>Title</b>:-  <code>{title2}</code> \n<b>URL Link</b>:- {url2}\n\n<b>Title</b>:-  <code>{title3}</code>\n<b>URL Link</b>:- {url3}\n\n<b>Title</b>:-  <code>{title4}</code> \n<b>URL Link</b>:- {url4}\n\n<b>Title</b>:-  <code>{title5}</code> \n<b>URL Link</b>:- {url5}\n\n<b>Links Gathered By Friday\nGet Your Own Friday From @FRIDAYCHAT</b>"
    await pablo.edit(NopZ, parse_mode="html")


@friday_on_cmd(
    ["animeinfo", "ainfo"],
    is_official=False,
    cmd_help={
        "help": "Gives Anime Information!",
        "example": "{ch}ainfo (anime name)",
    },
)
async def animeinfo(client, message):
    pablo = await edit_or_reply(message, "`Searching For Anime.....`")
    anime = get_text(message)
    if not anime:
        await pablo.edit("`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`")
        return
    search = AnimeSearch(anime)
    ID = search.results[0].mal_id
    anime = Anime(ID)
    jp = ""
    for x in anime.genres:
        jp += x + ";  "
    link = anime.image_url
    if link is None:
        link = search.results[0].image_url
    By = f"""<u><b>Anime Information Gathered</b></u>
<b>tlele:- {search.results[0].title}
Mal ID:- {search.results[0].mal_id}
Url:- {search.results[0].url}
Type:- {search.results[0].type}
Episodes:- {search.results[0].episodes}
Score:- {search.results[0].score}
Synopsis:- {search.results[0].synopsis}
Status:- {anime.status}
Genres:- {jp}
Duration:- {anime.duration}
Popularity:- {anime.popularity}
Rank:- {anime.rank}
favorites:- {anime.favorites}</b>
"""
    await pablo.edit(By, parse_mode="html")


@friday_on_cmd(
    ["manga", "mangainfo"],
    is_official=False,
    cmd_help={
        "help": "Gives manga Information!",
        "example": "{ch}manga (manga name)",
    },
)
async def manga(client, message):
    pablo = await edit_or_reply(message, "`Searching For Manga.....`")
    anime = get_text(message)
    if not anime:
        await pablo.edit("`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`")
        return
    search = MangaSearch(anime)
    ID = search.results[0].mal_id
    manga = Manga(ID)
    jp = ""
    for x in manga.genres:
        jp += x + ";  "
    link = manga.image_url
    if link is None:
        link = search.results[0].image_url
    By = f"""<u><b>manga Information Gathered</b></u>
<b>tlele:- {search.results[0].title}
Mal ID:- {search.results[0].mal_id}
Url:- {search.results[0].url}
Type:- {search.results[0].type}
volumes:- {search.results[0].volumes}
Score:- {search.results[0].score}
Synopsis:- {search.results[0].synopsis}
Status:- {manga.status}
Genres:- {jp}
Chapters:- {manga.chapters}
Popularity:- {manga.popularity}
Rank:- {manga.rank}
favorites:- {manga.favorites}</b>
"""
    await pablo.edit(By, parse_mode="html")
