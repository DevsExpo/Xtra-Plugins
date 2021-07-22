import os
import time

import pyshorteners
import requests
from bs4 import BeautifulSoup
from faker import Faker
from faker.providers import internet

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import (
    delete_or_pass,
    edit_or_reply,
    get_text,
    progress,
)


@friday_on_cmd(
    ["fakegen", "fakedata"],
    cmd_help={"help": "Generate Random Fake Details", "example": "{ch}fakegen"},
)
async def gen_fake_details(client, message):
    lel = await edit_or_reply(message, "`Processing...`")
    fake = Faker()
    name = str(fake.name())
    fake.add_provider(internet)
    address = str(fake.address())
    ip = fake.ipv4_private()
    cc = fake.credit_card_full()
    email = fake.ascii_free_email()
    job = fake.job()
    android = fake.android_platform_token()
    pc = fake.chrome()
    await lel.edit(
        f"<b><u> Fake Information Generated</b></u>\n<b>Name :-</b><code>{name}</code>\n\n<b>Address:-</b><code>{address}</code>\n\n<b>IP ADDRESS:-</b><code>{ip}</code>\n\n<b>credit card:-</b><code>{cc}</code>\n\n<b>Email Id:-</b><code>{email}</code>\n\n<b>Job:-</b><code>{job}</code>\n\n<b>android user agent:-</b><code>{android}</code>\n\n<b>Pc user agent:-</b><code>{pc}</code>",
        parse_mode="HTML",
    )


@friday_on_cmd(
    ["short"],
    cmd_help={"help": "Shorten URL link!", "example": "{ch}short link"},
)
async def vom(client, message):
    event = await edit_or_reply(message, "`Shortening the link.....`")
    link = get_text(message)
    if not link:
        await event.edit(
            "``Please Give Me A Valid Input. You Can Check Help Menu To Know More!``"
        )
        return
    sed = pyshorteners.Shortener()
    kek = sed.dagd.short(link)
    bestisbest = (
        f"<b>Url Shortened</b> \n<b><u>Given Link</u></b> ➠ {link}\n"
        f"<b><u>Shortened Link</u></b> ➠ {kek}"
    )
    await event.edit(bestisbest)


@friday_on_cmd(
    ["rmeme", "randomeme"],
    cmd_help={"help": "Generate Random Memes!", "example": "{ch}rmeme"},
)
async def givemememe(client, message):
    hmm_s = "https://some-random-api.ml/meme"
    r = requests.get(url=hmm_s).json()
    image_s = r["image"]
    await message.reply_photo(image_s)
    await delete_or_pass(message)


@friday_on_cmd(
    ["binlookup", "bin"],
    cmd_help={"help": "Get Details About Bin!", "example": "{ch}bin (bin number)"},
)
async def nobin(client, message):
    stark_m = await edit_or_reply(message, "`Please Wait!`")
    bin = get_text(message)
    if not bin:
        await stark_m.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    url = f"https://lookup.binlist.net/{bin}"
    r = requests.get(url=url)
    if r.status_code != 200:
        await stark_m.edit("Invalid Bin, Please Give Me A Valid Bin To Check.")
        return
    jr = r.json()
    data_is = (
        f"<b><u>Bin</u></b> ➠ <code>{bin}</code> \n"
        f"<b><u>Type</u></b> ➠ <code>{jr.get('type', '?')}</code> \n"
        f"<b><u>Scheme</u></b> ➠ <code>{jr.get('scheme', '?')}</code> \n"
        f"<b><u>Brand</u></b> ➠ <code>{jr.get('brand', '?')}</code> \n"
        f"<b><u>Country</u></b> ➠ <code>{jr['country']['name']} {jr['country']['emoji']}</code> \n"
    )
    await stark_m.edit(data_is, parse_mode="html")


@friday_on_cmd(
    ["iban", "ibaninfo"],
    cmd_help={"help": "Get Details About IBAN", "example": "{ch}iban (iban here)"},
)
async def ibanbanem(client, message):
    stark_m = await edit_or_reply(message, "`Please Wait!`")
    iban = get_text(message)
    if not iban:
        await stark_m.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    api = f"https://openiban.com/validate/{iban}?getBIC=true&validateBankCode=true"
    r = requests.get(url=api).json()
    if r["valid"] is False:
        await stark_m.edit("Invalid IBAN, Try Again With A Valid IBAN!")
        return
    banks = r["bankData"]
    kek = (
        f"<b><u>VALID</u></b> ➠ <code>{r['valid']}</code> \n"
        f"<b><u>IBAN</u></b> ➠ <code>{r['iban']}</code> \n"
        f"<b><u>BANK-CODE</u></b> ➠ <code>{banks['bankCode']}</code> \n"
        f"<b><u>BANK-NAME</u></b> ➠ <code>{banks['name']}</code> \n"
        f"<b><u>ZIP</u></b> ➠ <code>{banks['zip']}</code> \n"
        f"<b><u>CITY</u></b> ➠ <code>{banks['city']}</code> \n"
        f"<b><u>BIC</u></b> ➠ <code>{banks['bic']}</code> \n"
    )
    await stark_m.edit(kek, parse_mode="html")