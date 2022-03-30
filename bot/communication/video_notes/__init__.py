from telebot import types  # noqa

from bot.communication.video_notes.service import VideoNoteProcessor
from bot.config import bot


@bot.message_handler(content_types=["video_note"])
def video_note_message(message: types.Message):

    VideoNoteProcessor(message).process_video_note_message()
