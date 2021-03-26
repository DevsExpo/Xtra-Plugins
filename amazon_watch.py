import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bs4 import BeautifulSoup
from main_startup import Friday
from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from xtraplugins.dB.amazon_price_tracker_db import (
    add_amazon_tracker,
    get_all_amazon_trackers,
    is_amazon_tracker_in_db,
    rmamazon_tracker,
)


@friday_on_cmd(
    ["atl", "amazontrack"],
    is_official=False,
    cmd_help={
        "help": "Add Amazon Product To Tracking List!",
        "example": "{ch}atl (amazon-url)",
    },
)
async def add_to_db(client, message):
    aurl = await edit_or_reply(message, "`Processing..`")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    url = get_text(message)
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        title = soup.find(id="productTitle").get_text()
        price = soup.find(id="priceblock_ourprice").get_text()
        title = title.strip()
        price = price[2:].split(",")
    except BaseException:
        await aurl.edit("`Url is Invalid!`")
        return
    price = round(float("".join(price)))
    if is_amazon_tracker_in_db(str(url)):
        await aurl.edit("`Tracker Already Found In DB. Whats Point in Adding Again?`")
        return
    add_amazon_tracker(url, price)
    await aurl.edit(
        f"**Added To TrackList** \n**Title :** `{title}` \n**Price :** `{price}`"
    )


@friday_on_cmd(
    ["rmlt", "rmamazontrack"],
    is_official=False,
    cmd_help={
        "help": "Remove Amazon Product From Tracking List!",
        "example": "{ch}rmlt (amazon-url)",
    },
)
async def rm_from_db(client, message):
    rmurl = await edit_or_reply(message, "`Processing..`")
    url = get_text(message)
    if not is_amazon_tracker_in_db(str(url)):
        await rmurl.edit("`This Url Was Not Found In My DB!`")
        return
    rmamazon_tracker(str(url))
    await rmurl.edit("`Removed This Product From DB!`")
    return


async def track_amazon():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    kk = get_all_amazon_trackers()
    
    if len(kk) == 0:
        return
    for ujwal in kk:
        page = requests.get(ujwal["amazon_link"], headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        title = soup.find(id="productTitle").get_text()
        price = soup.find(id="priceblock_ourprice").get_text()
        title = title.strip()
        price = price[2:].split(",")
        price = round(float("".join(price)))
        if int(price) > int(ujwal["price"]):
            await Friday.send_message(
                Config.LOG_GRP,
                f"#Tracker - Price Reduced \nProduct Name : {title} \nCurrent price : {price}",
            )
            rmamazon_tracker(str(ujwal["amazon_link"]))
        else:
            pass


scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(track_amazon, trigger="cron", hour=13, minute=35)
scheduler.start()
