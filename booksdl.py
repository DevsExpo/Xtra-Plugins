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
    ["booksdl", "bookdl"],
    is_official=False,
    cmd_help={
        "help": "Downloads Books Just with name!",
        "example": "{ch}booksdl (book name)",
    },
)
async def bookdl(client, message):
    pablo = await edit_or_reply(message, "`Please Wait!`")
    book = get_text(message)
    if not book:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    c_time = time.time()
    h = {"user-agent": random.choice(cxc)}
    input = book
    r = requests.get(f"https://1lib.in/s/{input}", headers=h)
    soup = BeautifulSoup(r.content, "html5lib")
    mydivs = soup.find_all("div", {"id": "searchResultBox"})
    mydivs = mydivs[0]
    Kk = mydivs.find_all(href=True)
    try:
        L = Kk[0]["href"]
    except BaseException:
        await pablo.edit("`Book Not Found.`")
        return
    lemk = "https://1lib.in" + L
    r = requests.get(lemk, headers=h)
    soup = BeautifulSoup(r.content, "html5lib")
    images = soup.findAll("img")
    imaeo = images[0]["src"]
    
    try:
        imae = wget.download(imaeo)
    except BaseException:
        imae = wget.download("https://telegra.ph/file/22535f8051a58af113586.jpg")
    mydivs = soup.find_all("div", {"class": "bcNav"})
    lol = mydivs[0]
    lo0 = lol.text.strip()
    titl = lol.find_all("a")[0].text
    TTL = lo0.replace(titl, "")
    nme = TTL.strip()
    caption = f"""
    Title : {TTL.strip()},\n
        """
    try:
        mydivs = soup.find_all("div", {"id": "bookDescriptionBox"})
        caption += f"Description : {mydivs[0].text.strip()}"
    except BaseException:
        pass
    try:
        mydivs = soup.find_all("div", {"class": "bookProperty property_categories"})
        catse = mydivs[0]
        case = catse.find_all("div", {"class": "property_label"})
        lol = case[0].text
        case0 = catse.find_all("div", {"class": "property_value"})
        lolo = case0[0].text
        caption += f"{lol} : {lolo}\n\n"
    except BaseException:
        pass
    try:
        mydivs = soup.find_all("div", {"class": "bookProperty property_volume"})
        catse = mydivs[0]
        case = catse.find_all("div", {"class": "property_label"})
        lol = case[0].text
        case0 = catse.find_all("div", {"class": "property_value"})
        lolo = case0[0].text
        caption += f"{lol} : {lolo}\n\n"
    except BaseException:
        pass
    try:
        mydivs = soup.find_all("div", {"class": "bookProperty property_year"})
        catse = mydivs[0]
        case = catse.find_all("div", {"class": "property_label"})
        lol = case[0].text
        case0 = catse.find_all("div", {"class": "property_value"})
        lolo = case0[0].text
        caption += f"{lol} : {lolo}\n\n"
    except BaseException:
        pass
    try:
        mydivs = soup.find_all("div", {"class": "bookProperty property_language"})
        catse = mydivs[0]
        case = catse.find_all("div", {"class": "property_label"})
        lol = case[0].text
        case0 = catse.find_all("div", {"class": "property_value"})
        lolo = case0[0].text
        caption += f"{lol} : {lolo}\n\n"
    except BaseException:
        pass
    try:
        mydivs = soup.find_all("div", {"class": "bookProperty property_pages"})
        catse = mydivs[0]
        case = catse.find_all("div", {"class": "property_label"})
        lol = case[0].text
        case0 = catse.find_all("div", {"class": "property_value"})
        lolo = case0[0].text
        caption += f"{lol} : {lolo}\n\n"
    except BaseException:
        pass
    mydivs = soup.find_all("a", {"class": "btn btn-primary dlButton addDownloadedBook"})
    dl = "https://1lib.in" + mydivs[0]["href"]
    if "epub" in mydivs[0].text.lower():
        ext = "epub"
    elif "azw3" in mydivs[0].text.lower():
        ext = "azw3"
    else:
        ext = "pdf"
    flnl = f"{nme}.{ext}"
    h = requests.get(dl, headers=h)
    open(flnl, "wb").write(h.content)
    e_time = time.time()
    hmm_time = round(e_time - c_time)
    caption += f"Time Taken : {hmm_time} seconds"
    try:
        await client.send_document(
            message.chat.id, caption=caption, document=open(flnl, "rb"), thumb=imae
        )
    except BaseException:
        caption = f"""
Title : {TTL.strip()}
"""
        caption += f"Time Taken : {hmm_time} Seconds"
        await client.send_document(
            message.chat.id, caption=caption, document=open(flnl, "rb"), thumb=imae
        )
    await pablo.delete()
    os.remove(flnl)


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
