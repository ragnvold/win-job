import csv
import os
from telethon import TelegramClient
from config import keys
from datetime import date, timedelta

current_date = date.today()
days_in_year = 365
date_one_year_ago = current_date - timedelta(days=days_in_year)

# Создаем CSV файл и открываем его для записи
with open('messages.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Запишем заголовки для CSV файла
    csv_writer.writerow(['text'])

    # Создаем клиент Телеграмма
    with TelegramClient("userBot", api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"), device_model="iPhone 55 Pro",
                        system_version="IOS 100.1") as client:
        all_messages = client.iter_messages('https://t.me/infobizz1', reverse=True, offset_date=date_one_year_ago)
        a = 0
        k = 0
        for message in all_messages:
            k += 1
            try:
                # Проверяем условие с ключевыми словами и словом "ищу"
                if all(key.lower() not in message.text.lower() for key in keys) and "ищу" in message.text.lower():
                    a += 1

                    # Записываем информацию о сообщении в CSV файл
                    csv_writer.writerow([message.text])

                    # Выводим текст сообщения
                    print(message.text)
                else:
                    continue
            except:
                pass

print(a)
print(k)