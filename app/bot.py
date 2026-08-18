from config import BOT_TOKEN
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message:Message):
    await message.answer("Hello! How can I help you")

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())