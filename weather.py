import requests
import xmltodict
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from bs4 import BeautifulSoup
from pyrogram import filters
from main_startup.core.decorators import friday_on_cmd


@friday_on_cmd(['weather1','climate','we','cl'],
               cmd_help={
                'help': 'Get Weather info of town or pincode',
                'example': '{ch}weather1 hyderabad'})
async def geW_if(client, message):
    m_ = await edit_or_reply(message, "`Please Wait!`")
    city = get_text(message)
    data='{"params":"aroundLatLngViaIP=true&hitsPerPage=15&language=en&query='+city+'&type=city"}'
    ses=requests.session()
    res=ses.post("https://places-dsn.algolia.net/1/places/query",data=data).json()
    cords=res["hits"][0]["_geoloc"]
    res=ses.get("https://1weather.onelouder.com/feeds/onelouder2/fm.php?LAT="+str(round(cords["lat"],2))+"&LON="+str(round(cords["lng"],2))+"&UNITS=all")
    data=xmltodict.parse(res.text)
    flag=True
    msg=""
    try:
        msg+="<b><u>INFORMATION GATHERED SUCCESSFULLY</b></u>\n\n"
        today=data["locations"]["location"]
        msg+=("<b>city:  </b> <code>"+today["@city"]+" ("+today["@country"]+")"+"</code>\n")
        details=today["sfc_ob"]
        msg+=("<b>temperature:  </b><code>"+details["temp_C"]+" c"+"</code>\n")
        msg+=("<b>apparent temp:  </b><code>"+details["apparent_temp_C"]+" c"+"</code>\n")
        msg+=("<b>Weather report:  </b><code>"+details["wx"]+"</code>\n")
        msg+=("<b>Wind Speed:  </b><code>"+str(details["wnd_spd_kph"])+"kmph ("+str(details["wnd_dir"])+")"+"</code>\n")
        msg+=("<b>Humidity:  <b><code>"+details["rh_pct"]+" %"+"</code>\n")
        flag=False
    except Exception:
        pass
    if flag:
        return await m_.edit("Information not found")
    return await m_.edit(msg)
