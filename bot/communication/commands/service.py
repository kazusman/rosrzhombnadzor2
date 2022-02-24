import requests

from bot.service import ActionProcessor, get_readable_balance
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
        users = User.objects.filter(
            ~Q(telegram_id=self.telegram_id), is_deleted=False, coins__gt=0
        ).order_by('username')
        if len(users) == 0:
            self.bot.send_message(self.chat_id, text.POOR_USERS)
            return
        reply_markup = self.markup.bet_user_list(users)
        new_message = self.bot.send_message(self.chat_id, text.SELECT_TARGET_USER, reply_markup=reply_markup)
        Bet.objects.create(
            user=self.database_user,
            message=message,
            bot_message_id=new_message.id
        )

    def _create_donate(self) -> Donate:
        return Donate.objects.create(
            from_user=self.database_user
        )

    def _get_file_id(self):
        try:
            message = Message.objects.get(
                message_id=self.action.reply_to_message.message_id
            )
        except ObjectDoesNotExist:
            self.bot.send_message(self.chat_id, text.FILE_ID_NO_MESSAGE)
            return
        if message.file_id is None:
            self.bot.send_message(self.chat_id, text.FILE_ID_DOES_NOT_EXIST)
            return
        self.bot.send_message(self.chat_id, f'<code>{message.file_id}</code>', parse_mode='HTML')

    def process_start_command(self):
        message_text: str = choice(StartAnswer.objects.all()).answer
        self.bot.send_message(self.chat_id, message_text, parse_mode='HTML')

    def process_search_command(self):
        self.update_status('search_meme')
        self.bot.send_message(self.chat_id, text.LETS_SEARCH)

    def process_bet_command(self):
        if self.action.reply_to_message is None:
            self.bot.send_message(self.chat_id, text.NEED_TO_REPLY)
        elif self.database_user.coins == 0:
            self.bot.send_video(self.chat_id,
                                'BAACAgIAAx0CR_H_4AACklRiFW6us_ckKu7dPtN0k4Z6XyN_CQAC4hQAArxdqEi3SfbD7ZuF3yME')
        else:
            self._create_bet()

    def process_random_command(self):
        random_message: Message = choice(Message.objects.filter(message_type='photo'))
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
        users = User.objects.filter(is_deleted=False).order_by('-coins')
        stat_text = ''
        for user in users:
            stat_text += f'{user.username}: {get_readable_balance(user.coins)}\n'
        self.bot.send_message(self.chat_id, text.DAILY_STAT.format(stat_text))

    def process_donate_command(self):
        if self.database_user.coins == 0:
            self.bot.send_message(self.chat_id, text.DONATE_ZERO_BALANCE)
            return
        users = User.objects.filter(is_deleted=False).order_by('username')
        donate = self._create_donate()
        self.update_status(f'donate_id:{donate.id}')
        reply_markup = self.markup.donate_user_list(users, donate.id)
        self.bot.send_message(self.chat_id, text.SELECT_MONEY_RECEIVER, reply_markup=reply_markup)
