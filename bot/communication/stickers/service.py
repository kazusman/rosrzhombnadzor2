from bot.service import ActionProcessor
from typing import Union
from telebot import types  # noqa


class StickerProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку входящих стикеров от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)

    def process_sticker_message(self):
        self.save_message(file_id=self.action.sticker.file_id)
