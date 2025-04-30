import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("Привет! Я бот DAO LifeGame. Готов к работе.")

@dp.message_handler(commands=["день"])
async def day_handler(message: types.Message):
    await message.reply("Сегодняшняя дата по DAO-календарю: ...")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
