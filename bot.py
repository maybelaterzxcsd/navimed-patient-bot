import asyncio
import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from aiogram import Bot, Dispatcher
from config import settings
from middlewares import LoggingMiddleware
from handlers import start, routing, appointment, second_opinion

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def start_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    print(f"🌐 Dummy server started on port {port} for Render health check")
    server.serve_forever()

threading.Thread(target=start_dummy_server, daemon=True).start()

async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    
    dp.include_router(start.router)
    dp.include_router(routing.router)
    dp.include_router(appointment.router)
    dp.include_router(second_opinion.router)
    
    print("🤖 Бот МАКС запущен! Откройте Telegram и напишите /start patient_1")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())