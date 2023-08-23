from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_keyboards = [
    KeyboardButton('Достопримечательности'),
    KeyboardButton('Информация'),
    KeyboardButton('Отели'),
    KeyboardButton('Поесть'),
    KeyboardButton('Новости'),
    KeyboardButton('Ваканции'),
    KeyboardButton('Реклама'),
    KeyboardButton('Верификация')
]

verify_keyboards = [
    KeyboardButton('Отправить номер', request_contact=True),
    KeyboardButton('Отправить локацию', request_location=True)          

]

start_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*start_keyboards)

verify_button = ReplyKeyboardMarkup(resize_keyboard=True)