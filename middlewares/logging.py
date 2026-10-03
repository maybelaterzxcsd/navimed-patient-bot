import logging
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            logger.info(f"Message from {event.from_user.id}: {event.text}")
        elif isinstance(event, CallbackQuery):
            logger.info(f"Callback from {event.from_user.id}: {event.data}")
        return await handler(event, data)