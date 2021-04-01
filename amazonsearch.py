import requests
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["amsearch"],
    cmd_help={
        "help": "Search Product From Amazon",
        "example": "{ch}amsearch Iphone",
    }
)

async def _(client,message):
    msgg = get_text(message)

    sedlife = await edit_or_reply(message, "```Searching Product..```")
    if not msgg:
        await sedlife.edit("`Dumb Give Me Input`")
        return

    product = ""
    r=requests.get(f"https://amznsearch.vercel.app/api/?query={msgg}").json()

    for products in r:
        link = products['productLink']
        name = products['productName']
        price= products['productPrice']
        product += f"<a href='{link}'>• {name}\n{price}</a>\n"

    await edit_or_reply(message,product,parse_mode="HTML")
