from bot.config import bot
from telebot import types  # noqa
from bot.communication.text_messages.service import TextProcessor


@bot.message_handler(content_types=['text'])
def text_message(message: types.Message):

    TextProcessor(message).process_text_message()