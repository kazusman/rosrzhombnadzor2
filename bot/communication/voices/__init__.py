from telebot import types  # noqa

from bot.communication.voices.service import VoiceProcessor
from bot.config import bot


@bot.message_handler(content_types=["voice"])
def voice_message(message: types.Message):

    VoiceProcessor(message).process_voice_message()
