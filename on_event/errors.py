from telegram.ext import Updater
import random
from datetime import datetime
import requests
import pyowm
import re
import os
from flask import Flask, request
import logging


def weather_error(update, context, number):
    if number == '0001':
        update.message.reply_text(
            'Error №{}. Help: most likely the sentence was typed incorrectly.'.format(number))


def init_errors(update, context, number):
    weather_error(update, context, number)
