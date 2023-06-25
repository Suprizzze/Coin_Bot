import telebot
from os import environ
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

api_url = environ['api_url']
TOKEN = environ["TOKEN"]
bot = telebot.TeleBot(TOKEN)
group_chat_id = environ["group_chat_id"]
my_user_id = environ["my_user_id"]