# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import re
import aiohttp
import base64
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from lxml import etree
from main_startup.helper_func.basic_helpers import run_in_exc
from xtraplugins.helper_files.dl_helpers import api_request, find_between, base64_url_decode, decrypt_attr, base64_to_a32, parse_url 

class AnyDL:
    def __init__(self):
        self.dl_path = "./main_startup/downloads"
       
    @run_in_exc
    def one_dl(self, url):
        data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
        dbs_ = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
        fina_url = f"https://api.onedrive.com/v1.0/shares/u!{dbs_}/root/content"
        return fina_url
    
    @run_in_exc
    def dropbox_dl(self, url):
        url = "https://dl.dropboxusercontent.com" + url.split("https://www.dropbox.com")[1]
        return url
                        
    @run_in_exc
    def gdrive(self, url):
        drive = 'https://drive.google.com'
        file_id = ''
        if url.find('view') != -1:
            file_id = url.split('/')[-2]
        elif url.find('open?id=') != -1:
            file_id = url.split('open?id=')[1].strip()
        elif url.find('uc?id=') != -1:
            file_id = url.split('uc?id=')[1].strip()
        if file_id == '':
            return None
        url = f'{drive}/uc?export=download&id={file_id}'
        download = requests.get(url, stream=True, allow_redirects=False)
        cookies = download.cookies
        dl_url = download.headers.get("location")
        if not dl_url:
            page = BeautifulSoup(download.content, 'lxml')
            export = drive + page.find('a', {'id': 'uc-download-url'}).get('href')
            name = page.find('span', {'class': 'uc-name-size'}).text
            response = requests.get(export, stream=True, allow_redirects=False, cookies=cookies)
            dl_url = response.headers['location']
        if 'accounts.google.com' in dl_url:
            return None
        return dl_url
    
    
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
                    return None
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
                    return None
                b_ = BeautifulSoup(await resp.read(), 'lxml')
                file_url = b_.find("a", {"id": "download-url"}).get("href")
                file_name = b_.find("h1", {"class": "text-center text-wordwrap"}).text
                file_size = b_.find("a", {"id": "download-url"}).text
                file_size = find_between(r"\(", r"\)", file_size)
            return file_url, file_size, file_name
    
    
