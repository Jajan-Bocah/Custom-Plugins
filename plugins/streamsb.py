import os
import random
import asyncio
from re import match
from urllib.parse import quote_plus

import aiofiles
from selenium import webdriver

from userge import userge, Message, Config

@userge.on_cmd("ssb (?:(-hd)?\\s?(.+))", about={
    'header': "streamSB Direct Link",
    'flags': {'-hd': "High Quality"},
    'usage': "{tr}ssb [streamSB Link]",
    'examples': "{tr}ssb https://streamsb.net/d/rwqj5qwer2sl.html"}, del_pre=True)
async def stsb_dl(message: Message):
    if Config.GOOGLE_CHROME_BIN is None:
        await message.err("need to install Google Chrome. Module Stopping")
        return
    url = message.matches[0].group(2)
    hade = message.matches[0].group(1) == "-hd"
    #link_match = match(r'https://streamsb.net/d/.*\.html', url)
    #if not match:
    #    await message.err("Invalid URL: " + str(url))
    #    return
    await message.edit("`Processing ...`")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = Config.GOOGLE_CHROME_BIN
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    try:
        driver.get(url)
        await asyncio.sleep(0.5)
        if hade == True:
            driver.find_element_by_xpath("//a[contains(text(),'High quality')]").click()
        else:
            driver.find_element_by_xpath("//a[contains(text(),'Normal quality')]").click()
        await asyncio.sleep(1)
        site = driver.find_element_by_xpath("//a[contains(text(),'Direct Download')]")
        dl = site.get_attribute('href')
        await message.edit(f"**Original** : {url}\n"
                        f"`.download {dl}`",
                        disable_web_page_preview=True)
    except Exception as e:
        await message.edit(str(e), disable_web_page_preview=True, del_in=3)
    driver.quit()
