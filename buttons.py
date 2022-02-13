import asyncio
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


async def keyboard(data, message=None):

    if data == 'start':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton('📱 Личный кабинет')
        button2 = KeyboardButton('👥 Найти собеседника')
        button3 = KeyboardButton('💬 Поддержка')
        keyboard.add(button1, button2).add(button3)
    
    elif data == 'adm_start':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton('👨 Личный кабинет')
        button2 = KeyboardButton('🎲 Играть')
        button3 = KeyboardButton('💬 Техническая поддержка')
        button4 = KeyboardButton('🛠 Админ панель')
        keyboard.add(button1, button2).add(button3,button4)

    elif data == 'cub':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        button1 = KeyboardButton('🎲')
        keyboard.add(button1)

    elif data == 'cancel':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton('⛔️ Отменить')
        keyboard.add(button1)

    elif data == 'exit':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton('⛔️ Завершить чат')
        keyboard.add(button1)

    return keyboard