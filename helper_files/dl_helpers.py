"""
Generates Direct Link From Mega Public Url
Kanged From mega.py
"""

import json
import re
import json
import base64
import struct
from Crypto.Cipher import AES
import aiohttp
import asyncio
import random
import codecs

def aes_cbc_decrypt(data, key):
    aes_cipher = AES.new(key, AES.MODE_CBC, codecs.latin_1_encode('\0' * 16)[0])
    return aes_cipher.decrypt(data)

def decrypt_attr(attr, key):
    attr = aes_cbc_decrypt(attr, a32_to_str(key))
    attr = codecs.latin_1_decode(attr)[0]
    attr = attr.rstrip('\0')
    return json.loads(attr[4:]) if attr[:6] == 'MEGA{"' else False

def a32_to_str(a):
    return struct.pack('>%dI' % len(a), *a)

def str_to_a32(b):
    if isinstance(b, str):
        b = codecs.latin_1_encode(b)[0]
    if len(b) % 4:
        b += b'\0' * (4 - len(b) % 4)
    return struct.unpack('>%dI' % (len(b) / 4), b)

def base64_url_decode(data):
    data += '=='[(2 - len(data) * 3) % 4:]
    for search, replace in (('-', '+'), ('_', '/'), (',', '')):
        data = data.replace(search, replace)
    return base64.b64decode(data)

def base64_to_a32(s):
    return str_to_a32(base64_url_decode(s))

def parse_url(url):
        if '/file/' in url:
            url = url.replace(' ', '')
            file_id = re.findall(r'\W\w\w\w\w\w\w\w\w\W', url)[0][1:-1]
            id_index = re.search(file_id, url).end()
            key = url[id_index + 1:]
            return f'{file_id}!{key}'
        elif '!' in url:
            match = re.findall(r'/#!(.*)', url)
            path = match[0]
            return path
        else:
            return None

async def download_file(url):
        path = parse_url(url).split('!')
        if path == None:
            return None, None, None
        file_handle = path[0]
        file_key = path[1]
        file_key = base64_to_a32(file_key)
        file_data = await api_request({
                    'a': 'g',
                    'g': 1,
                    'p': file_handle
                })
        k = (file_key[0] ^ file_key[4], file_key[1] ^ file_key[5],
                 file_key[2] ^ file_key[6], file_key[3] ^ file_key[7])
        if 'g' not in file_data:
            return None, None, None
        file_url = file_data['g']
        file_size = file_data['s']
        attribs = base64_url_decode(file_data['at'])
        attribs = decrypt_attr(attribs, k)
        file_name = attribs['n']
        return file_name,file_size, file_url

async def api_request(data):
    sequence_num = random.randint(0, 0xFFFFFFFF)
    if not isinstance(data, list):
        data = [data]
    url = f'https://g.api.mega.co.nz/cs'
    params = {'id': sequence_num}
    async with aiohttp.ClientSession() as session:
        response = await session.post(url, data=json.dumps(data), params=params)
    json_resp = await response.json()
    return json_resp[0]

def find_between(start_string, end_string, to_find):
    _to_ = f"{start_string}(.*?){end_string}"
    result = re.search(_to_, to_find)
    if not result:
        return None
    return result.group(1)
   
