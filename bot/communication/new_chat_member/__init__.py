from bot.config import bot
from telebot import types  # noqa


@bot.message_handler(content_types=['new_chat_members'])
def new_chat_member(message: types.Message):

    pass

    # Надо добавить функцию, чтоб при вступлении нового юзера бот добвлял его в бд
