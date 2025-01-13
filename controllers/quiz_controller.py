from controllers.db_controller import update_user_db, get_question
from keyboard.ketboard_options import generate_keyboard_options


# Добавляем пользователя в базу и получаем для него вопрос
async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 1
    await update_user_db(user_id, current_question_index)
    await next_question(user_id, message)


# Переход к след. вопросу

async def next_question(user_id, message):
    question, options, correct_option = await get_question(user_id)
    kb = generate_keyboard_options(options, options[correct_option])
    await message.answer(question, reply_markup=kb)
