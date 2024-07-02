import asyncio
import logging
import sys
import requests
import os
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold
from aiogram.client.default import DefaultBotProperties
from aiogram import (
    Bot,
    Dispatcher,
    Router,
    types
)
from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    Message, 
    CallbackQuery
)

dp = Dispatcher()
rt = Router()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    logging.info("Print hello message")
    await message.answer(f"Приветствую, {hbold(message.from_user.full_name)}! Здесь будут отправляться фриланс заказы")

@dp.message()
async def echo(message: types.Message):
    if message.from_user.id == 6463487004:
        headers = {
            "X-Requested-With": "XMLHttpRequest"
        }

        url = "https://app.leadteh.ru/api/v1/getContacts?api_token=E3NgGK6Erarz2kcgopkgLjPHQbWwmnIA2Lfoit7WugDP9MNlTgSIYGOXScU6&bot_id=484142"

        response = requests.get(url, headers=headers)
        data = response.json()

        reject_button = InlineKeyboardButton(text="Отклонить", callback_data="reject")
        approve_button = InlineKeyboardButton(text="Одобрить", callback_data="approve")
        spam_button = InlineKeyboardButton(text="Спам", callback_data="spam")
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[approve_button], [reject_button], [spam_button]])

        await message.bot.send_message(chat_id=776062536, text=message.text, parse_mode=ParseMode.HTML,
                                       reply_markup=inline_keyboard)
        await message.bot.send_message(chat_id=474703177, text=message.text, parse_mode=ParseMode.HTML,
                                       reply_markup=inline_keyboard)
        await message.bot.send_message(chat_id=756743749, text=message.text, parse_mode=ParseMode.HTML,
                                       reply_markup=inline_keyboard)


@dp.callback_query(lambda c: c.data == "spam")
async def handle_spam_button(callback_query: CallbackQuery):
    # Перешлите сообщение в целевой канал
    await callback_query.message.forward(-4255452570)

    # Подтвердите получение нажатия кнопки
    await callback_query.message.edit_text("Отправлено в канал со спам-объявлениями")

    await asyncio.sleep(2)

    await callback_query.message.delete()


@dp.callback_query(lambda c: c.data == "approve")
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

                if i["telegram_id"] != "776062536" and i["telegram_id"] != "474703177" and i["telegram_id"] != "756743749":
                    print(f'id {i["telegram_id"]}')
                    await callback_query.message.bot.send_message(chat_id=i["telegram_id"],
                                                                  text=callback_query.message.text,
                                                                  default=DefaultBotProperties(parse_mode=ParseMode.HTML),
                                                                  reply_markup=inline_keyboard)
                    print("отправил")
            except:
                print(i["telegram_id"])
    await callback_query.message.edit_text("Отправлено пользователям")

    await asyncio.sleep(2)

    await callback_query.message.delete()


async def main() -> None:
    bot = Bot(os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())