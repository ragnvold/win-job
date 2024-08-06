from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 28496112
api_hash = '9a760f8886eb20ae322f4cde65a93f31'

with TelegramClient(StringSession(), api_id, api_hash) as client:
    session_string = client.session.save()
    print(f"Your session string:\n{session_string}")