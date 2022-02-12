from bot.config import bot
from telebot import types  # noqa
from bot.communication.animations.service import AnimationProcessor


@bot.message_handler(content_types=['animation'])
def animation_message(message: types.Message):

    AnimationProcessor(message).process_animation_message()
