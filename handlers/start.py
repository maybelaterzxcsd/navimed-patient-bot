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
    patient_id = args[1].replace("patient_", "") if len(args) > 1 else "1"
    
    patient = PATIENT_DATA.get(patient_id, PATIENT_DATA["1"])
    
    text = (
        f"Здравствуйте, {patient['name']}! \n\n"
        f"Я ваш медицинский ассистент **МАКС** от клиники «Третье мнение».\n\n"
        f"Ваш лечащий врач сформировал для вас индивидуальный AI-маршрут на основе анализа ваших обследований. "
        f"Выберите действие ниже, чтобы узнать подробности или записаться на приём."
    )
    
    await message.answer(text, reply_markup=get_main_keyboard(patient_id), parse_mode="Markdown")

@router.callback_query(F.data.startswith("menu_"))
async def cb_menu(call: CallbackQuery):
    patient_id = call.data.split("_")[1]
    patient = PATIENT_DATA.get(patient_id, PATIENT_DATA["1"])
    
    text = f"Главное меню для {patient['name']}\n\nВыберите действие:"
    await call.message.edit_text(text, reply_markup=get_main_keyboard(patient_id), parse_mode="Markdown")
    await call.answer()