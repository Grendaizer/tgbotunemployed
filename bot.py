import time

import telebot
from telebot import types

bot = telebot.TeleBot('6123473108:AAHAGw_6bNuDugI9blWw5slk6o9AB4xukmk')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Открыть список!")
    markup.add(btn1)
    bot.send_message(message.chat.id,"Кого уволить за не затреканное время в TFS?",reply_markup=markup)

@bot.message_handler(content_types=['text'])
def uvolit(message):
    if message.text == "Открыть список!":
        spisok = types.InlineKeyboardMarkup()
        bn = types.InlineKeyboardButton(text='Банников',url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        fr = types.InlineKeyboardButton(text='Фролов', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        spisok.add(bn,fr)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bannikov = types.KeyboardButton("Банников")
        frolov = types.KeyboardButton("Фролов")
        two = types.KeyboardButton("Уволить обоих")
        back = types.KeyboardButton("Назад")
        markup.add(frolov,bannikov,two,back)

        bot.send_message(message.chat.id,'Вот список:',reply_markup=spisok)
        bot.send_message(message.chat.id, 'Кого уволить?', reply_markup=markup)
    elif message.text =="Фролов":
        bot.send_message(message.chat.id, 'Начинаю процесс увольнения...')
        time.sleep(2)
        bot.send_message(message.chat.id, 'Уволен!')
    elif message.text =="Банников":
        bot.send_message(message.chat.id, 'Начинаю процесс увольнения...')
        time.sleep(2)
        bot.send_message(message.chat.id, 'Уволен!')
    elif message.text =="Уволить обоих":
        bot.send_message(message.chat.id, 'Начинаю процесс увольнения...')
        time.sleep(2)
        bot.send_message(message.chat.id, 'Уволены!')
    elif message.text == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Открыть список!")
        markup.add(btn1)
        bot.send_message(message.chat.id, "Кого уволить за не затреканное время в TFS?", reply_markup=markup)
bot.polling(none_stop=True,interval=0)