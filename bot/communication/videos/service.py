import os
from typing import Union

import cv2
from django.conf import settings
from telebot import types  # noqa

from bot.service import ActionProcessor


class VideoProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку входящих видео от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)
        self.downloaded_video_path = os.path.join(
            settings.BASE_DIR,
            "bot",
            "communication",
            "videos",
            "downloaded_files",
            "video.mp4",
        )
        self.first_frame_saved_destination = os.path.join(
            settings.BASE_DIR,
            "bot",
            "communication",
            "photos",
            "downloaded_files",
            "image.jpg",
        )

    def _extract_first_frame(self):
        video = cv2.VideoCapture(self.downloaded_video_path)
        _, frame = video.read()
        cv2.imwrite(self.first_frame_saved_destination, frame)
        return

    def _save_video(self) -> bool:
        if self.action.video.file_size > 20000000:
            return False
        else:
            video_id = self.action.video.file_id
            file_path = self.bot.get_file(video_id).file_path
            file_bytes = self.bot.download_file(file_path)
            with open(self.downloaded_video_path, "wb") as file:
                file.write(file_bytes)
            self._extract_first_frame()
            return True

    def process_video_message(self):
        database_message = self.save_message(file_id=self.action.video.file_id)
        if self._save_video():
            recognition_type, text_on_image = self.get_text_from_image(database_message)
            self.add_text_from_image(database_message, text_on_image, recognition_type)
            text_from_audio = self.get_text_from_audio(database_message)
            self.add_text_from_audio(database_message, text_from_audio)
