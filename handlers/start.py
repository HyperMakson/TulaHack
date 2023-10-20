from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.simple_keyboard import make_row_keyboard

router = Router()

class Clinic(StatesGroup):
    specialization = State()
    specialist = State()
    date = State()
    user = State()

specialization_arr = ["Терапевт", "Уролог", "Стоматолог", "Офтальмолог"]
specialist_arr = ["Сорокин", "Цыбуля", "Генералов", "Митяев", "Данилов"]
date_arr = ["18:00", "18:30", "19:00"]


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
    await message.answer(text="Хорошо. Выберете свободную дату и время.", reply_markup=make_row_keyboard(date_arr))
    await state.set_state(Clinic.date)

@router.message(Clinic.specialist)
async def specialist_chosen_incorrectly(message: Message):
    await message.answer(text="Я не знаю такого специалиста\nПожалуйста, напишите другого специалиста", reply_markup=make_row_keyboard(specialist_arr))

@router.message(Clinic.date, F.text.in_(date_arr))
async def date_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_date=message.text.lower())
    await message.answer(text="Хорошо. Введите свои данные (ФИО, СНИЛС, Полис).")
    await state.set_state(Clinic.user)

@router.message(Clinic.date)
async def date_chosen_incorrectly(message: Message):
    await message.answer(text="Такой даты нет\nПожалуйста, выберите свободную дату")





@router.callback_query(F.data == "my_notes")
async def start_appointment(callback: CallbackQuery):
    await callback.message.answer("Это мои записи")
    await callback.answer()

@router.callback_query(F.data == "my_tests")
async def start_appointment(callback: CallbackQuery):
    await callback.message.answer("Это мои анализы")
    await callback.answer()

@router.callback_query(F.data == "symptoms")
async def start_appointment(callback: CallbackQuery):
    await callback.message.answer("Это симптомы")
    await callback.answer()