from bot.config import bot
from telebot import types  # noqa
from bot.communication.videos.service import VideoProcessor


@bot.message_handler(content_types=['video'])
def video_message(message: types.Message):

    VideoProcessor(message).process_video_message()
