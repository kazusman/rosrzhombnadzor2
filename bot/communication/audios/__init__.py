from bot.config import bot
from telebot import types  # noqa
from bot.communication.audios.service import AudioProcessor


@bot.message_handler(content_types=['audio'])
def audio_message(message: types.Message):

    AudioProcessor(message).process_audio_message()
