import asyncio
import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from middlewares import LoggingMiddleware

# Импортируем ВСЕ роутеры (включая новый plan)
from handlers import start, routing, appointment, second_opinion, plan

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def start_health_check_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    logging.info(f"🌐 Health check server started on port {port} for Render")
    server.serve_forever()

threading.Thread(target=start_health_check_server, daemon=True).start()

async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    dp = Dispatcher()
    
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    
    dp.include_router(start.router)
    dp.include_router(plan.router)             
    dp.include_router(routing.router)
    dp.include_router(appointment.router)
    dp.include_router(second_opinion.router)
    
    logging.info("🤖 Бот МАКС успешно запущен и готов к работе!")
    logging.info("💡 Подсказка: Откройте Telegram и напишите /start patient_1")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")