from bot.service import ActionProcessor, text, get_readable_balance
from bot.models import User, Bet
from typing import Union
from telebot import types  # noqa
from datetime import datetime
from pytz import timezone
from django.conf import settings


class InlineProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку входящих callback от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)

    def _get_bet(self) -> Bet:
        return Bet.objects.get(bot_message_id=self.message_id)

    def _update_balances(self, author_amount: float, target_user_amount: float, bet: Bet):
        self.database_user.coins = target_user_amount
        self.database_user.save()
        bet.user.coins = author_amount
        bet.user.save()

    @staticmethod
    def _decline_bet(bet: Bet):
        bet.is_declined, bet.declined_at = True, datetime.now(timezone(settings.TIME_ZONE))
        bet.save()

    @staticmethod
    def _close_bet(bet: Bet, is_funny: bool):
        bet.is_funny = is_funny
        bet.save()

    @staticmethod
    def _add_target_user_to_bet(target_user: User, bet: Bet):
        bet.bet_target_user = target_user
        bet.save()

    def process_bet_target_user(self):
        target_user_id = int(self.action.data.split(':')[1])
        target_user = User.objects.get(id=target_user_id)
        bet = self._get_bet()
        self._add_target_user_to_bet(target_user, bet)
        self.update_status(f'waiting_bet_amount:{bet.id}')
        self.bot.edit_message_text(text.SEND_AMOUNT.format(
            get_readable_balance(self.database_user.coins), target_user.username,
            get_readable_balance(target_user.coins)
        ), self.chat_id, self.message_id)

    def process_haha_call(self):
        bet_id = int(self.call_data.split(':')[1])
        bet = Bet.objects.get(id=bet_id)
        if self.database_user != bet.bet_target_user:
            self.bot.answer_callback_query(self.call_id, text.DO_NOT_PRESS_BUTTON, True)
        else:
            self._close_bet(bet, True)
            author_new_amount = bet.user.coins + bet.amount
            target_user_amount = self.database_user.coins - bet.amount
            self._update_balances(author_new_amount, target_user_amount, bet)
            self.bot.edit_message_text(text.BET_FINISHED_HAHA.format(
                bet.user.username, get_readable_balance(bet.user.coins), self.database_user.username,
                get_readable_balance(self.database_user.coins)
            ), self.chat_id, self.message_id)

    def process_not_haha_call(self):
        bet_id = int(self.call_data.split(':')[1])
        bet = Bet.objects.get(id=bet_id)
        if self.database_user != bet.bet_target_user:
            self.bot.answer_callback_query(self.call_id, text.DO_NOT_PRESS_BUTTON, True)
        else:
            self._close_bet(bet, False)
            author_new_amount = bet.user.coins - bet.amount
            target_user_amount = self.database_user.coins + bet.amount
            self._update_balances(author_new_amount, target_user_amount, bet)
            self.bot.edit_message_text(text.BET_FINISHED_NOT_HAHA.format(
                bet.user.username, get_readable_balance(bet.user.coins), self.database_user.username,
                get_readable_balance(self.database_user.coins)
            ), self.chat_id, self.message_id)

    def process_decline_bet(self):
        bet_id = int(self.call_data.split(':')[1])
        bet = Bet.objects.get(id=bet_id)
        if self.database_user != bet.user:
            self.bot.answer_callback_query(self.call_id, text.DO_NOT_PRESS_BUTTON, True)
        else:
            self._decline_bet(bet)
            self.bot.edit_message_text(self.message_text + text.BET_DECLINED, self.chat_id, self.message_id)

    def process_already_haha(self):
        bet_id = int(self.call_data.split(':')[1])
        bet = Bet.objects.get(id=bet_id)
        if self.database_user != bet.bet_target_user:
            self.bot.answer_callback_query(self.call_id, text.DO_NOT_PRESS_BUTTON, True)
        else:
            self._decline_bet(bet)
            self.bot.edit_message_text(self.message_text + text.ALREADY_HAHA, self.chat_id, self.message_id)
