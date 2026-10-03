from aiogram import Router, F
from aiogram.types import CallbackQuery

from data.patients import PATIENT_DATA
from keyboards.inline import get_back_keyboard

router = Router()

@router.callback_query(F.data.startswith("route_"))
async def cb_route(call: CallbackQuery):
    patient_id = call.data.split("_")[1]
    patient = PATIENT_DATA.get(patient_id, PATIENT_DATA["1"])
    
    urgency_emoji = "🔴" if patient["urgency"] == "red" else "🟡" if patient["urgency"] == "yellow" else "🟢"
    
    text = (
        f"{urgency_emoji} **Результат AI-анализа**\n\n"
        f"👨‍⚕️ **Рекомендуемый специалист:** {patient['specialist']}\n"
        f"⏳ **Срок визита:** {patient['timeframe']}\n\n"
        f"💬 **Что это значит простыми словами:**\n"
        f"_{patient['human_conclusion']}_\n\n"
        f"️ **Обратитесь к врачу немедленно, если у вас есть:**\n"
        f"• Повышение температуры\n• Острая боль или дискомфорт\n• Ухудшение общего самочувствия"
    )
    
    await call.message.edit_text(text, reply_markup=get_back_keyboard(patient_id), parse_mode="Markdown")
    await call.answer()