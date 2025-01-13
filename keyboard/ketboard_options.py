from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types


# Создаем кнопки с вариантами ответов
def generate_keyboard_options(answer_options, correct_answer):
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=f'answer_correct|{option}' if option == correct_answer else f'answer_wrong|{option}')
        )
    builder.adjust(1)
    return builder.as_markup()

