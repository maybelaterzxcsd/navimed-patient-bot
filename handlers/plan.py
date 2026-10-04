from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import get_back_keyboard

router = Router()

# Моковые данные (в реальности берутся из БД)
PATIENT_PLANS = {
    "1": [
        "1. Завтра, 10:00 — Первичная консультация онколога-маммолога",
        "2. Через 2 недели — Биопсия образования (направление будет отправлено)",
        "3. Через 3 месяца — Контрольное УЗИ для оценки динамики"
    ],
    "2": [
        "1. Через неделю — Консультация пульмонолога",
        "2. Через 3 месяца — Повторное КТ для контроля динамики узла",
        "3. Через 6 месяцев — Плановый осмотр терапевта"
    ],
    "3": [
        "1. Сегодня, 16:00 — Срочный прием терапевта",
        "2. Через 3 дня — Контрольный рентген после начала лечения",
        "3. Через 2 недели — Повторная консультация для оценки выздоровления"
    ],
    "4": [
        "1. Через 2 недели — Плановый прием эндокринолога",
        "2. Через месяц — Сдача анализа на гликированный гемоглобин",
        "3. Через 3 месяца — Повторная консультация для коррекции терапии"
    ]
}

PATIENT_QUESTIONS = {
    "1": [
        "1. «Нужна ли мне биопсия при текущем размере образования (15 мм)?»",
        "2. «Можно ли мне продолжать принимать мои текущие лекарства?»",
        "3. «Какие симптомы должны заставить меня вызвать скорую до следующего приема?»"
    ],
    "2": [
        "1. «Какова вероятность, что узел доброкачественный?»",
        "2. «Нужны ли мне дополнительные анализы крови?»",
        "3. «Можно ли мне заниматься спортом при таком диагнозе?»"
    ],
    "3": [
        "1. «Нужны ли мне антибиотики или можно обойтись без них?»",
        "2. «Как долго мне придется находиться на больничном?»",
        "3. «Какие симптомы должны заставить меня вызвать скорую?»"
    ],
    "4": [
        "1. «Нужно ли мне менять дозировку текущих препаратов?»",
        "2. «Какая диета рекомендуется при моем диагнозе?»",
        "3. «Как часто мне нужно проверять уровень сахара?»"
    ]
}

@router.callback_query(F.data.startswith("plan_"))
async def cb_plan(call: CallbackQuery):
    patient_id = call.data.split("_")[1]
    plan = PATIENT_PLANS.get(patient_id, PATIENT_PLANS["1"])
    
    text = (
        "📆 **Ваш персональный план наблюдения от ИИ:**\n\n"
        + "\n".join(plan)
        + "\n\n_Мы будем мягко напоминать вам о каждом шаге, чтобы вы не потерялись в системе._"
    )
    
    await call.message.edit_text(text, reply_markup=get_back_keyboard(patient_id), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data.startswith("questions_"))
async def cb_questions(call: CallbackQuery):
    patient_id = call.data.split("_")[1]
    questions = PATIENT_QUESTIONS.get(patient_id, PATIENT_QUESTIONS["1"])
    
    text = (
        "❓ **ИИ составил для вас 3 главных вопроса к врачу:**\n\n"
        + "\n".join(questions)
        + "\n\n_Сохраните этот список или покажите его врачу на экране телефона._"
    )
    
    await call.message.edit_text(text, reply_markup=get_back_keyboard(patient_id), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data.startswith("book_"))
async def cb_book(call: CallbackQuery):
    patient_id = call.data.split("_")[1]
    
    text = (
        "⏳ **Мы предварительно забронировали для вас место:**\n\n"
        "🗓 Завтра, 10:00\n"
        "👨‍️ Онколог-маммолог (Зав. отделением)\n\n"
        "Бронь держится **2 часа**. Если вы не подтвердите запись нажатием кнопки ниже, слот будет передан другому пациенту из листа ожидания.\n\n"
        "✅ **Нажмите кнопку ниже, чтобы подтвердить запись в 1 клик**"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить запись", callback_data=f"confirm_{patient_id}")],
        [InlineKeyboardButton(text="← Назад в меню", callback_data=f"menu_{patient_id}")]
    ])
    
    await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data.startswith("confirm_"))
async def cb_confirm(call: CallbackQuery):
    patient_id = call.data.split("_")[1]
    
    text = (
        "✅ **Запись подтверждена!**\n\n"
        "Мы отправили вам напоминание за 24 часа до приема.\n"
        "Не забудьте взять с собой:\n"
        "• Паспорт и полис ОМС\n"
        "• Диск или пленку с текущим снимком\n"
        "• Предыдущие заключения (если есть)\n\n"
        "Ждем вас завтра в 10:00!"
    )
    
    await call.message.edit_text(text, reply_markup=get_back_keyboard(patient_id), parse_mode="Markdown")
    await call.answer("Запись подтверждена!")