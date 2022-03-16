import logging
import asyncio
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatType
from sqlite import SQLite
from buttons import keyboard


logging.basicConfig(level=logging.INFO)

token = ''
bot = Bot(token=token)
dp = Dispatcher(bot)
db = SQLite('database.db')

sup_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button = types.InlineKeyboardButton('Написать в поддержку', url='http://t.me/yourID')
sup_keyboard.add(button)

list_of_skipped_text = ['👨 Личный кабинет', '👥 Найти собеседника', '⛔️ Отменить', "⛔️ Завершить чат"]


@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    if db.get_user_in_base(message.from_user.id) is None:
        db.add_user_in_base(message.from_user.id, message.from_user.username)
        await message.answer("Вы зарегистрированы", reply_markup=await keyboard('start'))
    else:
        await message.answer("Главное меню", reply_markup=await keyboard('start'))

    await message.delete()


@dp.message_handler(commands=['queue'])
async def start_search(message: types.Message):

    if db.get_user_in_queue(message.from_user.id) is None:
        user_in_room_check = db.get_user_in_room(message.from_user.id)
        if user_in_room_check[0] is None and user_in_room_check[1] is None:
            db.add_user_in_queue(message.from_user.id)
            await message.answer("Вы начали поиск!", reply_markup=await keyboard('cancel'))
        else:
            await message.answer("Вы уже общаетесь!")
    else:
        await message.answer("Вы уже в поиске")

    await message.delete()


@dp.message_handler(commands=['exit'])
async def exit(message: types.Message):

    if db.get_user_in_queue(message.from_user.id) is None:
        await message.answer("Вы не в поиске!")
    else:
        user_in_room_check = db.get_user_in_room(message.from_user.id)
        if user_in_room_check[0] is None and user_in_room_check[1] is None:
            db.delete_user_from_queue(message.from_user.id)
            await message.answer("Вы удалены из поиска!", reply_markup=await keyboard('start'))
        else:
            await message.answer("Вы уже общаетесь!")

    await message.delete()


@dp.message_handler(commands=["stop_chat"])
async def stop_chatting(message: types.Message):

    room_id = db.get_user_id_room(message.from_user.id)
    if room_id is not None:
        room_mate_id = db.get_room_mate_id(room_id[0], message.from_user.id)
        db.delete_room(room_id[0])
        await bot.send_message(room_mate_id, f"Собеседник завершил чат с вами!", reply_markup=await keyboard('start'))
        await message.answer("Вы завершили чат!", reply_markup=await keyboard('start'))
    else:
        await message.answer("Вы не общаетесь с кем либо!")


@dp.message_handler(chat_type=ChatType.PRIVATE, content_types=['text', 'photo', 'sticker', 'video', 'game', 'animation', 'document', 'voice', 'dice', 'video_note'])
async def get_text(message: types.Message):  # u can remake this
    if message.text == '👨 Личный кабинет':
        pass
    elif message.text == '👥 Найти собеседника':
        await start_search(message)
    elif message.text == '⛔️ Отменить':
        await exit(message)
    elif message.text == "⛔️ Завершить чат":
        await stop_chatting(message)
    elif message.text == '💬 Поддержка':
        await bot.send_message(message.from_user.id, 'Сформулируйте свой вопрос четко, чтобы мы могли как можно скорее дать на него ответ', reply_markup=sup_keyboard)

    room_id = db.get_user_id_room(message.from_user.id)
    if room_id is not None:
        if message.text in list_of_skipped_text:
            pass
        else:
            room_mate_id = db.get_room_mate_id(room_id[0], message.from_user.id)
            if message.audio:
                await bot.send_audio(room_mate_id, message.audio.file_id, caption="Отправлено собеседником")
            elif message.document:
                await bot.send_document(room_mate_id, message.document.file_id, caption="Отправлено собеседником")
            elif message.video:
                await bot.send_video(room_mate_id, message.video.file_id, caption="Отправлено собеседником")
            elif message.video_note:
                await bot.send_video_note(room_mate_id, message.video_note.file_id, caption="Отправлено собеседником")
            elif message.photo:
                await bot.send_photo(room_mate_id, message.photo[-1].file_id, caption="Отправлено собеседником")
            elif message.text:
                await bot.send_message(room_mate_id, f"Собеседник: {message.text}")
            elif message.sticker:
                await bot.send_sticker(room_mate_id, message.sticker.file_id)


async def connect_users():
    queue = db.get_queue()
    if queue is None:
        pass
    elif len(queue) >= 2:
        users_id = [queue[0][0], queue[1][0]]
        db.delete_user_from_queue(users_id[0])
        db.delete_user_from_queue(users_id[1])
        await bot.send_message(users_id[0], "Собеседник найден!", reply_markup=await keyboard('exit'))
        await bot.send_message(users_id[1], "Собеседник найден!", reply_markup=await keyboard('exit'))
        rooms = len(db.get_count_rooms())
        room_id = 0 if rooms is None else rooms+1
        db.add_new_room(room_id, users_id[0], users_id[1])
    else:
        pass


def repeat_connect_users(coro, lp):
    asyncio.ensure_future(coro(), loop=lp)
    loop.call_later(1, repeat_connect_users, coro, lp)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(5, repeat_connect_users, connect_users, loop)
    executor.start_polling(dp, skip_updates=True)
