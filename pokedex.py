import requests

from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_readable_time, delete_or_pass, progress, get_text
import asyncio
import math
import time
from pyrogram import filters
from main_startup.config_var import Config


@friday_on_cmd(["pokedex", "pokemon"], 
cmd_help = {
               'help': 'Get Details About Pokémon!',
               'example': '{ch}pokedex (Pokemon name)'
               },)
async def pokedex(client, message):
    pablo = await edit_or_reply(message, "`Searching For Pokémon.....`")
    sgname = get_text(message)
    if not sgname:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    url = f"https://starkapi.herokuapp.com/pokedex/{sgname}"
    r = requests.get(url).json()
    pokemon = r
    if pokemon.get("error") is not None:
          kk = f"""
Error:   {pokemon.get("error")}"""
          ommhg = await pablo.edit(kk)
          return
    name = str(pokemon.get("name"))
    number = str(pokemon.get("number"))
    species = str(pokemon.get("species"))
    typo = pokemon.get("types")
    types = ""
    for tu in typo:
        types += str(tu) + ",  "

    lol = pokemon.get("abilities")
    lmao = lol.get("normal")
    ok = ""
    for ty in lmao:
        ok = str(ty) + ",  "

    kk = lol.get("hidden")
    hm = ""
    for pq in kk:
        hm += str(pq) + ",  "
    hell = pokemon.get("eggGroups")
    uio = ""
    for x in hell:
        uio += str(x) + ",  "

    height = pokemon.get("height")
    weight = pokemon.get("weight")
    yes = pokemon.get("family")
    Id = str(yes.get("id"))
    evo = str(yes.get("evolutionStage"))
    pol = yes.get("evolutionLine")
    xy = ""
    for p in pol:
        xy += str(p) + ",  "

    start = pokemon.get("starter")
    if start == False:
        start = "No"
    elif start == True:
        start = "True"
    else:
        pass

    leg = pokemon.get("legendary")

    if leg == False:
        leg = "No"
    elif leg == True:
        leg = "True"
    else:
        pass

    myt = pokemon.get("mythical")
    if myt == False:
        myt = "No"
    elif myt == True:
        myt = "True"
    else:
        pass
    ultra = pokemon.get("ultraBeast")

    if ultra == False:
        ultra = "No"
    elif ultra == True:
        ultra = "True"
    else:
        pass

    megA = pokemon.get("mega")

    if megA == False:
        megA = "No"
    elif megA == True:
        megA = "True"
    else:
        pass

    gEn = pokemon.get("gen")
    link = pokemon.get("sprite")
    des = pokemon.get("description")
    caption = f"<b><u>Pokemon Information Gathered Successfully</b></u>\n\n\n<b>Name:-   {name}\nNumber:-  {number}\nSpecies:- {species}\nType:- {types}\n\n<u>Abilities</u>\nNormal Abilities:- {ok}\nHidden Abilities:- {hm}\nEgg Group:-  {uio}\nHeight:- {height}\nWeight:- {weight}\n\n<u>Family</u>\nID:- {Id}\nEvolution Stage:- {evo}\nEvolution Line:- {xy}\nStarter:- {start}\nLegendary:- {leg}\nMythical:- {myt}\nUltra Beast:- {ultra}\nMega:- {megA}\nGen:-  {gEn}\nDescription:-  {des}</b>"

    await client.send_photo(
        message.chat.id,
        photo = link,
        caption = caption,
        parse_mode="HTML",
    )
    await pablo.delete()


