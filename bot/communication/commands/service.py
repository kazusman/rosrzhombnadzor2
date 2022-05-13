from random import choice
from typing import Optional
from typing import Union

from django.db.models import ObjectDoesNotExist
from django.db.models import Q
from telebot import types  # noqa

from bot.models import *
from bot.service import ActionProcessor
from bot.service import get_readable_balance
from bot.service import text
from bot.service.demotivator import DemotivatorMaker
from google_vision.models import RecognitionType


class CommandProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку воходящих команд от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)

    def _create_bet(self):
        try:
            message = Message.objects.get(
                message_id=self.action.reply_to_message.message_id
            )
        except ObjectDoesNotExist:
            self.bot.send_message(self.chat_id, text.NO_MESSAGE_IN_DATABASE)
            return
        users = User.objects.filter(
            ~Q(telegram_id=self.telegram_id), is_deleted=False, coins__gt=0
        ).order_by("username")
        if len(users) == 0:
            self.bot.send_message(self.chat_id, text.POOR_USERS)
            return
        reply_markup = self.markup.bet_user_list(users)
        new_message = self.bot.send_message(
            self.chat_id, text.SELECT_TARGET_USER, reply_markup=reply_markup
        )
        Bet.objects.create(
            user=self.database_user, message=message, bot_message_id=new_message.id
        )

    def _create_donate(self, to_user: Optional[User] = None) -> Donate:
        return Donate.objects.create(from_user=self.database_user, to_user=to_user)

    def _get_replied_message(self) -> Optional[Message]:
        try:
            return Message.objects.get(
                message_id=self.action.reply_to_message.message_id
            )
        except ObjectDoesNotExist:
            return

    def _get_file_id(self):
        message = self._get_replied_message()
        if message is None:
            self.bot.send_message(self.chat_id, text.FILE_ID_NO_MESSAGE)
            return
        if message.file_id is None:
            self.bot.send_message(self.chat_id, text.FILE_ID_DOES_NOT_EXIST)
            return
        self.bot.send_message(
            self.chat_id, f"<code>{message.file_id}</code>", parse_mode="HTML"
        )

    def _create_demotivator_with_avatar(self):
        profile_photos = self.bot.get_user_profile_photos(self.telegram_id)
        if profile_photos.total_count == 0:
            self.bot.send_message(self.chat_id, text.CANNOT_MAKE_DEMOTIVATOR)
        else:
            file_id = profile_photos.photos[0][-1].file_id
            file_path = self.bot.get_file(file_id).file_path
            file_bytes = self.bot.download_file(file_path)
            with open(self.downloaded_file_path, "wb") as image:
                image.write(file_bytes)
        demotivator_path = DemotivatorMaker(
            self.downloaded_file_path
        ).create_demotivator()
        with open(demotivator_path, "rb") as demotivator:
            self.bot.send_photo(self.chat_id, demotivator)

    def process_start_command(self):
        message_text: str = choice(StartAnswer.objects.all()).answer
        self.bot.send_message(self.chat_id, message_text, parse_mode="HTML")

    def process_search_command(self):
        if not self.is_forwarded:
            self.update_status("search_meme")
            self.bot.send_message(self.chat_id, text.LETS_SEARCH)

    def process_bet_command(self):
        if self.action.reply_to_message is None:
            self.bot.send_message(self.chat_id, text.NEED_TO_REPLY)
        elif self.database_user.coins == 0:
            self.bot.send_video(
                self.chat_id,
                "BAACAgIAAx0CR_H_4AACklRiFW6us_ckKu7dPtN0k4Z6XyN_CQAC4hQAArxdqEi3SfbD7ZuF3yME",
            )
        else:
            self._create_bet()

    def process_random_command(self):
        random_message: Message = choice(Message.objects.filter(message_type="photo"))
        self.bot.forward_message(self.chat_id, self.chat_id, random_message.message_id)

    def process_anek_command(self):
        anek: Anekdot = choice(Anekdot.objects.all()).anek
        self.bot.send_message(self.chat_id, anek)

    def process_file_id_command(self):
        if self.action.reply_to_message is None:
            self.bot.send_message(self.chat_id, text.FILE_ID_NEED_TO_REPLY)
            return
        self._get_file_id()

    def process_stat_command(self):
        users = User.objects.filter(is_deleted=False).order_by("-coins")
        stat_text = ""
        for user in users:
            stat_text += f"{user.username}: {get_readable_balance(user.coins)}\n"
        self.bot.send_message(self.chat_id, text.DAILY_STAT.format(stat_text))

    def process_donate_command(self):
        if self.database_user.coins == 0:
            self.bot.send_message(self.chat_id, text.DONATE_ZERO_BALANCE)
            return
        if self.action.reply_to_message is not None:
            message = Message.objects.filter(
                message_id=self.action.reply_to_message.message_id
            )
            if message:
                message = message[0]
                if message.user != self.database_user:
                    donate = self._create_donate(message.user)
                    self.update_status(f"donate_amount:{donate.id}")
                    self.bot.send_message(
                        self.chat_id,
                        text.SEND_DONATE_AMOUNT.format(
                            get_readable_balance(self.database_user.coins)
                        ),
                    )
                    return
        users = User.objects.filter(
            ~Q(telegram_id=self.telegram_id), is_deleted=False
        ).order_by("username")
        donate = self._create_donate()
        self.update_status(f"donate_id:{donate.id}")
        reply_markup = self.markup.donate_user_list(users)
        self.bot.send_message(
            self.chat_id, text.SELECT_MONEY_RECEIVER, reply_markup=reply_markup
        )

    def process_switch_vision_recognition(self):
        readable_recognition_type = {"google": "Google", "local": "Tesseract"}
        recognition_types = RecognitionType.objects.all()
        current_main_type = recognition_types.get(is_main=True)
        current_non_main_type = recognition_types.get(is_main=False)
        self.bot.send_message(
            self.chat_id,
            text.RECOGNITION_TYPE_CHANGE.format(
                readable_recognition_type[current_non_main_type.type]
            ),
        )
        current_main_type.is_main = False
        current_non_main_type.is_main = True
        current_main_type.save()
        current_non_main_type.save()

    def process_demotivator_command(self):
        if self.action.reply_to_message is None:
            self._create_demotivator_with_avatar()
            return
        if self.action.reply_to_message.content_type != "photo":
            self._create_demotivator_with_avatar()
            return
        self.download_photo(self.action)
        demotivator_path = DemotivatorMaker(
            self.downloaded_file_path
        ).create_demotivator()
        with open(demotivator_path, "rb") as demotivator:
            self.bot.send_photo(self.chat_id, demotivator)
