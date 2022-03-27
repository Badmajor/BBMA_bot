from aiogram.types import Message

from data.config import ADMIN
from loader import dp, bot


@dp.message(commands=["start"])
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await bot.send_message(chat_id=ADMIN, text='работает')