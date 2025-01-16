import asyncio
import logging
from aiogram import types

from aiogram import Bot, Dispatcher, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from controllers.db_controller import create_users_table, create_table_quiz, add_data_questions_db
from handlers import cmd_start, cmd_quiz, answer_callback, cmd_finish

logging.basicConfig(level=logging.INFO)

API_TOKEN = 'YOUR_TOKEN'
# Список вопросов
DATA_QUESTIONS = 'source/data_questions.json'

dp = Dispatcher()


# Главная функция
async def main():
    bot = Bot(token=API_TOKEN)
    # Запускаем создание таблиц баз данных
    await create_users_table()
    await create_table_quiz()
    # Записываем данные в базу
    await add_data_questions_db(DATA_QUESTIONS)
    # Регистрируем пути
    dp.include_routers(cmd_start.router, cmd_quiz.router, answer_callback.router, cmd_finish.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
