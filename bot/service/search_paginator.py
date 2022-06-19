import math

from django.conf import settings
from django.db.models import Q
from django.db.models import QuerySet

from bot.models import Message
from bot.models import SearchRequest
from bot.models import User
from bot.service import get_readable_date
from bot.service.markup import Markup


class Paginator:
    def __init__(self, user: User, message_text: str):
        self.message_text = message_text
        self.user = user

    messages: QuerySet[Message]
    search_request: SearchRequest

    def _get_pages_count(self) -> int:
        return math.ceil(len(self.messages) / 25)

    def _save_search_request(self):
        self.search_request = SearchRequest.objects.create(
            user=self.user, search_text=self.message_text
        )

    def _get_list_of_messages(
        self, total_amount: int, start_position: int = 0, end_position: int = 25
    ) -> str:
        messages_list = f"Найдено резульатов: {total_amount}\n\n"
        russian_message_types = {"photo": "Фото", "video": "Видео"}
        for i, message in enumerate(
            self.messages[start_position:end_position], start_position + 1
        ):
            if i < 10:
                spaces = "  "
            else:
                spaces = " "
            author_name = (
                message.user.username
                if message.user.username
                else message.user.first_name
            )
            messages_list += (
                f'<code>{i}.{spaces}</code><a href="{settings.CHAT_URL}/{message.message_id}">'
                f"{russian_message_types[message.message_type]}</a> "
                f"{get_readable_date(message.created_at)} ({author_name})\n"
            )
        return messages_list

    def _get_all_messages(self):
        self.messages = Message.objects.filter(
            Q(text_on_image__icontains=self.message_text)
            | Q(text_from_audio__icontains=self.message_text)
        ).order_by("created_at")

    @staticmethod
    def _get_positions(page: int) -> tuple[int, int]:
        return ((page - 1) * 25), ((page - 1) * 25) + 25

    def find_messages(self) -> dict:
        self._save_search_request()
        self._get_all_messages()
        if len(self.messages) == 0:
            return {"found": False}
        pages_count = self._get_pages_count()
        reply_markup = Markup(self.user).next_pages_buttons(
            self.search_request, pages_count
        )
        list_of_messages = self._get_list_of_messages(len(self.messages))
        return {
            "found": True,
            "reply_markup": reply_markup,
            "message_text": list_of_messages,
        }

    def turn_over_page(self, page: int):
        self._get_all_messages()
        pages_count = self._get_pages_count()
        start_position, end_position = self._get_positions(page)
        reply_markup = Markup(self.user).all_paginator_buttons(
            self.search_request, pages_count, page
        )
        list_of_messages = self._get_list_of_messages(
            len(self.messages), start_position, end_position
        )
        return {
            "found": True,
            "reply_markup": reply_markup,
            "message_text": list_of_messages,
        }
