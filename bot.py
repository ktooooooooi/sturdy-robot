# -*- coding: utf-8 -*-
# Данный скрипт написан @DarkUserWitch и VVcoder осенью 2021-ого года. при использовании скрипта просьба пересмотреть весь код и в надобности исправить ошибки. данный код был опубликован лишь потому что авторы так захотели :)

import asyncio
import random

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from models import db_session
from models.users import User

db_session.global_init('database.db')

bot_token = '5122922697:AAGAcfndeQYvzgdMWtco8XK6s7o4_v-Ly2o'

# bot = telebot.TeleBot(bot_token)
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# считаем для статистики
spins = 127
usersid = '1406556353'
chatsid = ''
users = 14


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    global users
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    await bot.send_message(message.chat.id, '🤘Привет! Я бот для игры в спины \n'
                                            '🎁Тебе предоставлен бонус - 5000 монет. \n'
                                            '🎲Теперь ты готов играть. \n'
                                            '🆘Основные команды: \n'
                                            '💰Б - Узнать свой баланс в игре. \n'
                                            '🎲Спин 1000 - Поставить ставку. \n'
                                            '💸+1000 в ответ на сообщение - передать деньги. ')


@dp.message_handler(content_types=["contact"])
async def number(message: types.Message):
    global users
    print(message.contact.phone_number)
    #
    iduser = message.from_user.id
    session = db_session.create_session()
    #
    user_all = session.query(User).all()
    T = True
    for all in user_all:
        if all.id == iduser:
            T = False

    if T:
        if message.from_user.username:
            session = db_session.create_session()
            name = message.from_user.first_name
            url = message.from_user.username
            iduser = message.from_user.id
            user = User(
                id=iduser,
                name=name,
                username='@' + url,
                money=5000,
            )
            users += 1
            session.add(user)
            session.commit()
        else:
            session = db_session.create_session()
            name = message.from_user.first_name
            url = message.from_user.username
            iduser = message.from_user.id
            user = User(
                id=iduser,
                name=name,
                username='@...',
                money=5000,
            )
            users += 1
            session.add(user)
            session.commit()


@dp.message_handler(content_types=["text"])
async def check(message: types.Message):
    global price_win
    try:
        if message.text == 'RDNO':
            await bot.send_message(message.chat.id, 'Это мой дедушка')
        elif message.text == 'Спин':
            money = 0
            session = db_session.create_session()
            user_all = session.query(User).all()
            for user in user_all:
                if user.id == message.from_user.id:
                    money = user.money

            if money != 0:
                el = [
                    '🖕', '🌚', '🌝', '🎰', '🎊', '🎁', '🦠', '🀄️', '🥃', '💎'
                ]
                random.shuffle(el)
                price = ''  
                pl = 0
                tr = 0
                if el[0] == '🖕':
                    price = '0💎'
                    pl = 0
                elif el[0] == '🌚':
                    price = '5💎'
                    pl = 5
                elif el[0] == '🌝':
                    price = '10💎'
                    pl = 10
                elif el[0] == '🎊':
                    price = '15💎'
                    pl = 15
                elif el[0] == '🎰':
                    price = '20💎'
                    pl = 20
                elif el[0] == '🎁':
                    price = '50💎'
                    pl = 50
                elif el[0] == '🦠':
                    price = '100💎'
                    pl = 100
                elif el[0] == '🀄️':
                    price = '200💎'
                    pl = 200
                elif el[0] == '💎':
                    price = '300💎'
                    pl = 300
                elif el[0] == '🥃':
                    price = '500💎'
                    pl = 500
                    
                session = db_session.create_session()
                user_all = session.query(User).all()
                name = message.from_user.first_name
                for user in user_all:
                    if user.id == message.from_user.id:
                        price_win = price[0] + price[1] + price[2]
                        user.money = user.money + pl
                session.commit()

                await bot.send_message(message.chat.id, 'Игра уже началась в этом чате!', reply_markup=types.ReplyKeyboardRemove())
                msg = await bot.send_message(message.chat.id,
                                             '' + name + '\n'
                                                         '|🌫]|🌫|🌫|')
                await asyncio.sleep(2)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                            text='' + name + '\n'
                                                             '|' + el[0] + '|🌫|🌫|')
                await asyncio.sleep(2)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                            text='' + name + '\n'
                                                             '|' + el[0] + '|' + el[1] + '|🌫|')
                await asyncio.sleep(2)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                            text='' + name + '\n'
                                                             '|' + el[0] + '|' + el[1] + '|' + el[2] + '|')
                await asyncio.sleep(3)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                            text='' + name + '\n'
                                                             '|' + el[0] + '|' + el[1] + '|' + el[2] + '|' " Ваш выигрыш: " + price_win)

        elif message.text == 'Б':
            session = db_session.create_session()
            user_all = session.query(User).all()
            money = 5000
            for user in user_all:
                if user.id == message.from_user.id:
                    money = user.money

            await bot.send_message(message.chat.id, '📑Счёт: \n' + str(money) + '💎\n' '🆔: ' + str(
                message.from_user.id))

    except BaseException as e:
        print(e)
        await bot.send_message(message.chat.id, '<b>Вы зарегались? /start в лс боту</b>', parse_mode='html')

    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()


#
if __name__ == "__main__":
    executor.start_polling(dp)
