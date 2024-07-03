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
    await message.answer(f"Приветствую, {hbold(message.from_user.full_name)}! Здесь будут отправляться фриланс заказы")

@dp.message()
async def sendMessageOnModeration(message: types.Message):
    if message.from_user.id == 6463487004:
        reject_button = InlineKeyboardButton(
            text="Отклонить",
            callback_data="reject"
        )
        approve_button = InlineKeyboardButton(
            text="Одобрить",
            callback_data="approve"
        )
        spam_button = InlineKeyboardButton(
            text="Спам",
            callback_data="spam"
        )

        inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [approve_button],
                [reject_button],
                [spam_button]
            ]
        )

        await message.bot.send_message(
            chat_id=474703177,
            text=message.text,
            parse_mode=ParseMode.HTML,
            reply_markup=inline_keyboard
        )

@dp.callback_query(lambda c: c.data == "spam")
async def handle_spam_button(callback_query: CallbackQuery):
    await callback_query.message.forward(-4255452570)
    await callback_query.message.edit_text("Отправлено в канал со спам-объявлениями")
    await asyncio.sleep(2)
    await callback_query.message.delete()


@dp.callback_query(lambda c: c.data == "approve")
async def handle_approve_button(callback_query: CallbackQuery):
    headers = {
        "X-Requested-With": "XMLHttpRequest"
    }

    url = "https://app.leadteh.ru/api/v1/getContacts?api_token=E3NgGK6Erarz2kcgopkgLjPHQbWwmnIA2Lfoit7WugDP9MNlTgSIYGOXScU6&bot_id=484142"

    response = requests.get(url, headers=headers)
    data = response.json()

    spam_button = InlineKeyboardButton(text="Спам", callback_data="spam")
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[spam_button]])

    for i in data["data"]:
        if ("оплатил 1 месяц" in i["tags"] or
                "триал" in i["tags"] or
                "оплатил 3 месяца" in i["tags"] or
                "оплатил 6 месяцев" in i["tags"] or
                "оплатил 12 месяцев" in i["tags"]):
            try:
                if i["telegram_id"] != "474703177":
                    await callback_query.message.bot.send_message(
                        chat_id=i["telegram_id"],
                        text=callback_query.message.text,
                        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
                        reply_markup=inline_keyboard
                    )
            except Exception as ex:
                logging.error(f"{ex}")

    await callback_query.message.edit_text("Отправлено пользователям")
    await asyncio.sleep(2)
    await callback_query.message.delete()

@dp.callback_query(lambda c: c.data == "reject")
async def handle_reject_button(callback_query: CallbackQuery):
    await callback_query.message.delete()

async def main() -> None:
    bot = Bot(
        os.getenv("BOT_TOKEN"),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())