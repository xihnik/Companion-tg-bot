from telegram.ext import Updater
import random
from datetime import datetime
import requests
import pyowm
import re
import os
from flask import Flask, request
import logging
import apiai
import json
import re
from on_event.work.text import *
from on_event.errors import *


def press_f(update, context):
    if(update.message.text == 'F'):
        press_f_answer(update, context)


def weather(update, context):
    if (update.message.text.lower().find("weather") >= 0) and (update.message.text.lower().find("\"") >= 0):
        try:
            result = re.search(
                r'\"\w{2,}\"', str(update.message.text.lower()))
            weather_answer(update, context, str(
                result.group(0)[1:-1]).capitalize())
        except:
            init_errors(update, context, '0001')


def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def other(update, context):
    if(findWholeWord('bot tell')(update.message.text.lower())):
        request = apiai.ApiAI(
            '***id***').text_request()
        request.lang = 'en'
        request.session_id = '***'
        request.query = update.message.text[len('Bot tell, '):]
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech']
        if response:
            update.message.reply_text(response)


def init(update, context):
    press_f(update, context)
    weather(update, context)
    other(update, context)
