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