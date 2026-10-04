from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard(patient_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=" Мой AI-маршрут", callback_data=f"route_{patient_id}")],
        [InlineKeyboardButton(text="📅 Забронировать слот (2 часа)", callback_data=f"book_{patient_id}")],
        [InlineKeyboardButton(text="❓ Вопросы к врачу от ИИ", callback_data=f"questions_{patient_id}")],
        [InlineKeyboardButton(text="📆 План наблюдения на 3 месяца", callback_data=f"plan_{patient_id}")],
        [InlineKeyboardButton(text="👨‍👩👧 Поделиться с родственником", callback_data=f"share_{patient_id}")]
    ])

def get_back_keyboard(patient_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад в меню", callback_data=f"menu_{patient_id}")]
    ])

def get_slots_keyboard(patient_id: str, slots: list) -> InlineKeyboardMarkup:
    keyboard = []
    for i, slot in enumerate(slots):
        keyboard.append([InlineKeyboardButton(text=slot, callback_data=f"book_{patient_id}_{i}")])
    keyboard.append([InlineKeyboardButton(text="← Назад", callback_data=f"menu_{patient_id}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)