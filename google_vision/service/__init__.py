import io
import json
import os
from typing import Optional

import cv2
import moviepy.editor as mp
import pytesseract
from django.conf import settings
from google.cloud import speech_v1
from google.cloud import vision_v1  # noqa
from google.cloud.vision_v1 import AnnotateImageResponse
from google.cloud.vision_v1 import types
from google.protobuf.json_format import MessageToJson
from PIL import Image

from bot.models import Message
from google_vision.models import RecognitionType
from google_vision.models import Request


class VisionAPI:
    def __init__(self, message: Message):
        self.message = message
        self.credential_file = settings.GOOGLE_CREDENTIALS_FILE_PATH
        self.client = vision_v1.ImageAnnotatorClient()
        self.downloaded_file_path = os.path.join(
            settings.BASE_DIR,
            "bot",
            "communication",
            "photos",
            "downloaded_files",
            "image.jpg",
        )
        self.gray_image_path = os.path.join(
            settings.BASE_DIR,
            "bot",
            "communication",
            "photos",
            "downloaded_files",
            "gray.jpg",
        )

    def _save_request(self, response: json):
        Request.objects.create(response=response, message=self.message)

    @staticmethod
    def _refactor_text(
        texts: list, has_description_attribute: Optional[bool] = True
    ) -> str:

        if has_description_attribute:
            text = texts[0].description.replace("\n", " ")
        else:
            text = texts[0].replace("\n", " ")
        while True:
            if text.count("  ") > 0:
                text = text.replace("  ", " ")
            else:
                break
        return text

    @staticmethod
    def _get_recognition_type() -> str:
        return RecognitionType.objects.get(is_main=True).type

    def _tesseract_recognition(self) -> str:
        text = pytesseract.image_to_string(
            Image.open(self.downloaded_file_path), lang="eng+rus"
        )
        return self._refactor_text([text], False)

    def get_text_from_photo(self) -> tuple:
        if self._get_recognition_type() == "google":
            with io.open(self.downloaded_file_path, "rb") as image_file:
                content = image_file.read()
            image = types.Image(content=content)  # noqa
            response = self.client.text_detection(
                image=image, image_context={"language_hints": ["en", "ru"]}
            )
            json_response = AnnotateImageResponse.to_json(response)
            self._save_request(json.loads(json_response))
            texts = response.text_annotations
            return "google", self._refactor_text(texts)
        else:
            return "local", self._tesseract_recognition()


class SpeechToTextAPI:
    def __init__(self, message: Message):
        self.message = message
        self.credential_file = settings.GOOGLE_CREDENTIALS_FILE_PATH
        self.speech_client = speech_v1.SpeechClient()
        self.downloaded_video_path = os.path.join(
            settings.BASE_DIR,
            "bot",
            "communication",
            "videos",
            "downloaded_files",
            "video.mp4",
        )
        self.audio_from_video_path = os.path.join(
            settings.BASE_DIR,
            "bot",
            "communication",
            "videos",
            "downloaded_files",
            "audio.mp3",
        )

    def _extract_audio_from_video(self):
        video = mp.VideoFileClip(self.downloaded_video_path)
        video.audio.write_audiofile(self.audio_from_video_path)

    def convert_speech_to_text(self) -> str:
        self._extract_audio_from_video()
        with open(self.audio_from_video_path, "rb") as audio:
            audio_bytes = audio.read()
        audio_mp3 = speech_v1.RecognitionAudio(content=audio_bytes)
        main_language_code = "ru-RU"
        additional_language_codes = ["en-US"]
        text_from_audio = ""
        config = speech_v1.RecognitionConfig(
            sample_rate_hertz=48000,
            enable_automatic_punctuation=False,
            language_code=main_language_code,
            alternative_language_codes=additional_language_codes,
        )
        response = self.speech_client.recognize(config=config, audio=audio_mp3)
        for result in response.results:
            alternative = result.alternatives[0]
            text = alternative.transcript
            text_from_audio += f"{text}"
        return text_from_audio
