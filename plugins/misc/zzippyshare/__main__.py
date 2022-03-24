#!/usr/bin/env python3
# https://github.com/Sorrow446/ZS-DL
# plugin by @aryanvikash
"""Zippyshare Direct Link Generator"""

import urllib.parse
import asyncio
from selenium import webdriver
from userge import userge, Message, config


from .. import zzippyshare

@userge.on_cmd("zipp", about={
    'header': "generate Direct link of zippyshare url",
    'usage': "{tr}zipp : [Zippyshare Link ]",
    'examples': "{tr}zipp https://www10.zippyshare.com/v/dyh988sh/file.html"}, del_pre=True)
async def jipiser(message: Message):
    """ zippy to direct """
    if zzippyshare.GOOGLE_CHROME_BIN is None:
        await message.err("need to install Google Chrome. Module Stopping")
        return
    url = message.input_str
    await message.edit("`Generating url ....`")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = zzippyshare.GOOGLE_CHROME_BIN
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    try:
        driver.get(url)
        await asyncio.sleep(1)
        button = driver.find_element_by_xpath('//a[@id="dlbutton"]')
        direct_url = urllib.parse.unquote(button.get_attribute('href'))
        fname = direct_url.split("/")[-1]
        await message.edit(f"**{fname}**\n"
                           f"`.download {direct_url}`",
                           disable_web_page_preview=True)
    except Exception as z_e:  # pylint: disable=broad-except
        await message.edit(f"`{z_e}`")
    driver.quit()

