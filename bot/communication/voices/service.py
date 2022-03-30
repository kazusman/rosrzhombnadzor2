from typing import Union

from telebot import types  # noqa

from bot.service import ActionProcessor


class VoiceProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку входящих войсов от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)

    def process_voice_message(self):
        self.save_message(file_id=self.action.voice.file_id)
