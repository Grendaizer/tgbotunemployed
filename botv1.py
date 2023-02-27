import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot("6222585016:AAHGD1TwO8ExLr8arlcTAOZUbUKScTpmg0Q")


def create_main_menu_keyboard():
    menu = types.InlineKeyboardMarkup()
    random = types.InlineKeyboardButton(text="Рандомайзер", callback_data="random")
    sts = types.InlineKeyboardButton(text="Статистика", callback_data="statistic")
    lwp = types.InlineKeyboardButton(text="Кандидаты на LWP", callback_data="candidates")
    delete = types.InlineKeyboardButton(text="Удалить себя", callback_data="delete")
    addd = types.InlineKeyboardButton(text="Добавить себя", callback_data="add")
    menu.add(lwp, random, sts, delete, addd)
    return menu

def create_user_buttons(user_data):
    buttons = []
    for user in user_data:
        button = types.InlineKeyboardButton(text=f"{user[0]} ({user[1]} кликов)", callback_data=f"user_{user[0]}")
        buttons.append(button)
    return buttons

def show_statistics(call):
    connect = sqlite3.connect('users1.db')
    cursor = connect.cursor()
    try:
        cursor.execute("SELECT name, clicks FROM users ORDER BY clicks DESC")
        data = cursor.fetchall()

        keyboard = types.InlineKeyboardMarkup()
        buttons = create_user_buttons(data)
        keyboard.add(*buttons)

        button_back = types.InlineKeyboardButton(text="Назад", callback_data="back")
        keyboard.add(button_back)

        bot.send_message(call.message.chat.id, "Таблица рейтингов:", reply_markup=keyboard)
    except Exception:
        bot.send_message(call.message.chat.id, "Ошибка")
    finally:
        cursor.close()
        connect.close()

@bot.callback_query_handler(func=lambda call: call.data == 'statistic')
def show_statistics_callback(call):
    show_statistics(call)


@bot.message_handler(commands=['start'])
def start(message):
    menu = create_main_menu_keyboard()
    bot.send_message(message.chat.id, 'Что будем делать ?', reply_markup=menu)


@bot.message_handler(commands=['menu'])
def text(message):
    menu = create_main_menu_keyboard()
    bot.send_message(message.chat.id, 'Что будем делать ?', reply_markup=menu)


@bot.callback_query_handler(func=lambda call: call.data.startswith('user_'))
def user_click(call):
    try:
        user_id = call.data[5:]  # extract user ID from callback data
        connect = sqlite3.connect('users1.db')
        cursor = connect.cursor()
        cursor.execute(f"UPDATE users SET clicks = clicks + 1 WHERE name = '{user_id}'")
        connect.commit()
        cursor.close()
        connect.close()

        keyboard = types.InlineKeyboardMarkup()
        action = types.InlineKeyboardButton(text="Уволен(а)!", callback_data="action")
        back = types.InlineKeyboardButton(text="Назад", callback_data="back1")
        keyboard.add(action, back)

        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=keyboard)
    except Exception:
        bot.send_message(call.message.chat.id, "Ошибка")


@bot.callback_query_handler(func=lambda call: call.data == 'action')
def user_action(call):
    bot.send_message(call.message.chat.id, "Уволен")


@bot.callback_query_handler(func=lambda call: call.data == 'candidates')
def show_lwp(call):
    connect = sqlite3.connect('users1.db')
    cursor = connect.cursor()
    try:
        cursor.execute("SELECT name, clicks FROM users")
        data = cursor.fetchall()

        keyboard = types.InlineKeyboardMarkup()
        for user in data:
            button = types.InlineKeyboardButton(text=f"{user[0]}", callback_data=f"user_{user[0]}")
            keyboard.add(button)

        button_back = types.InlineKeyboardButton(text="Назад", callback_data="back")
        keyboard.add(button_back)

        bot.send_message(call.message.chat.id, "Список непрошедних тренинги:", reply_markup=keyboard)
    except Exception:
        bot.send_message(call.message.chat.id, "Тебя нету в БД,добавь себя")
    finally:
        cursor.close()
        connect.close()


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back(query: types.CallbackQuery):
    menu = create_main_menu_keyboard()
    bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=menu)


@bot.callback_query_handler(func=lambda call: call.data == 'back1')
def back1(query: types.CallbackQuery):
    show_lwp(query)

import random
@bot.callback_query_handler(func=lambda call: call.data == 'random')
def random_user(call):
    connect = sqlite3.connect('users1.db')
    cursor = connect.cursor()
    try:
        cursor.execute("SELECT name, clicks FROM users")
        
        data = cursor.fetchall()
        if data:
            user = random.choice(data)
            user_name, user_clicks = user
            cursor.execute(f"UPDATE users SET clicks = clicks + 1 WHERE name = '{user_name}'")
            connect.commit()
            bot.send_message(call.message.chat.id, f"{user_name} отправляется в путешествие в БЕЗРАБОТИЦУ")
        else:
            bot.send_message(call.message.chat.id, "Список кандидатов на LWP пуст")
    except Exception:
        bot.send_message(call.message.chat.id, "Произошла ошибка")
    finally:
        cursor.close()
        connect.close()

@bot.callback_query_handler(func=lambda call: call.data == 'add')
def register(call):
    connect = sqlite3.connect('users1.db')
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                       id INTEGER,
                       name TEXT,
                       clicks INTEGER DEFAULT 0)''')
    connect.commit()
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    cursor.execute(f"SELECT id FROM users WHERE id = {user_id}")
    data = cursor.fetchone()
    if data is None:
        user_data = [user_id, user_name, 0]
        cursor.execute("INSERT INTO users VALUES(?,?,?);", user_data)
        connect.commit()
        bot.answer_callback_query(callback_query_id=call.id, text=f'Ты успешно добавлен(а) в базу, {user_name} !')
    else:
        bot.answer_callback_query(callback_query_id=call.id, text=f'Ты уже есть в базе данных, {user_name} !')
    cursor.close()
    connect.close()


@bot.callback_query_handler(func=lambda call: call.data == 'delete')
def delete(call):
    connect = sqlite3.connect('users1.db')
    cursor = connect.cursor()
    other_id = call.from_user.id
    try:
        cursor.execute(f"SELECT id FROM users WHERE id = {other_id}")
        data = cursor.fetchone()
        if data is None:
            bot.answer_callback_query(callback_query_id=call.id,
                                      text=f'{call.from_user.first_name}, тебя не существует =)')
        else:
            cursor.execute(f"DELETE FROM users WHERE id={other_id}")
            connect.commit()
            bot.answer_callback_query(callback_query_id=call.id,
                                      text=f'{call.from_user.first_name}, удален из базы данных !')
    except Exception:
        bot.answer_callback_query(callback_query_id=call.id, text="Ой, что-то пошло не так...")
    cursor.close()


bot.polling(none_stop=True, interval=0)
