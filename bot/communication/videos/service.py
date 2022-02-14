from bot.service import ActionProcessor
from typing import Union
from telebot import types  # noqa


class VideoProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку входящих видео от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)

    def process_video_message(self):
        self.save_message()
