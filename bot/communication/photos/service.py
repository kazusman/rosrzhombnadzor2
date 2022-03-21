import os
import textwrap

from bot.service import ActionProcessor, text
from bot.models import Message, DemotivatorText
from bot.service.funny_answer import TextAnalyzer
from typing import Union, Optional
from telebot import types  # noqa
from django.conf import settings
from google.api_core.exceptions import ClientError  # noqa
from random import randint, choice
from PIL import Image, ImageDraw, ImageFont


class PhotoProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку входящих изображений от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)
        self.downloaded_file_path = os.path.join(settings.BASE_DIR, 'bot', 'communication', 'photos',
                                                 'downloaded_files', 'image.jpg')
        self.demotivator_template_path = os.path.join(settings.BASE_DIR, 'bot', 'communication', 'photos',
                                                      'downloaded_files', 'demotivator_template.png')
        self.caption = self.action.caption

    photo_md5_hash: str
    font: ImageFont.FreeTypeFont

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

    def _resize_original_image(self):
        with Image.open(self.downloaded_file_path) as image:
            image = image.resize((508, 508), Image.ANTIALIAS)
            image.save(self.downloaded_file_path)

    def _add_image_to_demotivator_template(self):
        with Image.open(self.demotivator_template_path) as demotivator_template:
            with Image.open(self.downloaded_file_path) as image:
                demotivator_template.paste(image, box=(128, 53))
                demotivator_template.save(self.downloaded_file_path)

    def _get_font(self):
        self.font = ImageFont.truetype(os.path.join(settings.BASE_DIR, 'bot', 'fonts', 'times_new_roman.ttf'), 44)

    def _add_text_to_demotivator(self):
        demotivator_text = choice(DemotivatorText.objects.all()).text
        self._get_font()
        refactored_text = textwrap.wrap(demotivator_text, width=30)
        with Image.open(self.downloaded_file_path) as demotivator:
            width, height = demotivator.size
            draw = ImageDraw.Draw(demotivator)
            y_start_position, y_kerning = 585, 5
            for line in refactored_text:
                current_width, current_height = draw.textsize(line, font=self.font)
                draw.text(((width - current_width) / 2, y_start_position), line, font=self.font)
                y_start_position += current_height + y_kerning
            demotivator.save(self.downloaded_file_path)

    def _create_demotivator(self):
        self._resize_original_image()
        self._add_image_to_demotivator_template()
        self._add_text_to_demotivator()

    def process_photo_message(self):
        photo_bytes = self._download_photo()
        self.photo_md5_hash = self.get_md5_hash(photo_bytes)
        self._check_boyan_or_not()
        message = self.save_message(content_hash=self.photo_md5_hash, message_text=self.action.caption,
                                    file_id=self.action.photo[-1].file_id)
        if randint(1, 100) <= 15:
            self._create_demotivator()
            with open(self.downloaded_file_path, 'rb') as demotivator:
                self.bot.send_photo(self.chat_id, demotivator, reply_to_message_id=self.message_id)
        try:
            recognition_type, text_on_image = self.get_text_from_image(message)
        except ClientError as error:
            recognition_type = None
            text_on_image = ''
            self.bot.send_message(self.chat_id, text.GOOGLE_API_ERROR.format(
                error.__class__.__name__, error
            ))
        if text_on_image != '':
            self.add_text_from_image(message, text_on_image, recognition_type)
            TextAnalyzer(text_on_image, self.chat_id, self.message_id)
            return
        if self.caption is not None:
            TextAnalyzer(self.caption, self.chat_id, self.message_id)
