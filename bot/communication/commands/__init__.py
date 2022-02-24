from bot.config import bot
from telebot import types  # noqa
from bot.communication.commands.service import CommandProcessor


@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
    CommandProcessor(message).process_start_command()


@bot.message_handler(commands=['search'])
def search_command(message: types.Message):
    CommandProcessor(message).process_search_command()


@bot.message_handler(commands=['bet'])
def bet_command(message: types.Message):

    CommandProcessor(message).process_bet_command()


@bot.message_handler(commands=['random'])
def random_command(message: types.Message):

    CommandProcessor(message).process_random_command()


@bot.message_handler(commands=['anek'])
def anek_command(message: types.Message):

    CommandProcessor(message).process_anek_command()


@bot.message_handler(commands=['file_id'])
def file_id_command(message: types.Message):

    CommandProcessor(message).process_file_id_command()


@bot.message_handler(commands=['stat'])
def stat_command(message: types.Message):

    CommandProcessor(message).process_stat_command()


@bot.message_handler(commands=['donate'])
def donate_command(message: types.Message):

    CommandProcessor(message).process_donate_command()