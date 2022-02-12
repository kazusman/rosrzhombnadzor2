from bot.config import bot
from telebot import types  # noqa
from bot.communication.stickers.service import StickerProcessor


@bot.message_handler(content_types=['sticker'])
def sticker_message(message: types.Message):

    StickerProcessor(message).process_sticker_message()
