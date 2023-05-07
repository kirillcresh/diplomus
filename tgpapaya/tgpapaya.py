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
<b>/start</b> - <em>запуск бота;</em>
<b>Узнать категории</b> - <em>показывает категории товаров с магазина papayagame</em>
<b>Последняя новость магазина</b> - <em>показывает последнюю добавленную новость на сайте papayagame</em>
<b>Найти товар</b> - <em>показывает варианты поиска товара с интернет-магазина papayagame</em>"""


def get_buttons(buttons: list):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    keyboard = get_buttons(["/start", "/description", "Узнать категории магазина", "Последняя новость магазина",
                            "Найти товар"])
    await message.answer("<em>Привет</em>, <b>папаёнок</b> 🥭", reply_markup=keyboard, parse_mode="HTML")
    await message.delete()


@dp.message_handler(commands="description")
async def desc_command(message: types.Message):
    await message.answer("🫡 Я знаю следующие команды:"
                         " \n" + DESC_COMMAND + "\n ... а также, пока ничего, ждите моего нового обновления."
                        "Пока вот вам котик: ", parse_mode='HTML')
    await bot.send_sticker(message.from_user.id,
                           sticker='CAACAgIAAxkBAAEI5RlkWBFnPNZ_sHdS1ynt0yAy85G0jAACBAADnmyTLl0puI2aiCV1LwQ')
    await message.delete()


@dp.message_handler(Text(equals='Узнать категории магазина'))
async def categories_command(message: types.Message):
    result = requests.get('http://127.0.0.1:8000/api/category-list/')
    reply = "Вот смотри: \n"
    for i in result.json():
        reply += str('-' + '<u>' + i["category"] + '</u>' + '\n')
    await message.reply(reply, parse_mode='HTML')


@dp.message_handler(Text(equals='Найти товар'))
async def find_goods(message: types.Message):
    keyboard = get_buttons(['1.По категории', '2.По критериям'])
    await message.reply('Можно найти товар: \n '
                        '<b>1.</b><em>Список товаров из определенной категории</em> \n '
                        '<b>2.</b><em>По заданным критериям (Кол-во игроков, время игры и т.п.)</em>'
                        "<b>По комбинации символов</b><em>Просто введите название игры или ключевое слово, "
                        "которое может содержаться в описании игры</em>",  parse_mode='HTML', reply_markup=keyboard)


@dp.message_handler(Text(equals="Последняя новость магазина"))
async def last_news(message: types.Message):
    try:
        result = requests.get('http://127.0.0.1:8000/api/last-news/')
        reply = "Последняя новость: \n"
        reply += str('<b>'+result.json()["title"] + '</b>' + '\n')
        reply += str(result.json()["news"] + '\n')
        reply += str("Дата публикации:" + str(result.json()["pub_date"]) + '\n')
        await message.reply(reply, parse_mode='HTML')
    except Exception:
        await message.reply(text='Пока на сайте нет новостей, но очень скоро появятся и очень интересные, не пропусти!')


@dp.message_handler()
async def try_search(message: types.Message):
    try:
        result = requests.get(f'http://127.0.0.1:8000/api/game-by-name/?games_search={message.text}')
        reply = "Вот что я нашел: \n"
        reply += str('<i>' + result.json()["title"] + '</i>' + '\n')
        reply += str(result.json()["games"] + '\n')
        # reply += str('<b>' + result.json()["price"] + '</b>' + '\n')
        reply += str('<em' + 'Если это не то, что вы искали, попробуйте начать поиск заново, уже с учетом '
                             'данной информации, которая поможет сузить круг, '
                             'либо данного товара пока что нет в магазине \n' + '</em>')
        await message.reply(reply, parse_mode='HTML')
    except Exception:
        await echo(message)


# @dp.message_handler()
# async def try_search(message: types.Message):
#     try:
#         result = requests.get(f'http://127.0.0.1:8000/api/game-by-name/?games_search={message.text}')


async def echo(message: types.Message):
    text = "Я не понимаю что ты мне пишешь, человек 🫣"
    await bot.send_message(message.from_user.id, text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
