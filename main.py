import os
from os import system
import random
import datetime
import requests
import pyowm
import telegram
from telegram.bot import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.message import Message
from on_event.get_text import *
import time
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS


def cm_start(update, context):
    update.message.reply_text(
        'Hello {}, you wrote to me /start'.format(update.message.from_user.first_name))


def cm_hello(update, context):
    update.message.reply_text(
        'And you {}'.format(update.message.from_user.first_name))


def cm_random(update, context):
    update.message.reply_text(
        'Random number = {}'.format(random.randint(0, 10)))


def cm_date_time(update, context):
    now_date = str(datetime.now().strftime("%d.%m.%y"))
    hours = int(str(datetime.now().strftime("%H")))
    hours += 3
    now_time = str(datetime.now().strftime(":%M:%S.%f"))
    update.message.reply_text(
        'Today is date {} and time {}{}'.format(now_date, str(hours), now_time))


def cm_coin(update, context):
    bd_coin = ["Eagle", "Tails"]
    update.message.reply_text(
        '{}'.format(bd_coin[random.randint(0, (len(bd_coin)-1))]))


def cm_dog(update, context):
    update.message.reply_text(get_dog())


def get_dog():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def cm_cat(update, context):
    update.message.reply_text(get_cat())


def get_cat():
    contents = requests.get('http://thecatapi.com/api/images/get').url
    return contents


def music_menu_title():
    return 'Menu:'


def music_menu_keyboard():
    keyboard = [[InlineKeyboardButton(
        'Show all music', callback_data='music_all')], [InlineKeyboardButton(
            'Random music', callback_data='music_random')]]
    return InlineKeyboardMarkup(keyboard)


def list_music_menu_keyboard():
    keyboard = [[InlineKeyboardButton(
        'Vitamin', callback_data='get_vitaminka')], [InlineKeyboardButton(
            'Larin 30 years old', callback_data='get_larin_30_years')]]
    return InlineKeyboardMarkup(keyboard)


def cm_music_menu(update, context):
    context.bot.send_chat_action(chat_id=update.effective_user.id,
                                 action=telegram.ChatAction.TYPING)

    menu_main = [[InlineKeyboardButton('The whole list', callback_data='m1')],
                 [InlineKeyboardButton('Random', callback_data='m2')]]

    reply_keyboard = InlineKeyboardMarkup(menu_main)
    update.message.reply_text('Choose an action', reply_markup=reply_keyboard)


def menu_actions(update: Update, context: CallbackContext):
    query = update.callback_query

    if query.data == 'm1':
        menu_1 = [[InlineKeyboardButton('Larin30', callback_data='m1_1')],
                  [InlineKeyboardButton('Vitamin', callback_data='m1_2')]]
        reply_markup = InlineKeyboardMarkup(menu_1)

        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text='Выбирайте музыку:',
                                      reply_markup=reply_markup)

    elif query.data == 'm2':
        context.bot.delete_message(chat_id=query.message.chat_id,
                                   message_id=query.message.message_id)
        cm_music_random(update, context)

    elif query.data == 'm1_1':
        context.bot.delete_message(chat_id=query.message.chat_id,
                                   message_id=query.message.message_id)
        context.bot.send_audio(update.effective_chat.id,
                               open(str(os.path.abspath('songs/Larin30.mp3')), 'rb'))

    elif query.data == 'm1_2':
        context.bot.delete_message(chat_id=query.message.chat_id,
                                   message_id=query.message.message_id)
        context.bot.send_audio(update.effective_chat.id,
                               open(str(os.path.abspath('songs/Vitamin.mp3')), 'rb'))


def cm_music_random(update, context):
    music = ['songs/Larin30.mp3',
             'songs/Vitamin.mp3']
    context.bot.send_audio(update.effective_chat.id,
                           open(str(os.path.abspath(music[random.randint(0, (len(music)-1))])), 'rb'))


def cm_weather(update, context):
    owm = pyowm.OWM('***id***')
    sf = owm.weather_at_place('Минск')
    weather = sf.get_weather()
    context.bot.send_message(
        update.effective_chat.id, 'Weather in Minsk: {}°C'.format(str(weather.get_temperature('celsius')['temp'])))


def cm_version(update, context):
    update.message.reply_text('Alpha 0.0.1')


def cm_speak(update, context):
    tts = gTTS(text=update.message.text[7:], lang='ru')
    tts.save("speak.mp3")
    context.bot.send_audio(update.effective_chat.id,
                           open(str(os.path.abspath('speak.mp3')), 'rb'))


def cm_text(update, context):
    init(update, context)


def speech_to_text(update: Update, context: CallbackContext):
    try:
        bot = context.bot
        file = bot.getFile(update.message.voice.file_id)
        file.download('voice.ogg')
        m4a_audio = AudioSegment.from_file("voice.ogg", format="ogg")
        m4a_audio.export("voice.wav", format="wav")
        filename = "voice.wav"
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="ru")
            update.message.reply_text(text)
    except:
        update.message.reply_text('Error! Speak more clearly')


def cm_voice(update, context):
    speech_to_text(update, context)


def AppClose():
    time.sleep(3)
    hours = int(str(datetime.now().strftime("%H")))
    hours += 3
    if (hours >= 2 and hours <= 8):
        raise SystemExit(1)


AppClose()

TOKEN = "***token_bot***"

updater = Updater(TOKEN, use_context=True)

dp = updater
dp.dispatcher.add_handler(CommandHandler('start', cm_start))
dp.dispatcher.add_handler(CommandHandler('hello', cm_hello))
dp.dispatcher.add_handler(CallbackQueryHandler(menu_actions))
dp.dispatcher.add_handler(CommandHandler('random', cm_random))
dp.dispatcher.add_handler(CommandHandler('datetime', cm_date_time))
dp.dispatcher.add_handler(CommandHandler('coin', cm_coin))
dp.dispatcher.add_handler(CommandHandler('dog', cm_dog))
dp.dispatcher.add_handler(CommandHandler('cat', cm_cat))
dp.dispatcher.add_handler(CommandHandler('music', cm_music_menu))
dp.dispatcher.add_handler(CommandHandler('weather', cm_weather))
dp.dispatcher.add_handler(CommandHandler('version', cm_version))
dp.dispatcher.add_handler(CommandHandler('speak', cm_speak))
dp.dispatcher.add_handler(MessageHandler(Filters.text, cm_text))
dp.dispatcher.add_handler(MessageHandler(Filters.voice, cm_voice))
dp.start_polling()
updater.idle()
