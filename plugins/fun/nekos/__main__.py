import os

from anekos import NekosLifeClient, SFWImageTags
from pyrogram.errors import MediaEmpty, WebpageCurlFailed
from wget import download

from userge import userge, Message

client = NekosLifeClient()

SFW = [z for z in dir(SFWImageTags) if not z.startswith("__")]


neko_help = "\n\n<b>SFW</b> :  "
for m in SFW:
    neko_help += f"<code>{m.lower()}</code>   "


@userge.on_cmd(
    "nekos",
    about={
        "header": "Get stuff from nekos.life",
        "usage": "{tr}nekos\n{tr}nekos [Choice]",
        "Choice": neko_help,
    },
)
async def neko_life(message: Message):
    choice = message.input_str
    if choice:
        input_choice = (choice.strip()).upper()
        if input_choice in SFW:
            link = (await client.image(SFWImageTags[input_choice])).url
        else:
            await message.err(
                "Choose a valid Input !, See Help for more info.", del_in=5
            )
            return
    else:
        link = (await client.random_image()).url

    await message.delete()

    try:
        await send_nekos(message, link)
    except (MediaEmpty, WebpageCurlFailed):
        link = download(link)
        await send_nekos(message, link)
        os.remove(link)


async def send_nekos(message: Message, link: str):
    reply = message.reply_to_message
    reply_id = reply.message_id if reply else None
    if link.endswith(".gif"):
        #  Bots can't use "unsave=True"
        bool_unsave = not message.client.is_bot
        await message.client.send_animation(
            chat_id=message.chat.id,
            animation=link,
            unsave=bool_unsave,
            reply_to_message_id=reply_id,
        )
    else:
        await message.client.send_photo(
            chat_id=message.chat.id, photo=link, reply_to_message_id=reply_id
        )
