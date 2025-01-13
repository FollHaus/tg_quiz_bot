from aiogram import types
from aiogram import Router
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()


# Привет
@router.message(Command('start'))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Начать игру'))
    await message.answer("Я QUIZ бот!", reply_markup=builder.as_markup(resize_keyboard=True))
