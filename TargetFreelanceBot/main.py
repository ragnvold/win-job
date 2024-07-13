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
    await message.answer(f"Приветствую, {hbold(message.from_user.full_name)}! Здесь будут отправляться фриланс-заказы")

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
        
        targetChatBotOperatorId = int(os.getenv("TARGET_CHAT_BOT_OPERATOR"))

        await message.bot.send_message(
            chat_id=targetChatBotOperatorId,
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

async def checkUserHasChat(bot, userId: int) -> bool:
    try:
        chat = await bot.get_chat(userId)
        return True
    except Exception as e:
        logging.error(f"Error: {e}")
        return False

@dp.callback_query(lambda c: c.data == "approve")
async def handle_approve_button(callback_query: CallbackQuery):
    spam_button = InlineKeyboardButton(text="Спам", callback_data="spam")
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[spam_button]])
    
    headers = {
        "X-Requested-With": "XMLHttpRequest"
    }

    url = "https://app.leadteh.ru/api/v1/getContacts?api_token=E3NgGK6Erarz2kcgopkgLjPHQbWwmnIA2Lfoit7WugDP9MNlTgSIYGOXScU6&bot_id=484142"

    response = requests.get(url, headers=headers)
    responseJSON = response.json()
    requestRecipients = responseJSON["data"]
    
    requiredRecipientTags = [
        "target_category_trial_activated",
        "paid_target_category_1_month",
        "paid_target_category_3_months",
        "paid_target_category_6_months",
        "paid_target_category_12_months",
    ]
    
    for recipient in requestRecipients:
        recipientTags = recipient["tags"]
        
        if set(recipientTags) & set(requiredRecipientTags):
            recipientTelegramId = recipient["telegram_id"]
            try:
                if recipientTelegramId != os.getenv("TARGET_CHAT_BOT_OPERATOR"):
                    isUserHasChat = await checkUserHasChat(
                        callback_query.message.bot,
                        recipientTelegramId,
                    )
                    if checkUserHasChat:
                        await callback_query.message.bot.send_message(
                            chat_id=recipientTelegramId,
                            text=callback_query.message.text,
                            reply_markup=inline_keyboard,
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
        os.getenv("TARGET_BOT_TOKEN"),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())