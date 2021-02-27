from telegram.ext import Updater
import random
from datetime import datetime
import requests
import pyowm
import re
import os
from flask import Flask, request
import logging


def weather_answer(update, context, where):
    owm = pyowm.OWM('***')
    sf = owm.weather_at_place(where)
    weather = sf.get_weather()
    update.message.reply_text(
        'Weather in the city {}: {}°C'.format(where, str(round(float(weather.get_temperature('fahrenheit')['temp'])-32.00, 1))))


def press_f_answer(update, context):
    update.message.reply_text(
        'F')
