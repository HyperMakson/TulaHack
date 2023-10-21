from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.simple_keyboard import make_row_keyboard
from db_connect import dbworker

'''Подключение к базе данных'''
db = dbworker('baza.db')

router = Router()

'''Инициализация состояний'''
class Clinic(StatesGroup):
    specialization = State()
    specialist = State()
    date = State()
    time = State()
    user_fio = State()
    user_snils = State()
    user_polis = State()

    input_symptoms = State()

'''Списки значений кнопок'''
specialization_arr = ["Венеролог", "Вирусолог", "Гинеколог", "Дерматолог", "Терапевт", "Диетолог", "Акушер", "Кардиолог", "Нарколог", "Педиатр", "Хирург", "Лор"]
#specialist_arr = db.get_all_docs()
specialist_arr = ["Цыбуля", "Сорокин", "Митяев", "Генералов", "Данилов"]
date_arr = ["21.10", "22.10", "23.10", "24.10", "25.10", "26.10", "27.10"]
time_arr = ["07:30", "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00",
            "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30","15:00",
            "15:30", "16:00", "16:30", "17:00"]

dict_symptoms = {
    "Венеролог": "gfh"
}

'''Начальное меню бота'''
@router.message(Command("start"))
async def cmd_start(message: Message):
    buttons = [
        [InlineKeyboardButton(text="Запись на приём", callback_data="appointment")],
        [InlineKeyboardButton(text="Мои записи", callback_data="my_notes")],
        [InlineKeyboardButton(text="Мои анализы", callback_data="my_tests")],
        [InlineKeyboardButton(text="Симптомы", callback_data="symptoms")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Здравствуйте! Вы попали", reply_markup=keyboard)

'''Заполнение записи к врачу'''
@router.callback_query(F.data == "appointment")
async def start_appointment(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Выберете специализацию врача", reply_markup=make_row_keyboard(specialization_arr))
    await state.set_state(Clinic.specialization)
    await callback.answer()

@router.message(Clinic.specialization, F.text.in_(specialization_arr))
async def specialization_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_specialization=message.text.lower())
    await message.answer(text="Хорошо. Выберете конкретного врача.", reply_markup=make_row_keyboard(specialist_arr))
    await state.set_state(Clinic.specialist)

@router.message(Clinic.specialization)
async def specialization_chosen_incorrectly(message: Message):
    await message.answer(text="Я не знаю такой специальности\nПожалуйста, напишите другую специальность", reply_markup=make_row_keyboard(specialization_arr))

@router.message(Clinic.specialist, F.text.in_(specialist_arr))
async def specialist_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_specialist=message.text.lower())
    await message.answer(text="Хорошо. Выберете свободную дату.", reply_markup=make_row_keyboard(date_arr))
    await state.set_state(Clinic.date)

@router.message(Clinic.specialist)
async def specialist_chosen_incorrectly(message: Message):
    await message.answer(text="Я не знаю такого специалиста\nПожалуйста, напишите другого специалиста", reply_markup=make_row_keyboard(specialist_arr))

@router.message(Clinic.date, F.text.in_(date_arr))
async def date_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_date=message.text.lower())
    await message.answer(text="Хорошо. Выберете свободное время.", reply_markup=make_row_keyboard(time_arr))
    await state.set_state(Clinic.time)

@router.message(Clinic.date)
async def date_chosen_incorrectly(message: Message):
    await message.answer(text="Такой даты нет\nПожалуйста, выберите свободную дату", reply_markup=make_row_keyboard(date_arr))

@router.message(Clinic.time, F.text.in_(time_arr))
async def time_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_time=message.text.lower())
    if db.user_exists(message.from_user.id) == False:
       '''Проверка на наличие пользователя в базе данных'''
       await message.answer(text="Хорошо. Введите ФИО полностью.", reply_markup=ReplyKeyboardRemove())
       await state.set_state(Clinic.user_fio)
    else:
        user_data = await state.get_data()
        '''Получение данных о пользователе из базы данных'''
        date_user = db.get_user(message.from_user.id)
        await message.answer(
        text=f"Специализация: {user_data['chosen_specialization']}\n"
            f"Специалист: {user_data['chosen_specialist']}\n"
            f"Дата: {user_data['chosen_date']}\n"
            f"Время: {user_data['chosen_time']}\n"
            f"Данные пользователя:\n"
            f"ФИО: {date_user[0]}\n"
            f"СНИЛС: {date_user[1]}\n"
            f"Полис: {date_user[2]}\n", reply_markup=ReplyKeyboardRemove())
        await state.clear()       
@router.message(Clinic.time)
async def time_chosen_incorrectly(message: Message):
    await message.answer(text="Такого времени нет\nПожалуйста, выберите свободное время", reply_markup=make_row_keyboard(time_arr))

@router.message(Clinic.user_fio)
async def FIO_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_fio=message.text.lower())
    await message.answer(text="Хорошо. Введите ваш СНИЛС.")
    await state.set_state(Clinic.user_snils)

@router.message(Clinic.user_snils)
async def snils_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_snils=message.text.lower())
    await message.answer(text="Хорошо. Введите ваш номер Полиса.")
    await state.set_state(Clinic.user_polis)

@router.message(Clinic.user_polis)
async def polis_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_polis=message.text.lower())
    user_data = await state.get_data()
    print(user_data['chosen_specialist'])
    await message.answer(
        text=f"Специализация: {user_data['chosen_specialization']}\n"
            f"Специалист: {user_data['chosen_specialist']}\n"
            f"Дата: {user_data['chosen_date']}\n"
            f"Время: {user_data['chosen_time']}\n"
            f"Данные пользователя:\n"
            f"ФИО: {user_data['chosen_fio']}\n"
            f"СНИЛС: {user_data['chosen_snils']}\n"
            f"Полис: {user_data['chosen_polis']}\n"
    )
    db.add_appoint(user_data['chosen_specialist'], message.from_user.id, user_data['chosen_date'], user_data['chosen_time'])
    db.add_user(message.from_user.id, user_data['chosen_fio'], user_data['chosen_snils'], user_data['chosen_polis'])
    await state.clear()




@router.callback_query(F.data == "my_notes")
async def start_appointment(callback: CallbackQuery):
    await callback.message.answer("Вот ваши записи")
    await callback.answer()






@router.callback_query(F.data == "my_tests")
async def start_appointment(callback: CallbackQuery):
    await callback.message.answer("Это мои анализы")
    await callback.answer()






@router.callback_query(F.data == "symptoms")
async def start_symptoms(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ваши симптомы")
    await state.set_state(Clinic.input_symptoms)
    await callback.answer()

@router.message(Clinic.input_symptoms)
async def symptoms_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_symptoms=message.text.lower())
    symptoms_data = await state.get_data()
    symptoms = symptoms_data['chosen_symptoms']
    symptoms_split = str(symptoms).split()
    for i in symptoms_split:
        if i == dict_symptoms['Венеролог']:
            print("ff")
    print(symptoms)
    await state.clear()




@router.message(Command("cancel"))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Действие отменено", reply_markup=ReplyKeyboardRemove())