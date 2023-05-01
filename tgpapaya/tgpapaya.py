import os
from pathlib import Path

import requests
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, executor

CONFIG_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.abspath(CONFIG_DIR / 'config' / '.env'))
BOT_TOKEN = os.getenv('BOTTOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/start", "Покажи"]
    keyboard.add(*buttons)
    await message.answer("Привет, залупий", reply_markup=keyboard)


@dp.message_handler(Text(equals='Покажи'))
async def pokaji(message: types.Message):
    result = requests.get('http://127.0.0.1:8000/api/category-list/')
    reply = "Вот смотри \n"
    for i in result.json():
        reply += str(i["category"] + '\n')
    await message.answer(reply)


@dp.message_handler()
async def echo(message: types.Message):
    text = "Я не понимаю что ты мне пишешь, человек"
    await bot.send_message(message.from_user.id, text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
