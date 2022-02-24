from bot.config import bot
from telebot import types  # noqa
from bot.communication.inline_buttons.service import InlineProcessor


def call_data(call: types.CallbackQuery) -> str:

    if ':' in call.data:
        return call.data.split(':')[0]
    else:
        return call.data


@bot.callback_query_handler(func=lambda call: call_data(call) == 'bet_target_user')
def bet_target_user_call(call: types.CallbackQuery):

    InlineProcessor(call).process_bet_target_user()


@bot.callback_query_handler(func=lambda call: call_data(call) == 'haha')
def haha_call(call: types.CallbackQuery):

    InlineProcessor(call).process_haha_call()


@bot.callback_query_handler(func=lambda call: call_data(call) == 'not_haha')
def not_haha_call(call: types.CallbackQuery):

    InlineProcessor(call).process_not_haha_call()


@bot.callback_query_handler(func=lambda call: call_data(call) == 'decline')
def decline_call(call: types.CallbackQuery):

    InlineProcessor(call).process_decline_bet()


@bot.callback_query_handler(func=lambda call: call_data(call) == 'already_haha')
def already_haha_call(call: types.CallbackQuery):

    InlineProcessor(call).process_already_haha()


@bot.callback_query_handler(func=lambda call: call_data(call) == 'donate_to_user')
def to_user_donate_call(call: types.CallbackQuery):

    InlineProcessor(call).process_to_donate_call()