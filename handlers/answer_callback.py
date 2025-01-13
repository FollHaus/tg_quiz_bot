from aiogram import F
from aiogram import Router
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from controllers.db_controller import get_user_question_index, update_user_db, get_all_questions, get_answer_user
from controllers.quiz_controller import next_question

router = Router()


# Обработка кнопок ответов
@router.callback_query(F.data.startswith("answer_"))
async def answer_callback(callback: types.CallbackQuery):
    action, button_text = callback.data.split('|')
    action_type = action.split('_')[1]
    current_index = await get_user_question_index(callback.from_user.id)
    correct, incorrect = await get_answer_user(callback.from_user.id)
    all_questions = await get_all_questions()
    await callback.message.answer(f'Пройдено вопросов {current_index} из {len(all_questions)}')
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    if action_type == 'correct':
        await callback.message.answer(f'{button_text} верный ответ!')
        current_index += 1
        correct += 1
        await update_user_db(callback.from_user.id, current_index, correct_answer=correct,
                             incorrect_answer=incorrect)
        if current_index <= len(all_questions):
            await next_question(callback.from_user.id, callback.message)
        else:
            await finish_game(callback)
    else:
        await callback.message.answer(f'{button_text} не верный ответ!')
        current_index += 1
        incorrect += 1
        await update_user_db(callback.from_user.id, current_index, correct_answer=correct,
                             incorrect_answer=incorrect)
        if current_index <= len(all_questions):
            await next_question(callback.from_user.id, callback.message)
        else:
            await finish_game(callback)


# Выводим статистику по окончанию игры
@router.callback_query(F.data == "finish_game")
async def finish_game(callback: types.CallbackQuery):
    correct, incorrect = await get_answer_user(callback.from_user.id)
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Начать игру'))
    # Вывод статистики
    await callback.message.answer(
        f'Ваша статистика ответов:\nВерных: {correct}, Неверных: {incorrect}.',
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
