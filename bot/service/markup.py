from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton  # noqa
from bot.models import User
from django.db.models import QuerySet


class Markup:

    def __init__(self, user: User):
        self.user = user

    @staticmethod
    def bet_user_list(users: QuerySet[User]) -> InlineKeyboardMarkup:

        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(
            *[
                InlineKeyboardButton(user.username, callback_data=f'bet_target_user:{user.id}') for user in users
            ]
        )
        return markup

    @staticmethod
    def funny_or_not(bet_id: int):
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton('Прикол работает', callback_data=f'haha:{bet_id}'),
            InlineKeyboardButton('Не поржал', callback_data=f'not_haha:{bet_id}')
        )
        markup.add(
            InlineKeyboardButton('Отменить', callback_data=f'decline:{bet_id}'),
            InlineKeyboardButton('Уже видел', callback_data=f'already_haha:{bet_id}')
        )
        return markup

    @staticmethod
    def donate_user_list(users: QuerySet[User]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(
            *[
                InlineKeyboardButton(user.username, callback_data=f'donate_to_user:{user.id}') for user in users
            ]
        )
        return markup
