from aiogram import F
from aiogram import types
from aiogram import Router
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from controllers.quiz_controller import new_quiz

router = Router()

# Начинаем игру
@router.message(F.text == 'Начать игру')
@router.message(Command('quiz'))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Закончить игру'))
    await message.answer("Давайте начнём! Первый вопрос:...", reply_markup=builder.as_markup(resize_keyboard=True))
    await new_quiz(message)
