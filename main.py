import os
import random
from iso3166 import countries
import telebot
from telebot import types

bot = telebot.TeleBot('7705373320:AAEA0prKtm65Gh1tz8eFu13_G6FPEIPXDas')
kb = telebot.types.ReplyKeyboardMarkup(True)
kb.row('Start Quizz!')
kbs = []
c = 0
r = 0
right_country_code = ''


def choose_pos_for_right_flag(codes, counter, flag=False):
    global kbs
    if flag:
        kbs = []
    num = random.randint(0, 3)
    kbs.append(telebot.types.ReplyKeyboardMarkup(True))
    if num == 0:
        kbs[counter].row(countries.get(right_country_code).name, codes[0])
        kbs[counter].row(codes[1], codes[2])
    elif num == 1:
        kbs[counter].row(codes[0], countries.get(right_country_code).name)
        kbs[counter].row(codes[1], codes[2])
    elif num == 2:
        kbs[counter].row(codes[0], codes[1])
        kbs[counter].row(countries.get(right_country_code).name, codes[2])
    elif num == 3:
        kbs[counter].row(codes[0], codes[1])
        kbs[counter].row(codes[2], countries.get(right_country_code).name)

    return kbs[counter]


def flags(message, count, flag=False):
    global right_country_code
    country_codes = []
    for i in range(3):
        filename = random.choice(os.listdir('flags'))
        code = countries.get(filename.split('.')[0]).name
        country_codes.append(code)
    filename = random.choice(os.listdir('flags'))
    right_country_code = filename.split('.')[0]
    path = os.path.join('flags', filename)

    rk = choose_pos_for_right_flag(country_codes, count, flag)

    flag = open(path, 'rb')
    bot.send_photo(message.chat.id, photo=flag, reply_markup=rk)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi 👋! Guess all flags and check your geography level!',
                     reply_markup=kb)


@bot.message_handler(commands=['ban'])
def answer(message):
    command_parts = message.text.split()

    if len(command_parts) > 1:
        if message.from_user.username == 'a100lex':
            banned = command_parts[1]
            with open('ban.txt', 'a') as f:
                f.write(banned + '\n')
        else:
            bot.send_message(message, "You tried to hack. You will be banned!!!")
            with open('ban.txt', 'a') as f:
                f.write(message.from_user.username + '\n')
    else:
        bot.send_message(message, "Give username to ban")


@bot.message_handler(content_types=['text'])
def quizz(message):
    global c, r
    with open('ban.txt', 'r') as f:
        info = f.read().split('\n')
    if message.from_user.username not in info:
        if message.text == 'Start Quizz!':
            c = 0
            r = 0
            flags(message, 0, True)
        if c == 9:
            if message.text == countries.get(right_country_code).name and message.text != 'Start Quizz!':
                r += 1
                bot.send_message(message.chat.id, 'Yeah!', reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(message.chat.id, '🤗', reply_markup=types.ReplyKeyboardRemove())
            elif message.text != 'Start Quizz!':
                bot.send_message(message.chat.id, f'No! It is {countries.get(right_country_code).name}!',
                                 reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(message.chat.id, '😭', reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(message.chat.id, f'Your score is {r}/10!', reply_markup=kb)
        if c != 9:
            if message.text == countries.get(right_country_code).name and message.text != 'Start Quizz!':
                c += 1
                r += 1
                bot.send_message(message.chat.id, 'Yeah!', reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(message.chat.id, '🤗', reply_markup=types.ReplyKeyboardRemove())
                flags(message, c)
            elif message.text != 'Start Quizz!':
                c += 1
                bot.send_message(message.chat.id, f'No! It is {countries.get(right_country_code).name}!',
                                 reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(message.chat.id, '😭', reply_markup=types.ReplyKeyboardRemove())
                flags(message, c)
    else:
        bot.send_message(message.chat.id, 'You were banned! Admin: @a100lex')


bot.polling(none_stop=True, interval=0)
