from aiogram import Router, F
from aiogram.types import CallbackQuery

from data.patients import PATIENT_DATA
from keyboards.inline import get_slots_keyboard, get_back_keyboard

router = Router()

@router.callback_query(F.data.startswith("slots_"))
async def cb_slots(call: CallbackQuery):
    patient_id = call.data.split("_")[1]
    patient = PATIENT_DATA.get(patient_id, PATIENT_DATA["1"])
    
    text = (
        f"📅 **Свободные окна для записи**\n\n"
        f"Мы подобрали для вас ближайшие слоты к специалисту:\n"
        f"👨‍️ {patient['specialist']}"
    )
    
    await call.message.edit_text(
        text, 
        reply_markup=get_slots_keyboard(patient_id, patient['slots']), 
        parse_mode="Markdown"
    )
    await call.answer()

@router.callback_query(F.data.startswith("book_"))
async def cb_book(call: CallbackQuery):
    parts = call.data.split("_")
    patient_id = parts[1]
    slot_idx = int(parts[2])
    patient = PATIENT_DATA.get(patient_id, PATIENT_DATA["1"])
    chosen_slot = patient['slots'][slot_idx]
    
    text = (
        f"✅ **Вы успешно записаны!**\n\n"
        f"🗓 **Дата и время:** {chosen_slot}\n"
        f"👨‍⚕️ **Специалист:** {patient['specialist']}\n\n"
        f"За сутки до приёма мы пришлём вам напоминание с адресом клиники и списком документов, "
        f"которые нужно взять с собой (паспорт, полис ОМС, результаты снимков).\n\n"
        f"Если планы изменятся, вы можете отменить запись в любой момент."
    )
    
    await call.message.edit_text(text, reply_markup=get_back_keyboard(patient_id), parse_mode="Markdown")
    await call.answer("✅ Вы записаны!")