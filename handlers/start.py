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