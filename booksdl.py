import os
import random
import re
import time

import requests
import wget
from bs4 import BeautifulSoup
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text

cxc = [
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
]



@friday_on_cmd(
    ["booklinks", "books"],
    is_official=False,
    cmd_help={
        "help": "Gathers All The Book Download links!",
        "example": "{ch}booklinks (book name)",
    },
)
async def bookdl(client, message):
    pablo = await edit_or_reply(message, "`Please Wait!`")
    book = get_text(message)
    if not book:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    lin = "https://b-ok.cc/s/"
    text = book
    link = lin + text

    headers = [
        "User-Agent",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0",
    ]
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    f = open("book.txt", "w")
    total = soup.find(class_="totalCounter")
    for nb in total.descendants:
        nbx = nb.replace("(", "").replace(")", "")
    if nbx == "0":
        await pablo.edit("No Books Found with that name.")
    else:
        lool = 0
        for tr in soup.find_all("td"):
            for td in tr.find_all("h3"):
                for ts in td.find_all("a"):
                    title = ts.get_text()
                    lool + 1
                for ts in td.find_all("a", attrs={"href": re.compile("^/book/")}):
                    ref = ts.get("href")
                    link = "https://b-ok.cc" + ref

                f.write("\n" + title)
                f.write("\nBook link:- " + link + "\n\n")

        f.write("By Friday.")
        f.close()
        caption = "By Friday.\n Get Your Friday From @FRIDAYCHAT"

        await client.send_document(
            message.chat.id,
            document=open("book.txt", "rb"),
            caption=f"**BOOKS LINKS GATHERED SUCCESSFULLY!\n\nBY FRIDAY. GET YOUR OWN FRIDAY FROM @FRIDAYCHAT.**",
        )
        os.remove("book.txt")
        await pablo.delete()
