import aiohttp
import asyncio
import re
import random

my_code = {
    400: "『 Invalid Key 』",
    200: "『 Valid Key 』",
    69: "『 Only Testing Mode Enabled 』",
    498: "『 Key Expired 』"
}

async def check_stripe_key(key_: str):
    url = "https://api.stripe.com/v1/tokens"
    check_ = {
                'card[number]': 5154620061414478,
                'card[cvc]': random.randint(552, 99),
                'card[exp_month]': random.randint(1, 12),
                'card[exp_year]': random.randint(2022, 2026),
                'key': key_,
            }
    async with aiohttp.ClientSession() as session:
      async with session.post(url, params=check_) as resp:
          response_ = await resp.text()
    if stark_finder("invalid api key provided", response_):
        return 400
    elif stark_finder("api_key_expired", response_):
        return 498
    elif stark_finder("testmode_charges_only", response_):
        return 69
    elif stark_finder("test_mode_live_card", response_):
        return 69
    elif stark_finder("invalid_request_error", response_):
        return 400
    else:
        return 200
    
async def check_cc()
            
def stark_finder(to_find, from_find):
    if re.search(r"( |^|[^\w])" + re.escape(to_find) + r"( |$|[^\w])", from_find, flags=re.IGNORECASE):
        return True
    return False


async def cc_(cc_number, cvc, em, ey):
    stripe_key = Config.STRIPE_KEY
    url = "https://api.stripe.com/v1/payment_methods"
    header_s = {
'authority': 'api.stripe.com',
'method': 'POST',
'path': '/v1/payment_methods',
'scheme': 'https',
'accept': 'application/json',
'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6',
'content-type': 'application/x-www-form-urlencoded',
'origin': 'https://js.stripe.com',
'referer': 'https://js.stripe.com/',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-site',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    param_ = {
        'type': 'card',
        'billing_details[address][postal_code]': 10080,
        'billing_details[name]': 'Albert Rogers',
        'card[number]': cc_number,
        'card[cvc]': cvc,
        'card[exp_month]': em,
        'card[exp_year]': ey,
        'key': stripe_key
        
    }
    response_ = None
    async with aiohttp.ClientSession(headers=header_s) as session:
      async with session.post(url, params=param_) as resp:
          response_ = await resp.text()
    if not response_:
        return 422
    cvv_r = find_between('<input type="hidden" name="ssl_cvv2_response" value="', '"></td>', response_)
    avs_r = find_between('<input type="hidden" name="ssl_avs_response" value="', '"></td>', response_)
    msg_ = find_between('<span id="ssl_result_message">', '</span>', response_)
    return cvv_r, avs_r, msg_
    
    
def find_between(start_string, end_string, to_find):
    _to_ = f"{start_string}(.*?){end_string}"
    result = re.search(_to_, to_find)
    return result.group(1)

async def check_sk_key(client, message):
    msg = await edit_or_reply(message, "`Please Wait`")
    key_ = get_text(message)
    if not key_:
        return await msg.edit("`Give Me A Key To Check.`")
    key_result = await check_stripe_key(key_)
    _result_to_show = f"<b><u>Stripe Key Check Result</b></u> \n<b>Key :</b> <code>{key_}</code> \n<b>Response :</b> <code>{my_code[key_result]}</code> \n<b><u>Check Using FridayUB</b></u>"
    await msg.edit(_result_to_show)