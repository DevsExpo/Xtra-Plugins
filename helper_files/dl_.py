

import re
import aiohttp
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from lxml import etree
from xtraplugins.helper_files.dl_helpers import api_request, find_between, base64_url_decode, decrypt_attr, base64_to_a32, parse_url 

class AnyDL:
    def __init__(self):
        self.dl_path = "./main_startup/downloads"
    
    async def mega_dl(self, url):
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
        return file_url, file_name, file_size
    
    async def media_fire_dl(self, media_fire_url):
        ua = UserAgent()
        user_agent = ua.random
        headers = {"User-Agent": user_agent}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(media_fire_url) as resp:
                if resp.status != 200:
                    return resp.status
                b_ = BeautifulSoup(await resp.read(), 'html.parser')
                dom = etree.HTML(str(b_))
                file_url = dom.xpath('//*[@id="downloadButton"]')[0].get("href")
                file_name = dom.xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div[1]/div[1]')[0].text
                file_size = dom.xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/ul/li[1]/span')[0].text
                file_uploaded_date = dom.xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/ul/li[2]/span')[0].text
                caption_ = dom.xpath('/html/body/div[1]/div[1]/div[6]/div[1]/div[1]/div[3]/p')[0].text
                scan_result = dom.xpath("/html/body/div[1]/div[1]/div[6]/div[1]/div[2]/div/div[2]/p/span")[0].text
            return file_url, file_name, file_size, file_uploaded_date, caption_, scan_result
            
    async def anon_files_dl(self, anon_url):
        ua = UserAgent()
        user_agent = ua.random
        headers = {"User-Agent": user_agent}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(anon_url) as resp:
                if resp.status != 200:
                    return resp.status
                b_ = BeautifulSoup(await resp.read(), 'lxml')
                file_url = b_.find("a", {"id": "download-url"}).get("href")
                file_name = b_.find("h1", {"class": "text-center text-wordwrap"}).text
                file_size = b_.find("a", {"id": "download-url"}).text
                file_size = find_between(r"\(", r"\)", file_size)
            return file_url, file_size, file_name
    
    