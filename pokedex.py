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
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    url = f"https://starkapi.herokuapp.com/pokedex/{sgname}"
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
    if not start:
        start = "No"
    elif start:
        start = "True"
    else:
        pass

    leg = pokemon.get("legendary")

    if not leg:
        leg = "No"
    elif leg:
        leg = "True"
    else:
        pass

    myt = pokemon.get("mythical")
    if not myt:
        myt = "No"
    elif myt:
        myt = "True"
    else:
        pass
    ultra = pokemon.get("ultraBeast")

    if not ultra:
        ultra = "No"
    elif ultra:
        ultra = "True"
    else:
        pass

    megA = pokemon.get("mega")

    if not megA:
        megA = "No"
    elif megA:
        megA = "True"
    else:
        pass

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
