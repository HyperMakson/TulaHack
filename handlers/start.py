from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.simple_keyboard import make_row_keyboard
from keyboards.start_keyboard import start_row_keyboard
from db_connect import dbworker
import pandas as pd
from datetime import datetime

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
    input_specialization = State()
    input_specialist = State()
    input_date = State()
    input_time = State()
    input_user_fio = State()
    input_user_snils = State()
    input_user_polis = State()
    del_state = State()

'''Получаем следующие 9 будних дней'''

dateList = pd.bdate_range(start = datetime.today(), periods = 9).to_pydatetime().tolist()
date_arr =[]
for date in dateList:
    date_arr.append(date.strftime("%d.%m"))


'''Списки значений кнопок'''



specialization_arr = db.get_spec()
specialist_arr = db.get_docs()
time_arr = ["07:30", "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00",
            "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30","15:00",
            "15:30", "16:00", "16:30", "17:00"]
items = []

'''Начальное меню бота'''
@router.message(Command("start"))
@router.message(F.text.lower() == "старт")
@router.message(F.text.lower() == "начать")
async def cmd_start(message: Message):
    await message.answer(
        text="Здравствуйте! Вас приветствует клиника AmNyam\n"
            "Вы можете выбрать одно из действий, представленных ниже",
        reply_markup=start_row_keyboard()
    )

'''Команда отмена'''
@router.message(Command("cancel"))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Действие отменено", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        text="Здравствуйте! Вас приветствует клиника AmNyam\n"
            "Вы можете выбрать одно из действий, представленных ниже",
        reply_markup=start_row_keyboard()
    )

'''Заполнение записи к врачу'''
@router.callback_query(F.data == "appointment")
async def start_appointment(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Выберете специализацию врача", reply_markup=make_row_keyboard(specialization_arr))
    await state.set_state(Clinic.specialization)
    await callback.answer()

@router.message(Clinic.specialization, F.text.in_(specialization_arr))
async def specialization_chosen(message: Message, state: FSMContext):
    try:
        await state.update_data(chosen_specialization=message.text.lower())
        user_data = await state.get_data()
        global specialist_arr
        specialist_arr = db.get_all_docs(user_data['chosen_specialization'])
        await message.answer(text="Хорошо. Выберете конкретного врача.", reply_markup=make_row_keyboard(specialist_arr))
        await state.set_state(Clinic.specialist)
    except:
        await state.clear()
        await message.answer(text="Произошла ошибка", reply_markup=ReplyKeyboardRemove())
        await message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )

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
    try:
        await state.update_data(chosen_date=message.text.lower())
        user_data = await state.get_data()
        busy_time_arr = db.get_time_date(user_data['chosen_date'])
        '''Получение  свободного времени'''
        free_time_arr = [x for x in time_arr if x not in busy_time_arr]
        '''Проверка если свободного времени нет'''
        if free_time_arr == []:
            await message.answer(text="На эту дату нет сводного времени\nПожалуйста, выберите свободную дату", reply_markup=make_row_keyboard(date_arr))
        else:
            await message.answer(text="Хорошо. Выберете свободное время.", reply_markup=make_row_keyboard(free_time_arr))
            await state.set_state(Clinic.time)
    except:
        await state.clear()
        await message.answer(text="Произошла ошибка", reply_markup=ReplyKeyboardRemove())
        await message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )

@router.message(Clinic.date)
async def date_chosen_incorrectly(message: Message):
    await message.answer(text="Такой даты нет\nПожалуйста, выберите свободную дату", reply_markup=make_row_keyboard(date_arr))

@router.message(Clinic.time, F.text.in_(time_arr))
async def time_chosen(message: Message, state: FSMContext):
    try:
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
                    f"Полис: {date_user[2]}\n", reply_markup=ReplyKeyboardRemove()
            )
            db.add_appoint(user_data['chosen_specialist'], message.from_user.id, user_data['chosen_date'], user_data['chosen_time'])
            await state.clear()
            await message.answer(
                text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                    "Вы можете выбрать одно из действий, представленных ниже",
                reply_markup=start_row_keyboard()
            )
    except:
        await state.clear()
        await message.answer(text="Произошла ошибка", reply_markup=ReplyKeyboardRemove())
        await message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )
         
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
    try:
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
        await message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )
    except:
        await state.clear()
        await message.answer(text="Произошла ошибка", reply_markup=ReplyKeyboardRemove())
        await message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )



'''Кнопка мои записи'''
@router.callback_query(F.data == "my_notes")
async def start_appointment(callback: CallbackQuery):
    try:
        notes_user = db.get_all_appoints_user(callback.from_user.id)
        for i in range(len(notes_user)):
            notes_user_arr = [str(x) for x in notes_user[i]]
            notes_user_join = '\n'.join(notes_user_arr)
            await callback.message.answer(notes_user_join)
        '''Клавиатура удалить запись и повторный приём'''
        buttons = [
            [InlineKeyboardButton(text="Запись на повторный приём", callback_data="appointment")],
            [InlineKeyboardButton(text="Удалить запись", callback_data="del_appointment")],
            [InlineKeyboardButton(text="Отмена", callback_data="cancel_appointment")]
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.answer(text="Вы можете сделать одно из следующих действий", reply_markup=keyboard)
        await callback.answer()
    except:
        await callback.message.answer(text="Произошла ошибка", reply_markup=ReplyKeyboardRemove())
        await callback.message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )
        await callback.answer()

@router.callback_query(F.data == "del_appointment")
async def cmd_del_appointment(callback: CallbackQuery, state: FSMContext):
    try:
        notes_user = db.get_all_appoints_user(callback.from_user.id)
        print(notes_user)
        global items
        items = []
        for i in range(len(notes_user)):
            notes_user_arr = [str(x) for x in notes_user[i]]
            print(notes_user_arr)
            length = len(notes_user_arr[0])
            print(length)
            if length > 9:
                diff = length - 8
                items.append(notes_user_arr[0][-diff:])
            else:
                items.append(notes_user_arr[0][-1])
        print(items)
        await callback.message.answer("Выберите какую запись удалить", reply_markup=make_row_keyboard(items))
        await state.set_state(Clinic.del_state)
        await callback.answer()
    except:
        await callback.message.answer(text="Произошла ошибка", reply_markup=ReplyKeyboardRemove())
        await callback.message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )
        await callback.answer()

@router.callback_query(F.data == "cancel_appointment")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Действие отменено", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        text="Здравствуйте! Вас приветствует клиника AmNyam\n"
            "Вы можете выбрать одно из действий, представленных ниже",
        reply_markup=start_row_keyboard()
    )

@router.message(Clinic.del_state)
async def del_from_db(message: Message, state: FSMContext):
    try:
        await state.update_data(chosen_id_del=message.text.lower())
        user_data = await state.get_data()
        db.del_appoint(user_data['chosen_id_del'])
        await message.answer(text="Хорошо. Запись удалена", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        await message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )
    except:
        await state.clear()
        await message.answer(text="Произошла ошибка", reply_markup=ReplyKeyboardRemove())
        await message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )


'''Кнопка анализы'''
@router.callback_query(F.data == "my_tests")
async def start_appointment(callback: CallbackQuery):
    try:
        tests = db.get_file(callback.from_user.id)
        '''Проверка готовности анализов'''
        if tests != []:
            await callback.message.answer(text='Вот ваши анализы', reply_markup=ReplyKeyboardRemove())
            for test in tests:
                file = FSInputFile(test, filename="Analiz.pdf")
                await callback.message.answer_document(file)
        else:
            await callback.message.answer(text='У вас нет анализов или они ещё не готовы', reply_markup=ReplyKeyboardRemove())  
        await callback.answer()
    except:
        await callback.message.answer(text="Произошла ошибка", reply_markup=ReplyKeyboardRemove())
        await callback.message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )
        await callback.answer()

'''Кнопка симптомы'''
@router.callback_query(F.data == "symptoms")
async def start_symptoms(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ваши симптомы")
    await state.set_state(Clinic.input_symptoms)
    await callback.answer()

@router.message(Clinic.input_symptoms)
async def symptoms_chosen(message: Message, state: FSMContext):
    try:
        await state.update_data(chosen_symptoms=message.text.lower())
        symptoms_data = await state.get_data()
        symptoms = symptoms_data['chosen_symptoms']
        symptoms_split = str(symptoms).split()
        exist_sympton = db.select_symptom()
        symptom_finden = []
        id_finden = []
        specialist_finden = []
        for i in symptoms_split:
            i_srez = i[0:-1]
            if i_srez in exist_sympton:
                symptom_finden.append(i_srez)
                id_find = db.select_id(i_srez)
                id_finden.append(id_find[0])
        for i in id_finden:
            specialist_for_symptom = db.find_specialist_for_symptom(int(i))
            specialist_finden.append(specialist_for_symptom[0])
        if len(specialist_finden) == 0:
            specialist_finden.append("терапевт")
        await message.answer(text="По вашим симптомам найдены следующие специальности врачей\nВыберите, к кому записаться", reply_markup=make_row_keyboard(specialist_finden))
        await state.set_state(Clinic.input_specialization)
    except:
        await state.clear()
        await message.answer(text="Запишитесь к терапевту", reply_markup=ReplyKeyboardRemove())
        await message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )

@router.message(Clinic.input_specialization, F.text.in_(specialization_arr))
async def specialization_chosen(message: Message, state: FSMContext):
    try:
        await state.update_data(chosen_specialization=message.text.lower())
        user_data = await state.get_data()
        global specialist_arr
        specialist_arr = db.get_all_docs(user_data['chosen_specialization'])
        await message.answer(text="Хорошо. Выберете конкретного врача.", reply_markup=make_row_keyboard(specialist_arr))
        await state.set_state(Clinic.input_specialist)
    except:
        await state.clear()
        await message.answer(text="Произошла ошибка", reply_markup=ReplyKeyboardRemove())
        await message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )

@router.message(Clinic.input_specialization)
async def specialization_chosen_incorrectly(message: Message):
    await message.answer(text="Я не знаю такой специальности\nПожалуйста, напишите другую специальность", reply_markup=make_row_keyboard(specialization_arr))

@router.message(Clinic.input_specialist, F.text.in_(specialist_arr))
async def specialist_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_specialist=message.text.lower())
    await message.answer(text="Хорошо. Выберете свободную дату.", reply_markup=make_row_keyboard(date_arr))
    await state.set_state(Clinic.input_date)

@router.message(Clinic.input_specialist)
async def specialist_chosen_incorrectly(message: Message):
    await message.answer(text="Я не знаю такого специалиста\nПожалуйста, напишите другого специалиста", reply_markup=make_row_keyboard(specialist_arr))

@router.message(Clinic.input_date, F.text.in_(date_arr))
async def date_chosen(message: Message, state: FSMContext):
    try:
        await state.update_data(chosen_date=message.text.lower())
        user_data = await state.get_data()
        busy_time_arr = db.get_time_date(user_data['chosen_date'])
        '''Получение  свободного времени'''
        free_time_arr = [x for x in time_arr if x not in busy_time_arr]
        '''Проверка если свободного времени нет'''
        if free_time_arr == []:
            await message.answer(text="На эту дату нет сводного времени\nПожалуйста, выберите свободную дату", reply_markup=make_row_keyboard(date_arr))
        else:
            await message.answer(text="Хорошо. Выберете свободное время.", reply_markup=make_row_keyboard(free_time_arr))
            await state.set_state(Clinic.input_time)
    except:
        await state.clear()
        await message.answer(text="Произошла ошибка", reply_markup=ReplyKeyboardRemove())
        await message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )

@router.message(Clinic.input_date)
async def date_chosen_incorrectly(message: Message):
    await message.answer(text="Такой даты нет\nПожалуйста, выберите свободную дату", reply_markup=make_row_keyboard(date_arr))

@router.message(Clinic.input_time, F.text.in_(time_arr))
async def time_chosen(message: Message, state: FSMContext):
    try:
        await state.update_data(chosen_time=message.text.lower())
        if db.user_exists(message.from_user.id) == False:
            '''Проверка на наличие пользователя в базе данных'''
            await message.answer(text="Хорошо. Введите ФИО полностью.", reply_markup=ReplyKeyboardRemove())
            await state.set_state(Clinic.input_user_fio)
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
            db.add_appoint(user_data['chosen_specialist'], message.from_user.id, user_data['chosen_date'], user_data['chosen_time'])
            await state.clear()
            await message.answer(
                text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                    "Вы можете выбрать одно из действий, представленных ниже",
                reply_markup=start_row_keyboard()
            )
    except:
        await state.clear()
        await message.answer(text="Произошла ошибка", reply_markup=ReplyKeyboardRemove())
        await message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )
     
@router.message(Clinic.input_time)
async def time_chosen_incorrectly(message: Message):
    await message.answer(text="Такого времени нет\nПожалуйста, выберите свободное время", reply_markup=make_row_keyboard(time_arr))

@router.message(Clinic.input_user_fio)
async def FIO_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_fio=message.text.lower())
    await message.answer(text="Хорошо. Введите ваш СНИЛС.")
    await state.set_state(Clinic.user_snils)

@router.message(Clinic.input_user_snils)
async def snils_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_snils=message.text.lower())
    await message.answer(text="Хорошо. Введите ваш номер Полиса.")
    await state.set_state(Clinic.user_polis)

@router.message(Clinic.input_user_polis)
async def polis_chosen(message: Message, state: FSMContext):
    try:
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
        await message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )
    except:
        await state.clear()
        await message.answer(text="Произошла ошибка", reply_markup=ReplyKeyboardRemove())
        await message.answer(
            text="Здравствуйте! Вас приветствует клиника AmNyam\n"
                "Вы можете выбрать одно из действий, представленных ниже",
            reply_markup=start_row_keyboard()
        )