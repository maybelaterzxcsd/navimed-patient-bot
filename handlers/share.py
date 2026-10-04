from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from data.patients import PATIENT_DATA

router = Router()

@router.callback_query(F.data.startswith("share_"))
async def cb_share(call: CallbackQuery):
    patient_id = call.data.split("_")[1]
    patient = PATIENT_DATA.get(patient_id, PATIENT_DATA["1"])
    
    share_link = f"https://t.me/navimed_bot?start=relative_{patient_id}"
    
    text = (
        f"👨‍👩‍👧 **Семейный доступ (Shared Care)**\n\n"
        f"Мы знаем, что пожилым людям бывает сложно пользоваться приложениями. Отправьте эту ссылку сыну или дочери:\n\n"
        f"`{share_link}`\n\n"
        f"По этой ссылке они получат доступ к вашему маршруту и смогут помочь вам с записью к врачу ({patient['specialist']})."
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 Отправить родственнику", url=f"https://t.me/share/url?url={share_link}&text=Маршрут для {patient['full_name']}")]
    ])
    
    await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await call.answer()