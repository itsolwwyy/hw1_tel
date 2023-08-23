from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import random, os, logging

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="start")
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}! Выбери от 1 до 3.")

@dp.message_handler(text=[1,2,3])
async def select(message:types.Message):
        number = random.randint(1,3)
        user = int(message.text)
        if user ==number:
            await message.answer(f"Вы угадали. Бот выбрал: {number}")
            await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
        else:
            await message.reply(f" Вы проиграли. Бот выбрал: {number}")
            await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')

@dp.message_handler(text="want_to_play_more")
async def want_to_play_more(message:types.Message):
     await message.answer("Да")
     await message.answer("Нет")

executor.start_polling(dp)   