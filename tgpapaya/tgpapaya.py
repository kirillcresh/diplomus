import os
import random
from pathlib import Path

import requests
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv

CONFIG_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.abspath(CONFIG_DIR / "config" / ".env"))
BOT_TOKEN = os.getenv("BOTTOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text="Главная страница", url="http://127.0.0.1:8000/")
ib2 = InlineKeyboardButton(text="Новости", url="http://127.0.0.1:8000/news/")
ib3 = InlineKeyboardButton(text="Магазин", url="http://127.0.0.1:8000/shop/")
ib4 = InlineKeyboardButton(text="Регистрация", url="http://127.0.0.1:8000/register/")
ikb.add(ib1, ib2).add(ib3, ib4)

_NP_PHOTO_PATH = os.path.abspath(CONFIG_DIR / "papaya")

DESC_COMMAND = """
<b>/start</b> - <em>запуск бота;</em>
<b>/location</b> - <em>показывает адрес магазина papayagame;</em>
<b>/give_adr</b> - <em>ссылка на сайт papayagame;</em>
<b>Узнать категории</b> - <em>показывает категории товаров с магазина papayagame</em>
<b>Последняя новость магазина</b> - <em>показывает последнюю добавленную новость на сайте papayagame</em>
<b>Найти товар</b> - <em>показывает варианты поиска товара с интернет-магазина papayagame</em>"""


def get_buttons(buttons: list):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


async def on_startup(_):
    print("Бот запущен")


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    keyboard = get_buttons(["/start", "/description", "/give_adr"])
    await message.answer(
        "<i>Привет</i>, <b>папаёнок</b> 🥭", reply_markup=keyboard, parse_mode="HTML"
    )
    await message.delete()


@dp.message_handler(commands="description")
async def desc_command(message: types.Message):
    await message.answer(
        "🫡 Я знаю следующие команды:"
        " \n" + DESC_COMMAND + "\n ... а также, попробуйте мне прислать стикер. \n"
        "Пока вот вам котик:",
        parse_mode="HTML",
    )
    keyboard = get_buttons(
        [
            "/start",
            "/location",
            "/give_adr",
            "Узнать категории магазина",
            "Последняя новость магазина",
            "Найти товар",
        ]
    )
    await bot.send_sticker(
        message.from_user.id,
        reply_markup=keyboard,
        sticker="CAACAgIAAxkBAAEI5RlkWBFnPNZ_sHdS1ynt0yAy85G0jAACBAADnmyTLl0puI2aiCV1LwQ",
    )
    await message.delete()


@dp.message_handler(commands="location")
async def desc_command(message: types.Message):
    await bot.send_message(message.from_user.id, text="Магазин находится здесь: \n")
    await bot.send_location(
        message.from_user.id, latitude=57.861638, longitude=28.197695
    )
    await message.delete()


@dp.message_handler(commands="give_adr")
async def adr_need(message: types.Message):
    await message.answer(text="Выберите куда хотите перейти:", reply_markup=ikb)
    await message.delete()


@dp.message_handler(Text(equals="Узнать категории магазина"))
async def categories_command(message: types.Message):
    result = requests.get("http://127.0.0.1:8000/api/category-list/")
    reply = "Вот смотри: \n"
    for i in result.json():
        reply += str("-" + "<u>" + i["category"] + "</u>" + "\n")
    await message.reply(reply, parse_mode="HTML")


@dp.message_handler(Text(equals="Найти товар"))
async def find_goods(message: types.Message):
    keyboard = get_buttons(["По категории", "По критериям"])
    await message.reply(
        "Можно найти товар: \n "
        "<b>1.</b><em>Список товаров из определенной категории</em> \n "
        "<b>2.</b><em>По заданным критериям (Кол-во игроков, время игры и т.п.) \n</em>"
        "<b>3.По комбинации символов</b><em>Просто введите название игры или ключевое слово, "
        "которое может содержаться в описании игры</em>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


@dp.message_handler(Text(equals="Последняя новость магазина"))
async def last_news(message: types.Message):
    try:
        result = requests.get("http://127.0.0.1:8000/api/last-news/")
        reply = "Последняя новость: \n"
        reply += str("<b>" + result.json()["title"] + "</b>" + "\n")
        reply += str(result.json()["news"] + "\n")
        reply += str("Дата публикации:" + str(result.json()["pub_date"][:10]) + "\n")
        pic = open(
            (str(_NP_PHOTO_PATH) + "/" + str(result.json()["picture"])).replace(
                "\\", "/"
            ),
            "rb",
        )
        await bot.send_photo(
            message.from_user.id,
            photo=pic,
            caption=str(reply),
            reply_to_message_id=message.message_id,
            parse_mode="html"
        )
    except Exception:
        await message.answer(text='Новостей на сайте пока что нет.')


@dp.message_handler(Text(equals="По категории"))
async def search_by_category(message: types.Message):
    cat_list = requests.get("http://127.0.0.1:8000/api/category-list/")
    buttons = []
    for i in cat_list.json():
        buttons.append(i["category"])
    keyboard = get_buttons(buttons)
    answer = "Выберите нужную вам категорию с помощью кнопок."
    await bot.send_message(message.from_user.id, answer, reply_markup=keyboard)


@dp.message_handler()
async def try_category(message: types.Message):
    try:
        result = requests.get(
            f"http://127.0.0.1:8000/api/game-by-category/?cat_games_search={message.text}"
        )
        reply = "Вот товары из данной категории: \n"
        for i in result.json():
            reply += str(
                "-" + "<u>" + str(i["title"]) + "</u>" + str(i["price"]) + "₽" + "\n"
            )
        keyboard = get_buttons(
            [
                "/start",
                "/location",
                "Узнать категории магазина",
                "Последняя новость магазина",
                "Найти товар",
            ]
        )
        await message.reply(reply, parse_mode="HTML", reply_markup=keyboard)
    except Exception:
        await try_search(message)


@dp.message_handler()
async def try_search(message: types.Message):
    try:
        result = requests.get(
            f"http://127.0.0.1:8000/api/game-by-name/?games_search={message.text}"
        )
        reply = "Вот что я нашел: \n" + "Игра:"
        reply += str("<i>" + result.json()["title"] + "</i>" + "\n")
        reply += str(result.json()["games"] + "\n") + "Стоимость:"
        reply += str(result.json()["price"]) + "<b>" + "₽" + "</b>" + "\n"
        reply += (
            "<i>"
            + "Если это не то, что вы искали, попробуйте начать поиск заново, уже с учетом данной "
            "информации, которая поможет сузить круг, либо данного товара пока что нет в магазине"
            + "</i>"
        )
        keyboard = get_buttons(
            [
                "/start",
                "/location",
                "Узнать категории магазина",
                "Последняя новость магазина",
                "Найти товар",
            ]
        )
        pic = open(
            (str(_NP_PHOTO_PATH) + "/" + str(result.json()["picture"])).replace(
                "\\", "/"
            ),
            "rb",
        )
        await bot.send_photo(
            message.from_user.id,
            photo=pic,
            caption=str(reply),
            reply_to_message_id=message.message_id,
            parse_mode="html",
            reply_markup=keyboard,
        )
    except Exception:
        await echo(message)


@dp.message_handler(content_types=["sticker"])
async def random_sticker(message: types.Message):
    stick_list = [
        "CAACAgIAAxkBAAEI66FkWjQgx4fVZ4_ilcIMtqmSSV4XjwACBwADwDZPE0hhd1MIpyLHLwQ",
        "CAACAgIAAxkBAAEI66NkWjQmc80lwe2MGZKhUpaGYrOrOQACFgADwDZPE2Ah1y2iBLZnLwQ",
        "CAACAgIAAxkBAAEI7jdkW2ct7QwWXcwT0Roq6YTvpIy6JgACGAADwDZPE9b6J7-cahj4LwQ",
        "CAACAgIAAxkBAAEI7jlkW2c0ay0vbCgRJnRjoL28ugABpxwAAhAAA8A2TxPqgYop8R8C6C8E",
        "CAACAgIAAxkBAAEI7jtkW2c52Vl5OcmfMPLx6IRrY_IfSAACHgADwDZPE6FgWy2rAAHeBC8E",
        "CAACAgIAAxkBAAEI7j1kW2dAVO4w7Ov4yS0Ir3HtkOYUxwACWRgAAnNiCEpMsznZWoSrVy8E",
        "CAACAgIAAxkBAAEI7j9kW2dKCiAQkM5OIAXPc_ob4-UzHAACLQADoYxBCxo5ICfAtt_4LwQ",
        "CAACAgIAAxkBAAEI7kFkW2dXiP4vBGgBSbrWvw1KmujWxwACjAADFkJrCkKO_mIXPU3iLwQ",
    ]
    id_stick = random.choice(stick_list)
    keyboard = get_buttons(
        [
            "/start",
            "/location",
            "/give_adr",
            "Узнать категории магазина",
            "Последняя новость магазина",
            "Найти товар",
        ]
    )
    await bot.send_sticker(
        message.from_user.id, sticker=id_stick, reply_markup=keyboard
    )


@dp.message_handler()
async def echo(message: types.Message):
    keyboard = get_buttons(
        [
            "/start",
            "/location",
            "/give_adr",
            "Узнать категории магазина",
            "Последняя новость магазина",
            "Найти товар",
        ]
    )
    text = "Я не понимаю что ты мне пишешь, человек 🫣"
    await bot.send_message(message.from_user.id, text, reply_markup=keyboard)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
