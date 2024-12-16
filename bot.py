import logging

from os import getenv
from dotenv import load_dotenv, find_dotenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, BotCommand

import translate

load_dotenv(find_dotenv())

TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO, 
                    filename="py_log.log",
                    filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

# Создаем асинхронную функцию
async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Запустить бота'),
        BotCommand(command='/help',
                   description='Справка по работе бота')
        ]
    await bot.set_my_commands(main_menu_commands)

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    msg = f'Привет, {user_name}'
    logging.info(f'{user_name} - {user_id} запустил бота')
    await bot.send_message(chat_id=user_id, text=msg)
    await message.answer('Напиши мне Фамилию Имя Отчество и я отдам их в латинице')

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Отправьте мне ФИО в кириллице, а я верну их на латинице '
        'в соответствии с Приказом МИД России от 12.02.2020 № 2113'
    )

# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    original_text = message.text
    transliteration_text = translate.transliteration(original_text)
    logging.info(f'{user_name} {user_id}: {original_text} -> {transliteration_text}')
    await message.answer(text=transliteration_text)

if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)