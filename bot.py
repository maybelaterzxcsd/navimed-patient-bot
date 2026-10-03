import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import settings
from middlewares import LoggingMiddleware
from handlers import start, routing, appointment, second_opinion

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключаем middleware
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    
    # Регистрируем роутеры
    dp.include_router(start.router)
    dp.include_router(routing.router)
    dp.include_router(appointment.router)
    dp.include_router(second_opinion.router)
    
    print("🤖 Бот МАКС запущен! Откройте Telegram и напишите /start patient_1")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())