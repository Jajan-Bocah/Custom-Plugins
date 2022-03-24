""" Change database name for Userge """

import os
import asyncio
from shutil import copyfile, rmtree

from userge import userge, Message
from userge.utils import runcmd

DB_NAME = os.environ.get("DATABASE_NAME")

@userge.on_cmd('dbq', about={
    'header': "Change database and restart",
    'flags': {'-c': "Clear Logs"}}, del_pre=True)
async def cdb_(message: Message):
    if DB_NAME is None:
        await message.edit("Please add VAR `DATABASE_NAME`", del_in=5)
        return
    await message.edit("`replacing database.py`")
    await asyncio.sleep(1)
    os.remove("userge/core/database.py")
    #os.remove("resources/userge.png")
    await asyncio.sleep(0.5)
    copyfile("userge/plugins/tools/resources/database.py", "userge/core/database.py")
    #copyfile("resources/z-emblem.png", "resources/userge.png")
    await asyncio.sleep(0.5)
    if "-c" in message.text:
        await message.edit("`Removing logs...`")
        rmtree("logs")
        os.mkdir("logs")
        await asyncio.sleep(1)
    await message.edit("`Restarting...`", del_in=1)
    await userge.restart(hard=True)
