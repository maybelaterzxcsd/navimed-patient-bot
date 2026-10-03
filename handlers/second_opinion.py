from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from data.patients import PATIENT_DATA
from keyboards.inline import get_back_keyboard

router = Router()

@router.callback_query(F.data.startswith("second_"))
async def cb_second_opinion(call: CallbackQuery):
    patient_id = call.data.split("_")[1]
    
    text = (
        f"🩺 **Услуга «Живое второе мнение»**\n\n"
        f"Понимаем, что медицинские заключения могут вызывать тревогу. "
        f"Вы можете получить **видеоконсультацию** с ведущим специалистом клиники, который:\n\n"
        f"• Доступно объяснит каждый термин из заключения\n"
        f"• Ответит на все ваши вопросы\n"
        f"• Успокоит и составит четкий план действий\n\n"
        f"⏱ **Длительность:** 15 минут\n"
        f"💳 **Стоимость:** 2 900 ₽\n\n"
        f"Нажмите кнопку ниже, чтобы перейти к безопасной оплате. "
        f"Врач будет доступен в чате в течение 15 минут после оплаты."
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить и подключить врача", url="https://t.me/premium")],
        [InlineKeyboardButton(text="← Назад", callback_data=f"menu_{patient_id}")]
    ])
    
    await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data.startswith("payment_"))
async def cb_payment(call: CallbackQuery):
    patient_id = call.data.split("_")[1]
    patient = PATIENT_DATA.get(patient_id, PATIENT_DATA["1"])
    
    text = (
        f"💰 **Смета и способы оплаты**\n\n"
        f"📋 **Первичная консультация и AI-анализ:**\n"
        f"• По полису ОМС: **Бесплатно** (направление уже сформировано в системе)\n"
        f"• Платно: {patient['price']}\n\n"
        f"🏥 **Дополнительные обследования (при необходимости):**\n"
        f"• Биопсия / Доп. снимки: по ОМС или от 3 500 ₽\n\n"
        f"💡 *Совет: Хотите оплатить онлайн, чтобы не стоять в кассе перед приёмом? "
        f"Выберите услугу «Живое второе мнение» в главном меню.*"
    )
    
    await call.message.edit_text(text, reply_markup=get_back_keyboard(patient_id), parse_mode="Markdown")
    await call.answer()