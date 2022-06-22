import time
import io

from django.conf import settings
from telebot.apihelper import ApiTelegramException
from telebot import types

from bot.config import bot
from bot.config import minio


class Parser:
    def __init__(self, start_message_id: int, last_message_id: int):
        self.last_message_id = last_message_id
        self.start_message_id = start_message_id

    @staticmethod
    def _download_file(message: types.Message, original_message_id, file_type: str):
        if file_type == "video" and message.video.file_size > 20000000:
            return
        if file_type == "photo":
            file_id = message.photo[-1].file_id
        elif file_type == "video":
            file_id = message.video.file_id
        else:
            file_id = message.animation.file_id
        extension = {
            "photo": "png",
            "video": "mp4",
            "animation": "mp4"
        }
        file_path = bot.get_file(file_id).file_path
        file_bytes = bot.download_file(file_path)
        file_as_stream = io.BytesIO(file_bytes)
        bucket_name = str(settings.CHAT_ID)[4:]
        found = minio.bucket_exists(bucket_name)
        if not found:
            minio.make_bucket(bucket_name)
        minio.put_object(
            bucket_name,
            f"{file_type}/{original_message_id}.{extension[file_type]}",
            data=file_as_stream,
            length=len(file_bytes),
        )

    def parse(self):
        for message_id in range(self.start_message_id, self.last_message_id + 1):
            try:
                message = bot.forward_message(
                    settings.PARSER_CHAT_ID, settings.CHAT_ID, message_id
                )
                if message.content_type in ("photo", "video", "animation"):
                    self._download_file(message, message_id, message.content_type)
                    print(f"Скачан файл {message.content_type} с ID {message_id}")
                time.sleep(0.25)
            except ApiTelegramException as error:
                if str(error).endswith("the message can't be forwarded"):
                    continue
                elif "Too Many Requests" in str(error):
                    error_text = str(error).replace("\n", "")
                    seconds_to_wait = int(error_text.split()[-1])
                    print(f"Слишком много запросов, ждём {seconds_to_wait} секунд")
                    time.sleep(seconds_to_wait)
                elif str(error).endswith("message to forward not found"):
                    print(f"Сообщение с ID {message_id} было удалено")
                else:
                    print(error)
            finally:
                time.sleep(0.25)
