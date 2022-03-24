from userge import userge, Message, filters

LOG = userge.getLogger(__name__)  # logger object
CHANNEL = userge.getCLogger(__name__)  # channel logger object

# add command handler
@userge.on_cmd("zcus", about="Just notif")
async def test_cmd(message: Message):
   await message.edit("Custom Plugins Resources: Loaded!", del_in=3)  # this will be automatically deleted after 5 sec
