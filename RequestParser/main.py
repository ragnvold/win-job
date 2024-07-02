import asyncio
import requests
import os
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

async def check_username(message):
    sender = await message.get_sender()
    if sender.username == None:
        return (False)
    else:
        return f'{sender.username}'


@client.on(events.NewMessage)
async def main(event):
    if await check_username(event) == False:
        sender = await event.get_sender()
        msgFind = (f"📩 **Новая заявка!**\n\n**├🌐 Название чата:** `{event.message.chat.title}`\n**├🆔 ID чата:** `"
                   f"{event.message.chat_id}`\n**├👤 Пользователь:** `{sender.first_name}`\n**├💬 Юзернейм:** "
                   f"@{await check_username(event)}**└📎"
                   f"\n\n**💬 Сообщение:**\n\n`{event.message.text}`")
        check = await check_message(event.message.text)
        print(check)
        if check == True and all(key.lower() not in event.message.text.lower() for key in keys):
            await client.send_message(474703177, msgFind)

async def run_main():
    await client.start(password=os.getenv("USER_BOT_PASSWORD"))
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(run_main())