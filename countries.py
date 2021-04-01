# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
import flag
import html
from countryinfo import CountryInfo



@friday_on_cmd(
    ["country", "Countries"],
    is_official=False,
    cmd_help={
        "help": "Get Information About Any Country",
        "example": "{ch}country India",
    },
)
async def country(client, message):
    pablo09 = await edit_or_reply(message, "`Searching For Country.....`")
    lol = get_text(message)
    if not lol:
        await pablo09.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    
    country = CountryInfo(lol)
    try:
	    a = country.info()
    except:
	    await event.edit("Country Not Avaiable Currently")
    name = a.get("name")
    bb= a.get("altSpellings")
    hu = ''
    for p in bb:
    	hu += p+",  "
	
    area = a.get("area")
    borders = ""
    hell = a.get("borders")
    for fk in hell:
	    borders += fk+",  "
	
    call = "" 
    WhAt = a.get("callingCodes")
    for what in WhAt:
	    call+= what+"  "
	
    capital = a.get("capital")
    currencies = ""
    fker = a.get("currencies")
    for FKer in fker:
	    currencies += FKer+",  "

    HmM = a.get("demonym")
    geo = a.get("geoJSON")
    pablo = geo.get("features")
    Pablo = pablo[0]
    PAblo = Pablo.get("geometry")
    EsCoBaR= PAblo.get("type")
    iso = ""
    iSo = a.get("ISO")
    for hitler in iSo:
      po = iSo.get(hitler)
      iso += po+",  "
    fla = iSo.get("alpha2")
    nox = fla.upper()
    okie = flag.flag(nox)

    languages = a.get("languages")
    lMAO=""
    for lmao in languages:
	    lMAO += lmao+",  "

    nonive = a.get("nativeName")
    waste = a.get("population")
    reg = a.get("region")
    sub = a.get("subregion")
    tik = a.get("timezones")
    tom =""
    for jerry in tik:
	    tom+=jerry+",   "

    GOT = a.get("tld")
    lanester = ""
    for targaryen in GOT:
	    lanester+=targaryen+",   "

    wiki = a.get("wiki")

    caption = f"""<b><u>information gathered successfully</b></u>
<b>
Country Name:- {name}
Alternative Spellings:- {hu}
Country Area:- {area} square kilometers
Borders:- {borders}
Calling Codes:- {call}
Country's Capital:- {capital}
Country's currency:- {currencies}
Country's Flag:- {okie}
Demonym:- {HmM}
Country Type:- {EsCoBaR}
ISO Names:- {iso}
Languages:- {lMAO}
Native Name:- {nonive}
population:- {waste}
Region:- {reg}
Sub Region:- {sub}
Time Zones:- {tom}
Top Level Domain:- {lanester}
wikipedia:- {wiki}</b>
<u><b>
Information Gathered By Friday.
Get Your Own Friday From @FRIDAYCHAT.</b></u>
"""
    await pablo09.edit(caption, parse_mode="html")
