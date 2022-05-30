from typing import Optional

from django.db.models import QuerySet
from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup
from telebot.types import ReplyKeyboardMarkup

from bot.models import SearchRequest
from bot.models import User


class Markup:
    def __init__(self, user: User):
        self.user = user

    @staticmethod
    def bet_user_list(users: QuerySet[User]) -> InlineKeyboardMarkup:

        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        for user in users:
            if user.username is None:
                user.username = user.first_name
        markup.add(
            *[
                InlineKeyboardButton(
                    user.username, callback_data=f"bet_target_user:{user.id}"
                )
                for user in users
            ]
        )
        return markup

    @staticmethod
    def funny_or_not(bet_id: int):
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("Прикол работает", callback_data=f"haha:{bet_id}"),
            InlineKeyboardButton("Не поржал", callback_data=f"not_haha:{bet_id}"),
        )
        markup.add(
            InlineKeyboardButton("Отменить", callback_data=f"decline:{bet_id}"),
            InlineKeyboardButton("Уже видел", callback_data=f"already_haha:{bet_id}"),
        )
        return markup

    @staticmethod
    def donate_user_list(users: QuerySet[User]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        for user in users:
            if user.username is None:
                user.username = user.first_name
        markup.row_width = 2
        markup.add(
            *[
                InlineKeyboardButton(
                    user.username, callback_data=f"donate_to_user:{user.id}"
                )
                for user in users
            ]
        )
        return markup

    @staticmethod
    def next_pages_buttons(
        search_request: SearchRequest, pages_count: int
    ) -> Optional[InlineKeyboardMarkup]:
        if pages_count == 1:
            return
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🤔", callback_data="empty_back_button"),
            InlineKeyboardButton(
                f"1/{pages_count}",
                callback_data=f"amount_of_pages:{search_request.id}:{pages_count}",
            ),
            InlineKeyboardButton(
                "➡️", callback_data=f"next_page:2:{search_request.id}"
            ),
        )
        return markup

    @staticmethod
    def all_paginator_buttons(
        search_request: SearchRequest, pages_count: int, current_page: int
    ) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=3)
        if current_page == pages_count:
            buttons = [
                InlineKeyboardButton(
                    "⬅️",
                    callback_data=f"previous_page:{current_page - 1}:{search_request.id}",
                ),
                InlineKeyboardButton(
                    f"{current_page}/{pages_count}",
                    callback_data=f"amount_of_pages:{search_request.id}:{pages_count}",
                ),
                InlineKeyboardButton("🤔️", callback_data="empty_button"),
            ]
        elif current_page == 1:
            buttons = [
                InlineKeyboardButton("🤔️", callback_data="empty_button"),
                InlineKeyboardButton(
                    f"{current_page}/{pages_count}",
                    callback_data=f"amount_of_pages:{search_request.id}:{pages_count}",
                ),
                InlineKeyboardButton(
                    "➡️",
                    callback_data=f"next_page:{current_page + 1}:{search_request.id}",
                ),
            ]
        else:
            buttons = [
                InlineKeyboardButton(
                    "⬅️",
                    callback_data=f"previous_page:{current_page - 1}:{search_request.id}",
                ),
                InlineKeyboardButton(
                    f"{current_page}/{pages_count}",
                    callback_data=f"amount_of_pages:{search_request.id}:{pages_count}",
                ),
                InlineKeyboardButton(
                    "➡️",
                    callback_data=f"next_page:{current_page + 1}:{search_request.id}",
                ),
            ]
        markup.add(*buttons)
        return markup

    @staticmethod
    def get_all_pages(pages_count: int, search_request_id: int) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=5)
        buttons = [
            InlineKeyboardButton(
                str(i + 1), callback_data=f"get_page:{i + 1}:{search_request_id}"
            )
            for i in range(pages_count)
        ]
        markup.add(*buttons)
        return markup

    @staticmethod
    def get_download_buttons(resolutions: list, message_id: int) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=3)
        buttons = [InlineKeyboardButton(f"{resolution}p", callback_data=f'download:{resolution}:{message_id}')
                   for resolution in resolutions]
        markup.add(*buttons)
        return markup
