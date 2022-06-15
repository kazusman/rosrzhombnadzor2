import os
from random import randint
from typing import Optional
from typing import Union

from django.conf import settings
from google.api_core.exceptions import ClientError  # noqa
from telebot import types  # noqa

from bot.models import Message
from bot.models import User
from bot.service import ActionProcessor
from bot.service import text
from bot.service.demotivator import DemotivatorMaker
from bot.service.funny_answer import TextAnalyzer


class PhotoProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку входящих изображений от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)
        self.caption = self.action.caption

    photo_md5_hash: str

    @staticmethod
    def _is_boyan(md5_hash: str) -> tuple[bool, Optional[Message]]:

        """
        Проверяем, не баян ли
        """

        messages = Message.objects.filter(content_hash=md5_hash)
        if len(messages) != 0:
            return True, messages.order_by("-id")[0]
        return False, None

    def _check_boyan_or_not(self):
        is_boyan, message = self._is_boyan(self.photo_md5_hash)
        if is_boyan:
            self.bot.send_sticker(
                self.chat_id,
                "CAACAgIAAxkBAAEC9ulhUFSQn9kzOsyj2BHlARmo2JIO1QAC2g0AAjBJoEgRIA2_DLK51iEE",
                reply_to_message_id=message.message_id,
            )

    def process_photo_message(self):
        photo_bytes = self.download_photo()
        self.photo_md5_hash = self.get_md5_hash(photo_bytes)
        self._check_boyan_or_not()
        message = self.save_message(
            content_hash=self.photo_md5_hash,
            message_text=self.action.caption,
            file_id=self.action.photo[-1].file_id,
        )
        try:
            recognition_type, text_on_image = self.get_text_from_image(message)
        except ClientError as error:
            recognition_type = None
            text_on_image = ""
            self.bot.send_message(
                self.chat_id,
                text.GOOGLE_API_ERROR.format(error.__class__.__name__, error),
            )
        if text_on_image != "":
            self.add_text_from_image(message, text_on_image, recognition_type)
            TextAnalyzer(
                text_on_image, self.chat_id, self.message_id, self.database_user
            ).analyze()
            return
        if self.caption is not None:
            TextAnalyzer(
                self.caption, self.chat_id, self.message_id, self.database_user
            ).analyze()
        if randint(1, 100) <= 5:
            demotivator_path = DemotivatorMaker(
                self.downloaded_file_path
            ).create_demotivator()
            with open(demotivator_path, "rb") as demotivator:
                self.bot.send_photo(
                    self.chat_id, demotivator, reply_to_message_id=self.message_id
                )
