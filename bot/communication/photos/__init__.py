from telebot import types  # noqa

from bot.communication.photos.service import PhotoProcessor
from bot.config import bot


@bot.message_handler(content_types=["photo"])
def photo_message(message: types.Message):

    PhotoProcessor(message).process_photo_message()
