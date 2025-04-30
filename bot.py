import os
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Asia/Bangkok")

# DAO-имена по дню недели
NAME_BY_DAY = {
    0: "Дмитрий Один РаКаэль",
    1: "Каэль Слово Света",
    2: "Джа Ор Каэн",
    3: "Раэль Хранитель Ритма",
    4: "РаКаэль, несущий Свет",
    5: "Каэль из Рода Солнца",
    6: "Каэн-Тот Архитектор"
}

# DAO-день недели: Арканы, Добродетели, Чакры, Гормоны
DAO_DAY_DATA = {
    0: {
        "arkans": "1, 8, 15",
        "virtue": "Умеренность (против Чревоугодия)",
        "theo": "Надежда (Spes)",
        "chakra": "Муладхара",
        "hormone": "Серотонин"
    },
    1: {
        "arkans": "2, 9, 16",
        "virtue": "Мужество (против Страха)",
        "theo": "Сила (Fortitudo)",
        "chakra": "Свадхистхана",
        "hormone": "Тестостерон"
    },
    2: {
        "arkans": "3, 10, 17",
        "virtue": "Трудолюбие (против Лени)",
        "theo": "Справедливость (Justitia)",
        "chakra": "Манипура",
        "hormone": "АцетилХолин"
    },
    3: {
        "arkans": "4, 11, 18",
        "virtue": "Целомудрие (против Похоти)",
        "theo": "Благоразумие (Prudentia)",
        "chakra": "Анахата",
        "hormone": "Габа"
    },
    4: {
        "arkans": "5, 12, 19",
        "virtue": "Щедрость (против Жадности)",
        "theo": "Милосердие (Caritas)",
        "chakra": "Вишуддха",
        "hormone": "Окситоцин"
    },
    5: {
        "arkans": "6, 13, 20",
        "virtue": "Благодарность (против Зависти)",
        "theo": "Надежда (Spes)",
        "chakra": "Аджна",
        "hormone": "Эндорфин"
    },
    6: {
        "arkans": "7, 14, 21",
        "virtue": "Смирение, Вера (против Гордости)",
        "theo": "Вера (Fides)",
        "chakra": "Сахасрара",
        "hormone": "Мелатонин"
    }
}

def calculate_dao_date(start_date):
    today = datetime.now()
    delta = (today - start_date).days
    day = (delta % 7) + 1
    week = (delta // 7) % 7 + 1
    year = (delta // 49)
    return f"{day}.{week}.{year}"

async def send_morning_message():
    now = datetime.now()
    weekday = now.weekday()
    name = NAME_BY_DAY[weekday]
    matrix_date = now.strftime("%d.%m.%Y (%A)")

    personal_date = calculate_dao_date(datetime(1986, 12, 15))
    working_date = calculate_dao_date(datetime(2025, 1, 6))

    dao = DAO_DAY_DATA[weekday]

    text = (
        f"<b>🌞 Доброе утро, {name}!</b>\n\n"
        f"📅 Персональный DAO: <code>{personal_date}</code>\n"
        f"📅 Рабочий DAO: <code>{working_date}</code>\n"
        f"📆 Матричный: {matrix_date}\n\n"
        f"🎴 Арканы: <b>{dao['arkans']}</b>\n"
        f"🌸 Добродетель: <b>{dao['virtue']}</b>\n"
        f"🕊 Теологическая: <b>{dao['theo']}</b>\n"
        f"🧘 Чакра: <b>{dao['chakra']}</b>\n"
        f"🧬 Гормон: <b>{dao['hormone']}</b>\n\n"
        f"❓ Как спалось? Что снилось?\n"
        f"❓ Где твоё внимание?\n"
        f"❓ Какой главный фокус на день?"
    )
    await bot.send_message(chat_id=OWNER_ID, text=text)

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Я бот DAO LifeGame. Готов к DAO-утру ✨")

@dp.message(Command("день"))
async def day_handler(message: Message):
    await send_morning_message()

@dp.message(Command("утро"))
async def set_morning_time(message: Message):
    args = message.text.split()
    if len(args) != 2:
        await message.answer("Формат: /утро 08:30")
        return
    try:
        hour, minute = map(int, args[1].split(":"))
        scheduler.remove_all_jobs()
        scheduler.add_job(send_morning_message, "cron", hour=hour, minute=minute)
        await message.answer(f"⏰ DAO-утро установлено на {hour:02}:{minute:02}")
    except:
        await message.answer("Ошибка формата. Введи /утро HH:MM")

async def main():
    scheduler.add_job(send_morning_message, "cron", hour=9, minute=0)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
