from bot.service import ActionProcessor
from bot.models import *
from bot.service import text
from typing import Union
from telebot import types  # noqa
from random import choice
from django.db.models import ObjectDoesNotExist, Q


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
        users = User.objects.filter(~Q(telegram_id=self.telegram_id), is_deleted=False, coins__gte=0)
        if len(users) == 0:
            self.bot.send_message(self.chat_id, text.POOR_USERS)
            return
        reply_markup = self.markup.user_list(users)
        new_message = self.bot.send_message(self.chat_id, text.SELECT_TARGET_USER, reply_markup=reply_markup)
        Bet.objects.create(
            user=self.database_user,
            message=message,
            bot_message_id=new_message.id
        )

    def process_start_command(self):
        message_text: str = choice(StartAnswer.objects.all()).answer
        self.bot.send_message(self.chat_id, message_text)

    def process_search_command(self):
        self.update_status('search_meme')
        self.bot.send_message(self.chat_id, text.LETS_SEARCH)

    def process_bet_command(self):
        if self.action.reply_to_message is None:
            self.bot.send_message(self.chat_id, text.NEED_TO_REPLY)
        elif self.database_user.coins == 0:
            self.bot.send_message(self.chat_id, text.ZERO_BALANCE)
        else:
            self._create_bet()

    def process_random_command(self):
        random_message: Message = choice(Message.objects.filter(message_type='photo'))
        self.bot.forward_message(self.chat_id, self.chat_id, random_message.message_id)
