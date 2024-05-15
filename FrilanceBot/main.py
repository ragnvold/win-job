import asyncio
import logging
import sys
from os import getenv
import requests

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.utils.markdown import hbold

TOKEN = "6567650179:AAGgzkRmYKGwwWNDuznV_l8poqcrdbYq4nU"

dp = Dispatcher()
rt = Router()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(f"Приветствую! {hbold(message.from_user.full_name)}! Здесь будут отправляться фриланс заказы")


@dp.message()
async def echo(message: types.Message):
    if message.from_user.id == 6463487004:
        headers = {
            "X-Requested-With": "XMLHttpRequest"
        }

        url = "https://app.leadteh.ru/api/v1/getContacts?api_token=E3NgGK6Erarz2kcgopkgLjPHQbWwmnIA2Lfoit7WugDP9MNlTgSIYGOXScU6&bot_id=484142"

        response = requests.get(url, headers=headers)
        data = response.json()

        spam_button = InlineKeyboardButton(text="Спам", callback_data="spam")
        ne_spam_button = InlineKeyboardButton(text="Одобрить", callback_data="ne_spam")
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[spam_button],[ne_spam_button]])

        await message.bot.send_message(chat_id=776062536, text=message.text, parse_mode=ParseMode.HTML,
                                       reply_markup=inline_keyboard)
        await message.bot.send_message(chat_id=474703177, text=message.text, parse_mode=ParseMode.HTML,
                                       reply_markup=inline_keyboard)


@dp.callback_query(lambda c: c.data == "spam")
async def handle_spam_button(callback_query: CallbackQuery):
    # Перешлите сообщение в целевой канал
    await callback_query.message.forward(-4255452570)

    # Подтвердите получение нажатия кнопки
    await callback_query.message.edit_text("отправлено в канал Спам объявления")

    await asyncio.sleep(4)

    await callback_query.message.delete()


@dp.callback_query(lambda c: c.data == "ne_spam")
async def handle_ne_spam_button(callback_query: CallbackQuery):
    headers = {
        "X-Requested-With": "XMLHttpRequest"
    }

    url = "https://app.leadteh.ru/api/v1/getContacts?api_token=E3NgGK6Erarz2kcgopkgLjPHQbWwmnIA2Lfoit7WugDP9MNlTgSIYGOXScU6&bot_id=484142"

    response = requests.get(url, headers=headers)
    data = response.json()
    spam_button = InlineKeyboardButton(text="спам", callback_data="spam")
    message_text = callback_query.message.text
    logging.info(f" сообщение {message_text}")
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[spam_button]])
    print(data["data"])
    for i in data["data"]:
        if ("оплатил 1 месяц" in i["tags"] or
                "триал" in i["tags"] or
                "оплатил 3 месяца" in i["tags"] or
                "оплатил 6 месяцев" in i["tags"] or
                "оплатил 12 месяцев" in i["tags"]):
            try:

                if i["telegram_id"] != "776062536" and i["telegram_id"] !="474703177":
                    print(f'id {i["telegram_id"]}')
                    await callback_query.message.bot.send_message(chat_id=i["telegram_id"],
                                                                  text=callback_query.message.text,
                                                                  parse_mode=ParseMode.HTML,
                                                                  reply_markup=inline_keyboard)
                    print("отправил")
            except:
                print(i["telegram_id"])
    #await callback_query.message.forward(-4255452570)
    await callback_query.message.edit_text("отправлено пользователям")

    await asyncio.sleep(4)

    await callback_query.message.delete()


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())