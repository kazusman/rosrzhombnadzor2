from telebot import types  # noqa

from bot.communication.text_messages.service import TextProcessor
from bot.config import bot


@bot.message_handler(content_types=["text"])
def text_message(message: types.Message):

    TextProcessor(message).process_text_message()
