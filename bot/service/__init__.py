import hashlib
import os

from telebot import types  # noqa
from bot.models import User, Status, Message
from typing import Union, Optional
from bot.config import bot
from bot.service.markup import Markup
from bot.service.decorators import check_chat
from datetime import datetime
from google_vision.service import VisionAPI
from django.conf import settings


def user_status(telegram_id: int) -> Optional[str]:

    """
    Получаем последнюю запись из таблицы Status по telegram_id
    """

    user = User.objects.get(telegram_id=telegram_id)
    statuses = Status.objects.filter(user=user)
    if len(statuses) != 0:
        status: str = statuses.order_by('-id')[0].status
        if ':' in status:
            return status.split(':')[0]
        return status
    return


def get_readable_balance(balance: float) -> str:
    return '{:,}'.format(balance).replace(',', ' ')


def get_years_decade(user: User) -> str:
    years = datetime.now().year - user.date_of_birth.year
    return f'{str(years)[0]}0'


def get_readable_date(date: datetime) -> str:
    month_names = {
        1: 'января',
        2: 'февраля',
        3: 'марта',
        4: 'апреля',
        5: 'мая',
        6: 'июня',
        7: 'июля',
        8: 'августа',
        9: 'сентября',
        10: 'октября',
        11: 'ноября',
        12: 'декабря'
    }
    return f'{date.day} {month_names[date.month]} {date.year} г.'


class BotAction:

    """
    Сервисная модель действия, которое присылает telegram. Действие == сообщение или callback
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        self.action = action
        self.bot = bot
        self.action_type = type(action)
        self.message_id = self.action.id if self.action_type == types.Message else self.action.message.id
        self.message_text = self.action.text if self.action_type == types.Message else self.action.message.text
        self.call_id = self.action.id if self.action_type == types.CallbackQuery else None
        self.call_data = self.action.data if self.action_type == types.CallbackQuery else None
        self.reply_markup = self.action.reply_markup if self.action_type == types.Message else \
            self.action.message.reply_markup
        self.is_forwarded = self._is_message_forwarder()
        self.message_type = action.content_type if type(action) == types.Message else None

    def _is_message_forwarder(self) -> bool:
        if type(self.action) != types.CallbackQuery:
            return True if self.action.forward_from is not None or self.action.forward_from_chat is not None else False
        return False


class BotChat(BotAction):

    """
    Сервисная модель чата telegram-бота
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)
        self.chat_id = self.action.chat.id if self.action_type == types.Message else self.action.message.chat.id
        self.chat_type = self.action.chat.type if self.action_type == types.Message else self.action.message.chat.type


class BotUser(BotChat):

    """
    Сервисная модель пользователя telegram-бота
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)
        self.telegram_id = action.from_user.id
        self.username = action.from_user.username
        self.first_name = action.from_user.first_name
        self.last_name = action.from_user.last_name
        self.telegram_language_code = action.from_user.language_code
        self._init_user_in_database()

    database_user: User
    is_new: bool
    status: Optional[str] = None

    def _update_user_info(self):

        """
        Обновляем информацию по пользователю: его никнейм, имя, фамилию и установленный в телеграме язык
        """

        User.objects.filter(telegram_id=self.telegram_id).update(
            username=self.username, first_name=self.first_name, last_name=self.last_name
        )

    @check_chat
    def _init_user_in_database(self):

        """
        Получем запись о пользователе из базы данных либо через SELECT, если существуем, либо через CREATE, если нет
        """

        self.database_user, self.is_user_new = User.objects.get_or_create(
            telegram_id=self.telegram_id
        )
        self._update_user_info()

    def _get_last_status(self):

        """
        Получаем последний статус из модели Status
        """

        statuses = Status.objects.filter(user=self.database_user).order_by('-id')
        if len(statuses) != 0:
            self.status = statuses[0].status

    def update_status(self, status: str):

        """
        Добавляем новую запись в модель Status
        """

        Status.objects.create(
            user=self.database_user,
            status=status
        )

    def switch_deleted_status(self, deleted_status: bool, user: Optional[User] = None):
        if user is None:
            self.database_user.is_deleted = deleted_status
            self.database_user.save()
        else:
            user.is_deleted = deleted_status
            user.save()


class ActionProcessor(BotUser):

    """
    Родительская модель процессора событий, от которой наследуются процессоры под каждый конкретный тип события от бота
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)
        self.markup = Markup(self.database_user)
        self._get_last_status()

    downloaded_file_path = os.path.join(settings.BASE_DIR, 'bot', 'communication', 'photos',
                                        'downloaded_files', 'image.jpg')

    @staticmethod
    def get_md5_hash(file_bytes: bytes) -> str:
        """
        Получаем MD5 hash изображения
        """

        md5_hash = hashlib.md5()
        md5_hash.update(file_bytes)
        digest = md5_hash.hexdigest()
        return digest

    @staticmethod
    def get_text_from_image(message: Message) -> tuple:
        vision_api = VisionAPI(message)
        return vision_api.get_text_from_photo()

    @staticmethod
    def add_text_from_image(message: Message, text_on_image: str, recognition_type: str):
        message.text_on_image, message.recognition_type = text_on_image, recognition_type
        message.save()

    def save_message(self, content_hash: Optional[str] = None, message_text: Optional[str] = None,
                     text_on_image: Optional[str] = None, file_id: Optional[str] = None) -> Message:
        return Message.objects.create(
            user=self.database_user,
            message_type=self.message_type,
            is_forwarded=self.is_forwarded,
            message_text=message_text,
            content_hash=content_hash,
            message_id=self.message_id,
            text_on_image=text_on_image,
            file_id=file_id
        )

    def _save_photo(self, file_bytes: bytes):
        with open(self.downloaded_file_path, 'wb') as file:
            file.write(file_bytes)

    def download_photo(self, message: Optional[types.Message] = None) -> bytes:
        if message is None:
            photo_id = self.action.photo[-1].file_id
        else:
            photo_id = message.reply_to_message.photo[-1].file_id
        file_path = self.bot.get_file(photo_id).file_path
        file_bytes = self.bot.download_file(file_path)
        self._save_photo(file_bytes)
        return file_bytes
