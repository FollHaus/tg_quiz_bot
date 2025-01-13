import json
import aiofiles
import aiosqlite


# Создаём базу данных пользователей
async def create_users_table():
    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect('quiz_state.db') as db:
        # Выполняем SQL-запрос к базе данных
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER, correct_answer INTEGER, incorrect_answer INTEGER)'''
        )
        # Сохраняем изменения
        await db.commit()


# Создаём базу данных вопросов
async def create_table_quiz():
    async with aiosqlite.connect('questions_db.db') as db:
        await db.execute(
            'CREATE TABLE IF NOT EXISTS questions (quest_id INTEGER PRIMARY KEY, question TEXT NOT NULL UNIQUE, options TEXT NOT NULL,correct_option INTEGER NOT NULL)')
        await db.commit()


# Добавляем вопросы в базу данных
async def add_data_questions_db(json_path):
    async with aiosqlite.connect('questions_db.db') as db:
        async with aiofiles.open(json_path, 'r', encoding='utf-8') as file:
            questions_json = await file.read()
            questions = json.loads(questions_json)
            for question in questions:
                await db.execute(
                    'INSERT OR IGNORE INTO questions (quest_id ,question, options, correct_option) VALUES (?, ?, ?,?)',
                    (question['id'], question['question'], json.dumps(question['options'], ensure_ascii=False),
                     question['correct_option']))
        await db.commit()


# Добавляем пользователя в базу данных и присваиваем индекс вопроса
async def update_user_db(user_id, questions_index, correct_answer=0, incorrect_answer=0):
    async with aiosqlite.connect('quiz_state.db') as db:
        await db.execute(
            'INSERT OR REPLACE INTO quiz_state (user_id, question_index,correct_answer,incorrect_answer) VALUES (?, ?, ?, ?)',
            (user_id, questions_index, correct_answer, incorrect_answer))
        await db.commit()


# Проверяем есть ли пользователь в базе и выдаем ему вопрос
async def get_question(user_id):
    async with aiosqlite.connect('quiz_state.db') as quiz_state_db, \
            aiosqlite.connect('questions_db.db') as questions_db:
        async with quiz_state_db.execute(
                'SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return 0, 0  # В базе нет пользователя
            question_index = row[0]

        async with questions_db.execute(
                'SELECT question, options,correct_option FROM questions WHERE quest_id = (?)',
                (question_index,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return 0, 0, 0,  # В базе нет вопросов по указанному индексу
            question = row[0]
            options = json.loads(row[1])
            correct_option = row[2]
            return question, options, correct_option


# Получаем текущий индекс у пользователя
async def get_user_question_index(user_id):
    async with aiosqlite.connect('quiz_state.db') as db:
        async with db.execute(
                'SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return 0  # В базе нет пользователя
            return row[0]


# Получаем ответы пользователя
async def get_answer_user(user_id):
    async with aiosqlite.connect('quiz_state.db') as db:
        async with db.execute(
                'SELECT correct_answer, incorrect_answer FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return 0, 0  # В базе нет пользователя
            correct_answer, incorrect_answer = row
            return correct_answer, incorrect_answer


# Получаем весь список вопросов
async def get_all_questions():
    async with aiosqlite.connect('questions_db.db') as db:
        async with db.execute('SELECT * FROM questions') as cursor:
            rows = await cursor.fetchall()
            return rows
