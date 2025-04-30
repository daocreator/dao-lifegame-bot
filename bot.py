import os
import asyncio
from datetime import datetime, timedelta, time
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.utils.markdown import hbold
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

# Инициализация бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Asia/Bangkok")

# DAO-дата (рабочая, персональная, обычная) — упрощённо
def calculate_dao_dates():
    today = datetime.now()
    matrix_date = today.strftime("%d.%m.%Y")
    dow = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    weekday = dow[today.weekday()]
    # Пример: 3.3.3 = день 3, неделя 3, год 3
    delta = (today - datetime(2025, 1, 6)).days
    day = delta % 7 + 1
    week = (delta // 7) % 7 + 1
    year = (delta // 49) + 1
    dao_date = f"{day}.{week}.{year}"
    return weekday, dao_date, matrix_date

# Утреннее сообщение
async def send_morning_message():
    weekday, dao_date, matrix_date = calculate_dao_dates()
    text = (
        f"<b>🌞 Доброе утро, Дмитрий!</b>\n\n"
        f"📅 <b>Рабочий DAO-календарь:</b> <code>{dao_date}</code> ({weekday})\n"
        f"📆 <b>Общематричный:</b> {matrix_date}\n\n"
        f"🧭 Добродетель дня: <b>Умеренность</b>\n"
        f"🎴 Арканы: 1, 8, 15\n"
        f"🧬 Гормон: <b>Серотонин</b>\n"
        f"⚡ Активация: пробежка, благодарность, световое дыхание\n\n"
        f"❓ Как спалось? Что снилось?\n"
        f"❓ Где твоё внимание?\n"
        f"❓ Главный фокус на день?"
    )
    await bot.send_message(chat_id=OWNER_ID, text=text)

# Команда: /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот DAO LifeGame. Готов к запуску ☀️")

# Команда: /день
@dp.message(Command("день"))
async def day(message: Message):
    weekday, dao_date, matrix_date = calculate_dao_dates()
    await message.answer(
        f"📅 Сегодня:\n"
        f"— DAO: <code>{dao_date}</code>\n"
        f"— День недели: {weekday}\n"
        f"— Матричное: {matrix_date}"
    )

# Команда: /утро HH:MM
@dp.message(Command("утро"))
async def set_morning_time(message: Message):
    args = message.text.split()
    if len(args) != 2:
        await message.answer("Формат: /утро 08:45")
        return
    try:
        hour, minute = map(int, args[1].split(":"))
        scheduler.remove_all_jobs()
        scheduler.add_job(send_morning_message, "cron", hour=hour, minute=minute)
        await message.answer(f"⏰ Утреннее сообщение установлено на {hour:02}:{minute:02}")
    except:
        await message.answer("Неверный формат времени. Используй /утро HH:MM")

# Запуск
async def main():
    scheduler.add_job(send_morning_message, "cron", hour=9, minute=0)  # по умолчанию 9:00
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
