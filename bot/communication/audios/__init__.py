from telebot import types  # noqa

from bot.communication.audios.service import AudioProcessor
from bot.config import bot


@bot.message_handler(content_types=["audio"])
def audio_message(message: types.Message):

    AudioProcessor(message).process_audio_message()
