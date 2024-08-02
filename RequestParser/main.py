import asyncio
import requests
import os
import logging
from telethon.tl.types import PeerUser
from config import keys
from gpt4free import check_message
from telethon import (
    TelegramClient, 
    events, 
    utils
)

client = TelegramClient(
    "userBot",
    api_id=os.getenv("API_ID"),
    api_hash=os.getenv("API_HASH"),
    device_model="iPhone 55 Pro",
    system_version="IOS 100.1"
)

banUserSet = {
    6520281407,
    7346459736,
    5111381608,
    1223438727,
    7302101418,
    486084821,
    5620022640,
    1591094277,
    6319502017,
    7236659071,
    5533958174,
    6410409097,
    5303059998,
    6765407077,
    5662208565,
    5228317551,
    5640323779,
    6853005537,
    5592599153,
    7402233764,
    6564790996,
    7355426232,
    553147242,
    6707598103,
    6917732312,
    5604687742,
    5794766025,
    7222338989,
    5700211834,
    7131538094,
    1602210650,
    7263765711,
    6938455016,
    7388268937,
    6451880645,
    5085903947,
    7416478052,
    6840629202,
    6454743780,
    1709990968,
    2105028192,
    7261814814,
    875512659,
    1237690305,
    6628908108,
    6957641230,
    7451162316,
    7458007485,
    5248094972,
    1618862931,
    7072393085,
    5323961178,
    6450096759,
    6485742675,
    1675582506,
    5406169457,
    7028187940,
    6673824542,
    6656647741,
    6441784053,
    5984140691,
    5221524413,
    5748510253,
    5537201341,
    6980169027,
    6527894081,
    7022516094,
    6570307951,
    7415126973,
    1591254032,
    1666316390,
    2075961827,
    6966421769,
    1874105176,
    5628817359,
    6362780519,
    5572159027,
    6511372210,
    5423054147,
    7273609849,
    6949171148,
    971480272,
    7193096897,
    962081869,
    7290918366,
    6302870359,
    5486893260,
    382687440,
    5580502006,
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def checkSenderUsername(event):
    sender = await event.message.get_sender()
    return sender is not None and sender.username is not None

async def checkUserIdBlocked(event):
    sender = await event.message.get_sender()
    if sender != None:
        return sender.id in banUserSet
    else:
        logging.info(f"No sender information for message: {event.message.id}")
        return True

@client.on(events.NewMessage)
async def main(event):
    isUserBanned = await checkUserIdBlocked(event)

    if isUserBanned == False:
        isSenderHasUsername = await checkSenderUsername(event)

        if isSenderHasUsername:
            sender = await event.get_sender()
            messageText = event.message.text

            msgFind = (
                f"📩 Новая заявка!\n\n"
                f"👤 Юзернейм: @{sender.username}\n\n"
                f"💬 Сообщение:\n\n`{messageText}`"
            )

            targetChatBotId = int(os.getenv("TARGET_CHAT_BOT_ID"))
            await client.send_message(targetChatBotId, msgFind)
            
            smmChatBotId = int(os.getenv("SMM_CHAT_BOT_ID"))
            await client.send_message(smmChatBotId, msgFind)

async def run_main():
    await client.start(password=os.getenv("USER_BOT_PASSWORD"))
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(run_main())