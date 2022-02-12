from bot.config import bot
from telebot import types  # noqa
from bot.communication.photos.service import PhotoProcessor


@bot.message_handler(content_types=['photo'])
def photo_message(message: types.Message):

    PhotoProcessor(message).process_photo_message()
