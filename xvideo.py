import requests
import bs4

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["xvideo"],
    cmd_help={
        "help": "Get direct Downloadable",
        "example": "{ch}xvideo xvideo_link",
    },
)
async def xvid(client, message):
    editer= await edit_or_reply(message, "`Please Wait.....`")
    msg = get_text(message)
    if not msg:
            await editer.edit("`Please Enter Valid Input`")
            return
    try:
        req = requests.get(msg)
        soup = bs4.BeautifulSoup(req.content, 'html.parser')

        soups = soup.find("div",{"id":"video-player-bg"})
        link =""
        for a in soups.find_all('a', href=True):
            link = a["href"]
        await editer.edit(f"HERE IS YOUR LINK:\n`{link}`")
    except:
        await editer.edit("Something went wrong")


@friday_on_cmd(
    ["xsearch"],
    cmd_help={
        "help": "Xvideo Searcher",
        "example": "{ch}xsearch query",
    },
)

async def xvidsearch(client, message):
    editer= await edit_or_reply(message, "`Please Wait.....`")
    msg = get_text(message)
    if not msg:
            await editer.edit("`Please Enter Valid Input`")
            return
    try:
        qu = msg.replace(" ","+")
        page= requests.get(f"https://www.xvideos.com/?k={qu}").content
        soup = bs4.BeautifulSoup(page, 'html.parser')
        col= soup.findAll("div",{"class":"thumb"})

        links= ""

        for i in col:
            a = i.find("a")
            link = a.get('href')

            semd = link.split("/")[2]

            links += f"<a href='https://www.xvideos.com{link}'>• {semd.upper()}</a>\n"
        await editer.edit(links,parse_mode="HTML")


    except:
         await editer.edit("Something Went Wrong")
