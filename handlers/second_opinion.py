from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from data.patients import PATIENT_DATA
from keyboards.inline import get_back_keyboard

router = Router()

@router.callback_query(F.data.startswith("question_"))
async def cb_question(call: CallbackQuery):
    patient_id = call.data.split("_")[1]
    text = (
        f"❓ **Задать вопрос по заключению**\n\n"
        f"Медицинские термины могут быть непонятны. Наши кураторы помогут расшифровать ваше заключение простым языком.\n\n"
        f"Напишите ваш вопрос прямо в этот чат, и дежурный медицинский координатор ответит вам в течение 15 минут в рабочее время (с 09:00 до 21:00)."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Написать вопрос", url="https://t.me/navimed_bot")], # Ссылка на самого себя для демо
        [InlineKeyboardButton(text="← Назад", callback_data=f"menu_{patient_id}")]
    ])
    await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data.startswith("reminder_"))
async def cb_reminder(call: CallbackQuery):
    patient_id = call.data.split("_")[1]
    text = (
        f"🔔 **Напоминания о визите**\n\n"
        f"Мы ценим ваше время и здоровье. Вы можете включить автоматические напоминания:\n\n"
        f"• За 24 часа до визита к врачу\n"
        f"• За 2 часа до визита (с адресом клиники)\n"
        f"• Напоминание о необходимости взять снимки и паспорт\n\n"
        f"✅ *Функция будет активирована автоматически после записи на приём.*"
    )
    await call.message.edit_text(text, reply_markup=get_back_keyboard(patient_id), parse_mode="Markdown")
    await call.answer()