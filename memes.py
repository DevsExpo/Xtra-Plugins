import random
from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
import asyncio

SLAP_TEMPLATES = [
    "{user1} {hits} {user2} with a {item}.",
    "{user1} {hits} {user2} in the face with a {item}.",
    "{user1} {hits} {user2} around a bit with a {item}.",
    "{user1} {throws} a {item} at {user2}.",
    "{user1} grabs a {item} and {throws} it at {user2}'s face.",
    "{user1} launches a {item} in {user2}'s general direction.",
    "{user1} starts slapping {user2} silly with a {item}.",
    "{user1} pins {user2} down and repeatedly {hits} them with a {item}.",
    "{user1} grabs up a {item} and {hits} {user2} with it.",
    "{user1} ties {user2} to a chair and {throws} a {item} at them.",
    "{user1} gave a friendly push to help {user2} learn to swim in lava."
]

ITEMS = [
    "cast iron skillet",
    "large trout",
    "baseball bat",
    "cricket bat",
    "wooden cane",
    "nail",
    "printer",
    "shovel",
    "CRT monitor",
    "physics textbook",
    "toaster",
    "portrait of Richard Stallman",
    "television",
    "five ton truck",
    "roll of duct tape",
    "book",
    "laptop",
    "old television",
    "sack of rocks",
    "rainbow trout",
    "rubber chicken",
    "spiked bat",
    "fire extinguisher",
    "heavy rock",
    "chunk of dirt",
    "beehive",
    "piece of rotten meat",
    "bear",
    "ton of bricks",
]

THROW = [
    "throws",
    "flings",
    "chucks",
    "hurls",
]

HIT = [
    "hits",
    "whacks",
    "slaps",
    "smacks",
    "bashes",
]

INSULT_STRINGS = [
    "`Owww ... Such a stupid idiot.`",
    "`Don't drink and type.`",
    "`Command not found. Just like your brain.`",
    "`Bot rule 420 section 69 prevents me from replying to stupid nubfuks like you.`",
    "`Sorry, we do not sell brains.`",
    "`Believe me you are not normal.`",
    "`I bet your brain feels as good as new, seeing that you never use it.`",
    "`If I wanted to kill myself I'd climb your ego and jump to your IQ.`",
    "`You didn't evolve from apes, they evolved from you.`",
    "`What language are you speaking? Cause it sounds like bullshit.`",
    "`You are proof that evolution CAN go in reverse.`",
    "`I would ask you how old you are but I know you can't count that high.`",
    "`As an outsider, what do you think of the human race?`",
    "`Ordinarily people live and learn. You just live.`",
    "`Keep talking, someday you'll say something intelligent!.......(I doubt it though)`",
    "`Everyone has the right to be stupid but you are abusing the privilege.`",
    "`I'm sorry I hurt your feelings when I called you stupid. I thought you already knew that.`",
    "`You should try tasting cyanide.`",
    "`You should try sleeping forever.`",
    "`Sharam kar bsdwale,kitni bkchodi deta.`",
    "`Chup Madarhox, bilkul chup..`",
    "`Me zindagi me chunotiyo se jyda inn jese Chutiyo se pareshaan hu.`",
    "`Pick up a gun and shoot yourself.`",
    "`Try bathing with Hydrochloric Acid instead of water.`",
    "`Go Green! Stop inhaling Oxygen.`",
    "`God was searching for you. You should leave to meet him.`",
    "`You should Volunteer for target in an firing range.`",
    "`Try playing catch and throw with RDX its fun.`",
    "`Jaana chodu chad jake land chaat`",
    "`Yaar ajab tere nkhare,gazab tera style hain, gand dhone ki tameez nahi, haath main mobile hai`",
    "`People like you are the reason we have middle fingers.`",
    "`When your mom dropped you off at the school, she got a ticket for littering.`",
    "`You’re so ugly that when you cry, the tears roll down the back of your head…just to avoid your face.`",
    "`If you’re talking behind my back then you’re in a perfect position to kiss my a**!.`",
]



def gen_random_slap(user1, user2):
    temp = random.choice(SLAP_TEMPLATES)
    item = random.choice(ITEMS)
    hit = random.choice(HIT)
    throw = random.choice(THROW)
    return temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw)


@friday_on_cmd(
    ["slap"],
    cmd_help={
        "help": "Slap Replied User",
        "example": "{ch}slap (replying to user)",
    })
async def slap_hard(client, message):
    msg_ = await edit_or_reply(message, "Giving Him A Slap.")
    if not message.reply_to_message:
        await msg_.edit("Reply To User To Give Him A Slap.")
        return 
    if not message.reply_to_message.from_user:
        await msg_.edit("Reply To User To Give Him A Slap.")
        return 
    if message.reply_to_message.from_user.id == message.from_user.id:
        return await msg_.edit("Wow Teach Me To Slap Myself.")
    slap_ = gen_random_slap(message.from_user.mention, message.reply_to_message.from_user.mention)
    await msg_.edit(slap_)

@friday_on_cmd(
    ["insult"],
    cmd_help={
        "help": "Insult A User",
        "example": "{ch}insult (replying to user)",
    })
async def insult_hard(client, message):
    msg_ = await edit_or_reply(message, "`Insult Incoming.`")
    insult_ = random.choice(INSULT_STRINGS)
    await msg_.edit(insult_)


@friday_on_cmd(
    ["lmgtf"],
    cmd_help={
        "help": "Let me Google that for you.",
        "example": "{ch}lmgtf hello world",
    })
async def lmgtfm(client, message):
    query = get_text(message)
    query = query.replace(" ", "+")
    url = f"https://letmegooglethat.com/?q={query}"
    await edit_or_reply(message, f"I have Google That For [You]({url}) .")


@friday_on_cmd(
    ["type"],
    cmd_help={
        "help": "Type Like You Are Typing IN A Key board",
        "example": "{ch}type hello world",
    })
async def type_my_ass(client, msg):
    typew = await edit_or_reply(msg, "`Typing..`")
    message = get_text(msg)
    if not message:
        await typew.edit("`Give Something To Type.`")
        return
    await client.send_chat_action(msg.chat.id, "typing")
    sleep_time = 0.03
    typing_symbol = "|"
    old_text = ""
    await typew.edit(typing_symbol)
    await asyncio.sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await asyncio.sleep(sleep_time)
        await typew.edit(old_text)
        await asyncio.sleep(sleep_time)
    await client.send_chat_action(msg.chat.id, "cancel")
