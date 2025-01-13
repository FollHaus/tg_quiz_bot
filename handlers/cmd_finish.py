from aiogram import F
from aiogram import types
from aiogram.types import CallbackQuery

from aiogram import Router
from aiogram.filters import Command

from handlers.answer_callback import finish_game

router = Router()


# Заканчиваем игру
@router.message(F.text == 'Закончить игру')
@router.message(Command('finish'))
async def cmd_finish(message: types.Message):
    # Создаем "фейковый" CallbackQuery
    finish_callback = CallbackQuery(
        id="finish_callback_id",
        from_user=message.from_user,
        chat_instance="finish_callback_instance",
        message=message,
        data="finish_game",
    )
    # Вызываем callback-обработчик напрямую
    await finish_game(finish_callback)
