import asyncio
from telethon.tl.types import PeerUser
from telethon import TelegramClient, events, utils
from config import api_id, api_hash,keys
import requests
from gpt4free import check_message
#import nest_asyncio

#nest_asyncio.apply()

client = TelegramClient("userBot", api_id=api_id, api_hash=api_hash, device_model="iPhone 55 Pro", system_version="IOS 100.1")


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
        if check == True and all(key.lower() not in event.message.text.lower() for key in keys) :

                    await client.send_message(6567650179, msgFind)
                    print("отправил!!!!!!!!!!!!!")

async def run_main():
    await client.start(password='jvgggigz9teb')
    print("Bot started and waiting for new messages...")
    await client.run_until_disconnected()

# Run the event loop
if __name__ == "__main__":
    asyncio.run(run_main())