import requests
from bs4 import BeautifulSoup
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


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
        soup = BeautifulSoup(page, 'html.parser')
        col = soup.findAll("div",{"class":"thumb"})
        links = ""
        for i in col:
            a = i.find("a")
            link = a.get('href')

            semd = link.split("/")[2]

            links += f"<a href='https://www.xvideos.com{link}'>• {semd.upper()}</a>\n"
        await editer.edit(links,parse_mode="HTML")
    except:
         await editer.edit("`Something Went Wrong!`")
