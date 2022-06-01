from random import choice
from typing import Union

from telebot import types  # noqa

from bot.models import *
from bot.service import ActionProcessor
from bot.service import get_mention_user
from bot.service import get_readable_balance
from bot.service import search_paginator
from bot.service import text
from bot.service.funny_answer import TextAnalyzer


class TextProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку входящих текстовых сообщений от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)

    amount: str

    def _process_search_meme(self):
        if len(self.message_text) <= 2:
            random_answer = choice(NotFoundAnswer.objects.all()).text
            self.bot.send_message(self.chat_id, random_answer)
            return
        found_memes = search_paginator.Paginator(
            self.database_user, self.message_text
        ).find_messages()
        if found_memes["found"]:
            message_text = found_memes["message_text"]
            reply_markup = found_memes["reply_markup"]
            self.bot.send_message(
                self.chat_id, message_text, reply_markup=reply_markup, parse_mode="HTML"
            )
        else:
            random_answer = choice(NotFoundAnswer.objects.all())
            self.bot.send_message(self.chat_id, random_answer.text, parse_mode="HTML")

    def _is_float(self) -> bool:
        try:
            self.amount = self.message_text.replace(",", ".").replace(" ", "")
            float(self.amount)
            return True
        except ValueError:
            return False

    def _add_amount_to_bet(self, bet: Bet):
        bet.amount = float(self.amount)
        bet.save()

    def _process_bet_amount(self):
        self.bot.delete_message(self.chat_id, self.message_id)
        bet_id = int(self.status.split(":")[1])
        if self._is_float():
            float_amount = round(float(self.amount), 2)
            bet = Bet.objects.get(id=bet_id)
            if float_amount > self.database_user.coins:
                self.bot.send_message(self.chat_id, text.TOO_MUCH)
                return
            elif float_amount > bet.bet_target_user.coins:
                self.bot.send_message(
                    self.chat_id,
                    text.TOO_MUCH_TARGET.format(bet.bet_target_user.username),
                )
                return
            elif float_amount == 0:
                self.bot.send_message(self.chat_id, text.ZERO_NOT_ALLOWED)
                return
            self._add_amount_to_bet(bet)
            reply_markup = self.markup.funny_or_not(bet.id)
            self.bot.send_message(
                self.chat_id,
                text.CALL_TARGET_USER.format(
                    get_mention_user(bet.user),
                    get_mention_user(bet.bet_target_user),
                ),
                reply_markup=reply_markup,
                parse_mode="HTML",
            )
            self.update_status("rzhomber")
        else:
            self.bot.send_message(self.chat_id, text.SEND_FLOAT_AMOUNT)
            self.update_status("rzhomber")

    @staticmethod
    def _provide_donate_amounts(donate: Donate, float_amount: float):
        donate.amount, donate.to_user.coins, donate.from_user.coins = (
            float_amount,
            donate.to_user.coins + float_amount,
            donate.from_user.coins - float_amount,
        )
        donate.save()
        donate.to_user.save()
        donate.from_user.save()

    def _process_donate_amount(self):
        if self._is_float():
            float_amount = round(float(self.amount), 2)
            if float_amount <= 0:
                self.bot.send_message(self.chat_id, text.DONATE_ZERO_AMOUNT)
                return
            if float_amount > self.database_user.coins:
                self.bot.send_message(self.chat_id, text.DONATE_TOO_MUCH_AMOUNT)
                return
            donate_id = int(self.status.split(":")[1])
            donate = Donate.objects.get(id=donate_id)
            self._provide_donate_amounts(donate, float_amount)
            self.update_status("rzhomber")
            self.bot.send_message(
                self.chat_id,
                text.DONATE_FINISHED.format(
                    get_readable_balance(donate.from_user.coins),
                    get_mention_user(donate.to_user),
                    get_readable_balance(donate.to_user.coins),
                ),
                parse_mode="HTML",
            )
        else:
            self.bot.send_message(self.chat_id, text.SEND_FLOAT_AMOUNT)
            self.update_status("rzhomber")

    def process_text_message(self):
        if self.status == "search_meme":
            self._process_search_meme()
            self.update_status("rzhomber")
        elif "waiting_bet_amount" in self.status:
            self._process_bet_amount()
        elif "donate_amount" in self.status:
            self._process_donate_amount()
        else:
            self.save_message(message_text=self.message_text)
            TextAnalyzer(
                self.message_text, self.chat_id, self.message_id, self.database_user
            ).analyze()
