from bot.service import ActionProcessor
from typing import Union
from telebot import types  # noqa


class AudioProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку входящих аудиофайлов (не войсов) от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)

    def process_audio_message(self):
        self.save_message(file_id=self.action.audio.file_id)
