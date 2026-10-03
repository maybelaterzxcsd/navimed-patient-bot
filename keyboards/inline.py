from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard(patient_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Мой AI-маршрут", callback_data=f"route_{patient_id}")],
        [InlineKeyboardButton(text="📅 Записаться на приём", callback_data=f"slots_{patient_id}")],
        [InlineKeyboardButton(text="❓ Задать вопрос по заключению", callback_data=f"question_{patient_id}")],
        [InlineKeyboardButton(text="🔔 Напоминания о визите", callback_data=f"reminder_{patient_id}")],
    ])

def get_back_keyboard(patient_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← В главное меню", callback_data=f"menu_{patient_id}")]
    ])

def get_slots_keyboard(patient_id: str, slots: list) -> InlineKeyboardMarkup:
    keyboard = []
    for i, slot in enumerate(slots):
        keyboard.append([InlineKeyboardButton(text=slot, callback_data=f"book_{patient_id}_{i}")])
    keyboard.append([InlineKeyboardButton(text="← Назад", callback_data=f"menu_{patient_id}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)