from bot.config import bot
from telebot import types  # noqa
from bot.communication.voices.service import VoiceProcessor


@bot.message_handler(content_types=['voice'])
def voice_message(message: types.Message):

    VoiceProcessor(message).process_voice_message()
