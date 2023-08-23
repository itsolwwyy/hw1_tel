from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
import os, time, logging

from keyboards import start_button
from dotabase import connection, cursor

load_dotenv('.env')

bot = Bot(token=str(os.environ.get('token')))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    cursor.execute(f"SELECT * FROM users WHERE id = {message.from_user.id};")
    result = cursor.fetchall()
    print(result)
    if result == []:
        cursor.execute(f"""INSERT INTO users VALUES ({message.from_user.id}, '{message.from_user.username}',
                    '{message.from_user.first_name}', '{message.from_user.last_name}', '{time.ctime()}');""")
        cursor.connection.commit()
    await message.answer(f"Здравствуйте, {message.from_user.full_name}\nЯ вам помогу узнать наш город Ош в мельчайших подробностях\nЧто вас интересует на данный момент?", reply_markup=start_button)

class MailingState(StatesGroup):
    text = State()

@dp.message_handler(commands='mailing')
async def get_mailing_text(message:types.Message):
    await message.reply("Введите текст для рассылки")
    await MailingState.text.set()

@dp.message_handler(text='Информация')
async def information(message:types.Message):
    await message.answer("""Ош — город республиканского подчинения в Киргизии, административный центр Ошской области.
Ош — второй по численности населения город Киргизии после Бишкека, крупнейший город юга страны, официально именуемый «южной столицей». 
18 декабря 2018 года город Ош объявлен Культурной столицей тюркского мира на 2019 год.""")
    
    
class SightsState(StatesGroup):
    title = State()
    descriptions = State()
    location = State()
    longitude = State()
    latitude = State()

@dp.message_handler(commands='add_sights')
async def get_sigths_title(message:types.Message):
      if message.answer('Введите заголовок'):
        await SightsState.title.set()
    
@dp.message_handler(state=SightsState.title)
async def get_sigths_description(message:types.Message, state:FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите описание")
    await SightsState.descriptions.set()

@dp.message_handler(state=SightsState.descriptions)
async def get_email_adress(message:types.Message, state:FSMContext):
    await state.update_data(descriptions=message.text)
    await message.answer("Введите долготу") 
    await SightsState.longitude.set()

@dp.message_handler(state=SightsState.descriptions)
async def get_email_adress(message:types.Message, state:FSMContext):
    await state.update_data(descriptions=message.text)
    await message.answer("Введите широту") 
    await SightsState.longitude.set()

async def get_dinamic_buttons():
    buttons = []
    cursor.execute("SELECT title FROM sights;")
    items = cursor.fetchall()
    for i in range(len(items)):
      for item in items [1]:
        buttons.append(types.KeyboardButton(item))
    return buttons
    
@dp.message_handler(text='Достопримичательности')
async def show_sigths(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    dynamic_buttons = await get_dinamic_buttons()
    keyboard.add9(*dynamic_buttons)
    await message.answer("Вот наши Достопримичательности:, reply_markup=keyboard")
    await SightsState.title.set()



@dp.message_handler(state=SightsState.title)
async def get_sights_title_user(message:types.message, state:FSMContext):
    if message.text == " Назад":
        await start(message)
    cursor.execute(f" SELECT * FROM sights WHERE title = '{message.text};")
    result = cursor.fetchall()
    await message.reply(f"""{result[0][0]}
{result[0][1]}
Адрес: {result}[0][2]""")
     