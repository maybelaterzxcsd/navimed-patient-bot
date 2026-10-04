from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram import F

from data.patients import PATIENT_DATA
from keyboards.inline import get_main_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    args = message.text.split()
    
    if len(args) <= 1:
        await message.answer(
            "Пожалуйста, используйте персональную ссылку, которую вам отправил врач или ваш родственник."
        )
        return

    command = args[1]

    if command.startswith("relative_"):
        patient_id = command.replace("relative_", "")
        patient = PATIENT_DATA.get(patient_id, PATIENT_DATA["1"])
        
        text = (
            f"👋 Здравствуйте! Вы получили **семейный доступ** к маршруту пациента:\n"
            f"👤 **{patient['full_name']}**\n\n"
            f"Теперь вы можете просматривать его AI-рекомендации и помочь с записью к врачу ({patient['specialist']}).\n\n"
            f"Выберите действие ниже:"
        )
        await message.answer(text, reply_markup=get_main_keyboard(patient_id), parse_mode="Markdown")
        return

    elif command.startswith("patient_"):
        patient_id = command.replace("patient_", "")
        patient = PATIENT_DATA.get(patient_id, PATIENT_DATA["1"])
        
        text = (
            f"Здравствуйте, {patient['name']}! \n\n"
            f"Я ваш медицинский ассистент **МАКС** от клиники «Третье мнение».\n\n"
            f"Ваш лечащий врач сформировал для вас индивидуальный AI-маршрут на основе анализа ваших обследований. "
            f"Выберите действие ниже, чтобы узнать подробности или записаться на приём."
        )
        await message.answer(text, reply_markup=get_main_keyboard(patient_id), parse_mode="Markdown")
        return

@router.callback_query(F.data.startswith("menu_"))
async def cb_menu(call: CallbackQuery):
    patient_id = call.data.split("_")[1]
    patient = PATIENT_DATA.get(patient_id, PATIENT_DATA["1"])
    
    text = f"Главное меню\n\nВыберите действие:"
    await call.message.edit_text(text, reply_markup=get_main_keyboard(patient_id), parse_mode="Markdown")
    await call.answer()