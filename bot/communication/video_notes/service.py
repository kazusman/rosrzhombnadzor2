from bot.service import ActionProcessor
from typing import Union
from telebot import types  # noqa


class VideoNoteProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку входящих видео-кружков от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)

    def process_video_note_message(self):
        self.save_message(file_id=self.action.video_note.file_id)
