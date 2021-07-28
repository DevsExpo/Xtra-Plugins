# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import requests
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["pokedex", "pokemon"],
    is_official=False,
    cmd_help={
        "help": "Get Details About Pokémon!",
        "example": "{ch}pokedex (Pokemon name)",
    },
)
async def pokedex(client, message):
    pablo = await edit_or_reply(message, "`Searching For Pokémon.....`")
    sgname = get_text(message)
    if not sgname:
        await pablo.edit("`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`")
        return
    url = f"https://starkapis.herokuapp.com/pokedex/{sgname}"
    r = requests.get(url).json()
    pokemon = r
    if pokemon.get("error") is not None:
        kk = f"""
Error:   {pokemon.get("error")}"""
        await pablo.edit(kk)
        return
    name = str(pokemon.get("name"))
    number = str(pokemon.get("number"))
    species = str(pokemon.get("species"))
    typo = pokemon.get("types")
    types = "".join(str(tu) + ",  " for tu in typo)
    lol = pokemon.get("abilities")
    lmao = lol.get("normal")
    ok = ""
    for ty in lmao:
        ok = str(ty) + ",  "

    kk = lol.get("hidden")
    hm = "".join(str(pq) + ",  " for pq in kk)
    hell = pokemon.get("eggGroups")
    uio = "".join(str(x) + ",  " for x in hell)
    height = pokemon.get("height")
    weight = pokemon.get("weight")
    yes = pokemon.get("family")
    Id = str(yes.get("id"))
    evo = str(yes.get("evolutionStage"))
    pol = yes.get("evolutionLine")
    xy = "".join(str(p) + ",  " for p in pol)
    start = pokemon.get("starter")
    start = "No" if not start else "True"
    leg = pokemon.get("legendary")

    leg = "No" if not leg else "True"
    myt = pokemon.get("mythical")
    myt = "No" if not myt else "True"
    ultra = pokemon.get("ultraBeast")

    ultra = "No" if not ultra else "True"
    megA = pokemon.get("mega")

    megA = "No" if not megA else "True"
    gEn = pokemon.get("gen")
    link = pokemon.get("sprite")
    des = pokemon.get("description")
    caption = f"<b><u>Pokemon Information Gathered Successfully</b></u>\n\n\n<b>Name:-   {name}\nNumber:-  {number}\nSpecies:- {species}\nType:- {types}\n\n<u>Abilities</u>\nNormal Abilities:- {ok}\nHidden Abilities:- {hm}\nEgg Group:-  {uio}\nHeight:- {height}\nWeight:- {weight}\n\n<u>Family</u>\nID:- {Id}\nEvolution Stage:- {evo}\nEvolution Line:- {xy}\nStarter:- {start}\nLegendary:- {leg}\nMythical:- {myt}\nUltra Beast:- {ultra}\nMega:- {megA}\nGen:-  {gEn}\nDescription:-  {des}</b>"

    await client.send_photo(
        message.chat.id,
        photo=link,
        caption=caption,
        parse_mode="HTML",
    )
    await pablo.delete()
