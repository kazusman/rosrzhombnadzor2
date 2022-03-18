import os
import io
import json
import pytesseract
import cv2

from google.cloud import vision_v1  # noqa
from google.cloud.vision_v1 import types, AnnotateImageResponse  # noqa
from google_vision.models import Request, RecognitionType
from django.conf import settings
from bot.models import Message
from PIL import Image
from typing import Optional


class VisionAPI:

    def __init__(self, message: Message):
        self.message = message
        self.credential_file = settings.GOOGLE_CREDENTIALS_FILE_PATH
        self.client = vision_v1.ImageAnnotatorClient()
        self.downloaded_file_path = os.path.join(settings.BASE_DIR, 'bot', 'communication', 'photos',
                                                 'downloaded_files', 'image.jpg')
        self.gray_image_path = os.path.join(settings.BASE_DIR, 'bot', 'communication', 'photos',
                                                 'downloaded_files', 'gray.jpg')

    def _save_request(self, response: json):
        Request.objects.create(
            response=response,
            message=self.message
        )

    @staticmethod
    def _refactor_text(texts: list, has_description_attribute: Optional[bool] = True) -> str:

        if has_description_attribute:
            text = texts[0].description.replace('\n', ' ')
        else:
            text = texts[0].replace('\n', ' ')
        while True:
            if text.count('  ') > 0:
                text = text.replace('  ', ' ')
            else:
                break
        return text

    @staticmethod
    def _get_recognition_type() -> str:
        return RecognitionType.objects.get(is_main=True).type

    def _tesseract_recognition(self) -> str:
        text = pytesseract.image_to_string(Image.open(self.downloaded_file_path), lang='eng+rus')
        return self._refactor_text([text], False)

    def get_text_from_photo(self) -> tuple:
        if self._get_recognition_type() == 'google':
            with io.open(self.downloaded_file_path, 'rb') as image_file:
                content = image_file.read()
            image = types.Image(content=content)  # noqa
            response = self.client.text_detection(image=image, image_context={"language_hints": ["en", "ru"]})
            json_response = AnnotateImageResponse.to_json(response)
            self._save_request(json.loads(json_response))
            texts = response.text_annotations
            return 'google', self._refactor_text(texts)
        else:
            return 'local', self._tesseract_recognition()
