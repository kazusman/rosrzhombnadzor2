import os
from datetime import datetime
from typing import Union

from django.conf import settings
from pytube import YouTube
from pytube.exceptions import PytubeError
from pytube.exceptions import RegexMatchError
from pytz import timezone
from telebot import types  # noqa

from bot.models import Bet
from bot.models import Donate
from bot.models import Message
from bot.models import SearchRequest
from bot.models import User
from bot.service import ActionProcessor
from bot.service import get_mention_user
from bot.service import get_readable_balance
from bot.service import text
from bot.service.search_paginator import Paginator


class InlineProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку входящих callback от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)

    def _get_bet(self) -> Bet:
        return Bet.objects.get(bot_message_id=self.message_id)

    def _update_balances(
        self, author_amount: float, target_user_amount: float, bet: Bet
    ):
        self.database_user.coins = target_user_amount
        self.database_user.save()
        bet.user.coins = author_amount
        bet.user.save()

    @staticmethod
    def _decline_bet(bet: Bet):
        bet.is_declined, bet.declined_at = True, datetime.now(
            timezone(settings.TIME_ZONE)
        )
        bet.save()

    @staticmethod
    def _close_bet(bet: Bet, is_funny: bool):
        bet.is_funny = is_funny
        bet.save()

    @staticmethod
    def _add_target_user_to_bet(target_user: User, bet: Bet):
        bet.bet_target_user = target_user
        bet.save()

    @staticmethod
    def _add_donate_to_user(donate_to_user: User, donate: Donate):
        donate.to_user = donate_to_user
        donate.save()

    @staticmethod
    def _get_search_request(search_request_id: int) -> SearchRequest:
        return SearchRequest.objects.get(id=search_request_id)

    def _get_found_memes_paginator(self) -> Paginator:
        search_request_id = int(self.call_data.split(":")[2])
        search_request = self._get_search_request(search_request_id)
        found_memes = Paginator(self.database_user, search_request.search_text)
        found_memes.search_request = search_request
        return found_memes

    @staticmethod
    def _add_amount_to_bet(bet: Bet, amount: int):
        bet.amount = float(amount)
        bet.save()

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

    def process_bet_target_user(self):
        target_user_id = int(self.action.data.split(":")[1])
        target_user = User.objects.get(id=target_user_id)
        bet = self._get_bet()
        self._add_target_user_to_bet(target_user, bet)
        self.update_status(f"waiting_bet_amount:{bet.id}")
        reply_markup = self.markup.get_default_bet_amount(bet.id)
        self.bot.edit_message_text(
            text.SEND_AMOUNT.format(
                get_readable_balance(self.database_user.coins),
                get_mention_user(target_user),
                get_readable_balance(target_user.coins),
            ),
            self.chat_id,
            self.message_id,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

    def process_haha_call(self):
        bet_id = int(self.call_data.split(":")[1])
        bet = Bet.objects.get(id=bet_id)
        if self.database_user != bet.bet_target_user:
            self.bot.answer_callback_query(self.call_id, text.DO_NOT_PRESS_BUTTON, True)
        else:
            self._close_bet(bet, True)
            author_new_amount = bet.user.coins + bet.amount
            target_user_amount = self.database_user.coins - bet.amount
            self._update_balances(author_new_amount, target_user_amount, bet)
            self.bot.edit_message_text(
                text.BET_FINISHED_HAHA.format(
                    get_mention_user(bet.user),
                    get_readable_balance(bet.user.coins),
                    get_mention_user(self.database_user),
                    get_readable_balance(self.database_user.coins),
                ),
                self.chat_id,
                self.message_id,
                parse_mode="HTML",
            )

    def process_not_haha_call(self):
        bet_id = int(self.call_data.split(":")[1])
        bet = Bet.objects.get(id=bet_id)
        if self.database_user != bet.bet_target_user:
            self.bot.answer_callback_query(self.call_id, text.DO_NOT_PRESS_BUTTON, True)
        else:
            self._close_bet(bet, False)
            author_new_amount = bet.user.coins - bet.amount
            target_user_amount = self.database_user.coins + bet.amount
            self._update_balances(author_new_amount, target_user_amount, bet)
            self.bot.edit_message_text(
                text.BET_FINISHED_NOT_HAHA.format(
                    get_mention_user(bet.user),
                    get_readable_balance(bet.user.coins),
                    get_mention_user(self.database_user),
                    get_readable_balance(self.database_user.coins),
                ),
                self.chat_id,
                self.message_id,
                parse_mode="HTML",
            )

    def process_decline_bet(self):
        bet_id = int(self.call_data.split(":")[1])
        bet = Bet.objects.get(id=bet_id)
        if self.database_user != bet.user:
            self.bot.answer_callback_query(self.call_id, text.DO_NOT_PRESS_BUTTON, True)
        else:
            self._decline_bet(bet)
            self.bot.edit_message_text(
                self.message_text + text.BET_DECLINED, self.chat_id, self.message_id
            )

    def process_already_haha(self):
        bet_id = int(self.call_data.split(":")[1])
        bet = Bet.objects.get(id=bet_id)
        if self.database_user != bet.bet_target_user:
            self.bot.answer_callback_query(self.call_id, text.DO_NOT_PRESS_BUTTON, True)
        else:
            self._decline_bet(bet)
            self.bot.edit_message_text(
                self.message_text + text.ALREADY_HAHA, self.chat_id, self.message_id
            )

    def process_to_donate_call(self):
        donate_to_user_id = int(self.call_data.split(":")[1])
        donate_to_user = User.objects.get(id=donate_to_user_id)
        donate_id = int(self.status.split(":")[1])
        donate = Donate.objects.get(id=donate_id)
        if self.database_user != donate.from_user:
            self.bot.answer_callback_query(self.call_id, text.DO_NOT_PRESS_BUTTON, True)
            return
        if "donate_id" not in self.status:
            self.bot.answer_callback_query(self.call_id, text.DONATE_ROTTEN, True)
            return
        self._add_donate_to_user(donate_to_user, donate)
        self.update_status(f"donate_amount:{donate_id}")
        reply_markup = self.markup.get_default_donate_amount()
        self.bot.edit_message_text(
            text.SEND_DONATE_AMOUNT.format(
                get_readable_balance(self.database_user.coins)
            ),
            self.chat_id,
            self.message_id,
            reply_markup=reply_markup
        )

    def process_turn_over_page(self):
        page = int(self.call_data.split(":")[1])
        found_memes = self._get_found_memes_paginator().turn_over_page(page)
        message_text = found_memes["message_text"]
        reply_markup = found_memes["reply_markup"]
        self.bot.edit_message_text(
            message_text,
            self.chat_id,
            self.message_id,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )

    def process_empty_button(self):
        self.bot.answer_callback_query(self.call_id, "🤔")

    def process_amount_of_pages_call(self):
        search_request_id = int(self.call_data.split(":")[1])
        pages_count = int(self.call_data.split(":")[2])
        reply_markup = self.markup.get_all_pages(pages_count, search_request_id)
        self.bot.edit_message_reply_markup(
            self.chat_id, self.message_id, reply_markup=reply_markup
        )

    def process_download_video_call(self):
        try:
            self.bot.edit_message_text("Качаю...", self.chat_id, self.message_id)
            _, resolution, message_id = self.call_data.split(":")
            message = Message.objects.get(id=int(message_id))
            video = YouTube(message.message_text)
            for stream in video.streams:
                if (
                    stream.mime_type == "video/mp4"
                    and stream.resolution[:-1] == resolution
                    and stream._filesize < 50000000
                    and stream._filesize != 0
                ):
                    file_path = stream.download()
                    self.bot.edit_message_text(
                        "Скачал, отправляю", self.chat_id, self.message_id
                    )
                    self.bot.send_chat_action(self.chat_id, "upload_video")
                    with open(file_path, "rb") as video:
                        self.bot.send_video(self.chat_id, video, caption=stream.title)
                    os.remove(file_path)
                    break
        except KeyError:
            self.bot.edit_message_text(
                "Какая-то внутренная ошибка библиотеки для скачивания, не в этот раз",
                self.chat_id,
                self.message_id,
            )
        except Exception as error:
            self.bot.edit_message_text(
                f"Словил ошибку при скачивании: {error.__class__.__name__}\n\n{error}"
            )

    def process_default_bet_amount_call(self):
        _, bet_id, amount = self.call_data.split(':')
        bet_id = int(bet_id)
        if amount == "full":
            amount = self.database_user.coins
        else:
            amount = int(amount)
        bet = Bet.objects.get(id=bet_id)
        if amount > self.database_user.coins:
            self.bot.answer_callback_query(self.call_id, text.TOO_MUCH_CALLBACK, True)
            return
        elif amount > bet.bet_target_user.coins:
            self.bot.answer_callback_query(
                self.call_id,
                text.TOO_MUCH_TARGET_CALLBACK.format(bet.bet_target_user.username),
                True
            )
            return
        self._add_amount_to_bet(bet, amount)
        self.bot.edit_message_reply_markup(self.chat_id, self.message_id)
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

    def process_default_donate_call(self):
        if self.call_data == "full":
            amount = self.database_user.coins
        else:
            amount = int(self.call_data.split(":")[1])
        if amount > self.database_user.coins:
            self.bot.answer_callback_query(self.call_id, text.DONATE_TOO_MUCH_AMOUNT_CALLBACK, True)
            return
        donate_id = int(self.status.split(":")[1])
        donate = Donate.objects.get(id=donate_id)
        self._provide_donate_amounts(donate, amount)
        self.update_status("rzhomber")
        self.bot.edit_message_reply_markup(self.chat_id, self.message_id)
        self.bot.send_message(
            self.chat_id,
            text.DONATE_FINISHED.format(
                get_readable_balance(donate.from_user.coins),
                get_mention_user(donate.to_user),
                get_readable_balance(donate.to_user.coins),
            ),
            parse_mode="HTML",
        )
