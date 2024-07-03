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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def checkSenderUsername(event):
    sender = await event.message.get_sender()
    if sender == None:
        return False
    else:
        if sender.username == None:
            return False
        else:
            return True

@client.on(events.NewMessage)
async def main(event):
    isSenderHasUsername = await checkSenderUsername(event)

    if isSenderHasUsername:
        sender = await event.get_sender()
        chatTitle = event.message.chat.title
        chatId = event.message.chat_id
        messageText = event.message.text

        msgFind = (
            f"📩 **Новая заявка!**\n\n"
            f"**├🌐 Название чата:** `{chatTitle}`\n"
            f"**├🆔 ID чата:** `{chatId}`\n"
            f"**├👤 Юзернейм:** @{sender.username}**└📎\n\n"
            f"**💬 Сообщение:**\n\n`{messageText}`"
        )

        chatBotId = int(os.getenv("CHAT_BOT_ID"))
        await client.send_message(chatBotId, msgFind)

async def run_main():
    await client.start(password=os.getenv("USER_BOT_PASSWORD"))
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(run_main())