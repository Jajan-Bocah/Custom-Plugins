#!/usr/bin/env python3
# https://github.com/Sorrow446/ZS-DL
# plugin by @aryanvikash
"""Zippyshare Direct Link Generator"""

import asyncio
import urllib.parse
from pathlib import Path
from selenium import webdriver

from userge import userge, Message
from userge.utils.exceptions import ProcessCanceled
from ..upload import upload_path
from ..download import url_download

from .. import zzippyshare

@userge.on_cmd("zipp", about={
    'header': "generate Direct link of zippyshare url",
    'flags': {
        '-dl': "download to server",
        '-t': "upload to telegram",
        '-d': "upload as document",
        '-wt': "without thumb",
        '-df': "don't forward to log channel"},
    'usage': "{tr}zipp [flags] [Zippyshare Link ]",
    'examples': [
        "{tr}zipp https://www10.zippyshare.com/v/dyh988sh/file.html",
        "{tr}zipp -u https://www10.zippyshare.com/v/dyh988sh/file.html"]}, del_pre=True)
async def jipiser(message: Message):
    """ zippy to direct """
    if zzippyshare.GOOGLE_CHROME_BIN is None:
        await message.err("need to install Google Chrome. Module Stopping")
        return

    url = message.filtered_input_str
    if not url:
        await message.err("Input not foud!")
        return

    await message.edit("`Generating url ....`")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = zzippyshare.GOOGLE_CHROME_BIN
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    await asyncio.sleep(1)
    try:
        driver.get(url)
        await asyncio.sleep(1)
        button = driver.find_element_by_xpath('//a[@id="dlbutton"]')
        direct_url = urllib.parse.unquote(button.get_attribute('href'))
        fname = direct_url.split("/")[-1]

        if 't' in message.flags or 'd' in message.flags or 'dl' in message.flags:
            try:
                direct_url, d_in = await url_download(message, direct_url)
            except ProcessCanceled:
                await message.canceled()
                driver.quit()
                return
            except Exception as e_e:  # pylint: disable=broad-except
                await message.err(str(e_e))
                driver.quit()
                return
            
            try:
                string = Path(direct_url)
            except IndexError:
                await message.err("wrong syntax")
            else:
                await message.delete()
                with message.cancel_callback():
                    if 'dl' in message.flags:
                        await message.edit(f"Downloaded to `{string}` in {d_in} seconds")
                    else:
                        await upload_path(message, string, True)
        else:
            await message.edit(f"**{fname}**\n"
                           f"`.download {direct_url}`",
                           disable_web_page_preview=True)
    except Exception as z_e:  # pylint: disable=broad-except
        await message.edit(f"`{z_e}`")
    driver.quit()
