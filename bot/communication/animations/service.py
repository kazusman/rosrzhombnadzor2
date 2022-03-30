from typing import Union

from telebot import types  # noqa

from bot.service import ActionProcessor


class AnimationProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку входящих GIF от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)

    def process_animation_message(self):
        self.save_message(file_id=self.action.animation.file_id)
