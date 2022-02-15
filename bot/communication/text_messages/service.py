from bot.service import ActionProcessor, text, get_readable_balance
from bot.models import *
from typing import Union
from telebot import types  # noqa
from random import choice
from django.db.models import QuerySet
from datetime import datetime
from bot.service.funny_answer import TextAnalyzer


class TextProcessor(ActionProcessor):

    """
    Класс, отвечающий за обработку входящих текстовых сообщений от пользователя к боту
    """

    def __init__(self, action: Union[types.Message, types.CallbackQuery]):
        super().__init__(action)

    amount: str

    @staticmethod
    def _get_readable_date(date: datetime) -> str:
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

    def _create_list_of_founded_messages(self, messages: QuerySet[Message]) -> str:

        """
        Собираем текстовое сообщение со ссылками на найденные в бд мемы
        """

        messages_list = 'Кое-что нарыл:\n\n'
        for i, message in enumerate(messages, 1):
            messages_list += f'{i}. <a href="{settings.CHAT_URL}/{message.message_id}">Сообщение</a> от ' \
                             f'{self._get_readable_date(message.created_at)}\n'
        return messages_list

    def _process_search_meme(self):

        """
        Ищем мемы в БД
        """

        possible_messages = Message.objects.filter(
            text_on_image__icontains=self.message_text
        ).order_by('created_at')

        if len(possible_messages) > 75:
            self.bot.send_message(self.chat_id, text.TOO_MANY_RESULTS)

        elif len(possible_messages) > 0:
            message_list = self._create_list_of_founded_messages(possible_messages)
            self.bot.send_message(self.chat_id, message_list, parse_mode='HTML')

        else:
            not_found_answer: str = choice(NotFoundAnswer.objects.all()).text
            self.bot.send_message(self.chat_id, not_found_answer)

        self.update_status('rzhomber')

    def _is_float(self) -> bool:
        try:
            self.amount = self.message_text.replace(',', '.').replace(' ', '')
            float(self.amount)
            return True
        except ValueError:
            return False

    def _add_amount_to_bet(self, bet: Bet):
        bet.amount = float(self.amount)
        bet.save()

    def _process_bet_amount(self):
        bet_id = int(self.status.split(':')[1])
        if self._is_float():
            float_amount = round(float(self.amount), 2)
            bet = Bet.objects.get(id=bet_id)
            if float_amount > self.database_user.coins:
                self.bot.send_message(self.chat_id, text.TOO_MUCH)
                return
            elif float_amount > bet.bet_target_user.coins:
                self.bot.send_message(self.chat_id, text.TOO_MUCH_TARGET.format(bet.bet_target_user.username))
                return
            elif float_amount == 0:
                self.bot.send_message(self.chat_id, text.ZERO_NOT_ALLOWED)
                return
            self._add_amount_to_bet(bet)
            reply_markup = self.markup.funny_or_not(bet.id)
            self.bot.send_message(self.chat_id, text.CALL_TARGET_USER.format(
                bet.user.username, bet.bet_target_user.username, get_readable_balance(bet.amount)
            ), reply_markup=reply_markup)
            self.update_status('rzhomber')
        else:
            self.bot.send_message(self.chat_id, text.SEND_FLOAT_AMOUNT)

    def process_text_message(self):
        if self.status == 'search_meme':
            self._process_search_meme()
        elif 'waiting_bet_amount' in self.status:
            self._process_bet_amount()
        else:
            self.save_message(message_text=self.message_text)
            TextAnalyzer(self.message_text, self.chat_id, self.message_id).analyze()
