import os

from bot.service import ActionProcessor, text
from bot.models import Message
from bot.service.funny_answer import TextAnalyzer
from typing import Union, Optional
from telebot import types  # noqa
from django.conf import settings
from google.api_core.exceptions import ClientError  # noqa


class PhotoProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку входящих изображений от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)
        self.downloaded_file_path = os.path.join(settings.BASE_DIR, 'bot', 'communication', 'photos',
                                                 'downloaded_files', 'image.jpg')
        self.caption = self.action.caption

    photo_md5_hash: str

    def _save_photo(self, file_bytes: bytes):
        with open(self.downloaded_file_path, 'wb') as file:
            file.write(file_bytes)

    def _download_photo(self) -> bytes:
        photo_id = self.action.photo[-1].file_id
        file_path = self.bot.get_file(photo_id).file_path
        file_bytes = self.bot.download_file(file_path)
        self._save_photo(file_bytes)
        return file_bytes

    @staticmethod
    def _is_boyan(md5_hash: str) -> tuple[bool, Optional[Message]]:

        """
        Проверяем, не баян ли
        """

        messages = Message.objects.filter(content_hash=md5_hash)
        if len(messages) != 0:
            return True, messages.order_by('-id')[0]
        return False, None

    def _check_boyan_or_not(self):
        is_boyan, message = self._is_boyan(self.photo_md5_hash)
        if is_boyan:
            self.bot.send_sticker(self.chat_id,
                                  'CAACAgIAAxkBAAEC9ulhUFSQn9kzOsyj2BHlARmo2JIO1QAC2g0AAjBJoEgRIA2_DLK51iEE',
                                  reply_to_message_id=message.message_id)

    def process_photo_message(self):
        photo_bytes = self._download_photo()
        self.photo_md5_hash = self.get_md5_hash(photo_bytes)
        self._check_boyan_or_not()
        message = self.save_message(content_hash=self.photo_md5_hash, message_text=self.action.caption,
                                    file_id=self.action.photo[-1].file_id)
        try:
            text_on_image = self.get_text_from_image(message)
        except ClientError as error:
            text_on_image = ''
            self.bot.send_message(self.chat_id, text.GOOGLE_API_ERROR.format(
                error.__class__.__name__, error
            ))
        if text_on_image != '':
            self.add_text_from_image(message, text_on_image)
            TextAnalyzer(text_on_image, self.chat_id, self.message_id)
            return
        if self.caption is not None:
            TextAnalyzer(self.caption, self.chat_id, self.message_id)
