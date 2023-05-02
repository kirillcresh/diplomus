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

DESC_COMMAND="""
<b>/start</b> - <em>запуск бота</em>
<b>Узнать категории</b> - <em>показывает категории товаров с магазина papayagame</em>"""


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/start", "/description", "Узнать категории магазина"]
    keyboard.add(*buttons)
    await message.answer("<em>Привет, <b>папаёнок</b></em> 🥭", reply_markup=keyboard, parse_mode="HTML")
    await message.delete()


@dp.message_handler(commands="description")
async def desc_command(message: types.Message):
    await message.answer("🫡 Я знаю следующие команды: \n" + DESC_COMMAND + "\n ...а также, пока ничего", parse_mode='HTML')
    await message.delete()


@dp.message_handler(Text(equals='Узнать категории'))
async def categories_command(message: types.Message):
    result = requests.get('http://127.0.0.1:8000/api/category-list/')
    reply = "Вот смотри: \n"
    for i in result.json():
        reply += str('-' + i["category"] + '\n')
    await message.reply(reply)


@dp.message_handler(Text(equals='Найти товар'))
async def echo(message: types.Message):
    await message.reply('Можно найти товар: \n <b>1.</b><em>По названию игры или комбинации символов</em> \n '
                        '<b>2.</b><em>Список товаров из определенной категории</em> \n <b>3.</b><em>По заданным критериям</em>', parse_mode='HTML')

@dp.message_handler()
async def echo(message: types.Message):
    text = "Я не понимаю что ты мне пишешь, человек"
    await bot.send_message(message.from_user.id, text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
