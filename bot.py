bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(f"Привет, {hbold(message.from_user.first_name)}! Я бот DAO LifeGame. Готов к запуску ☀️")


@dp.message(Command("день"))
async def day_handler(message: Message):
    await message.answer("🗓 Сегодняшняя дата по DAO-календарю: (здесь будет вставка позже)")

if __name__ == "__main__":
    import asyncio

    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())
