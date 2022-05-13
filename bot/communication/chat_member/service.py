from typing import Union

from telebot import types  # noqa

from bot.models import *
from bot.service import ActionProcessor
from bot.service import text


class ChatMemberProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку сообщение о вступлении новых пользователей
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)

    @staticmethod
    def _get_database_user(new_member_telegram_id: int) -> tuple[User, bool]:
        return User.objects.get_or_create(telegram_id=new_member_telegram_id)

    def process_new_chat_member(self):
        for new_member in self.action.new_chat_members:
            database_user, is_new = self._get_database_user(new_member.id)
            if is_new:
                self.bot.send_message(self.chat_id, text.HELLO_NEW_USER)
            else:
                self.bot.send_message(self.chat_id, text.WHY_YOU_LEAVE)
                self.switch_deleted_status(False, database_user)
            self.update_status("rzhomber", self.database_user)

    def process_left_chat_member(self):
        database_user, _ = self._get_database_user(self.action.left_chat_member.id)
        self.switch_deleted_status(True, database_user)
        self.bot.send_message(self.chat_id, text.BYE)
