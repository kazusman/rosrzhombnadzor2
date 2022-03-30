from telebot import types  # noqa

from bot.communication.chat_member.service import ChatMemberProcessor
from bot.config import bot


@bot.message_handler(content_types=["new_chat_members"])
def new_chat_member(message: types.Message):

    ChatMemberProcessor(message).process_new_chat_member()


@bot.message_handler(content_types=["left_chat_member"])
def left_chat_member(message: types.Message):

    ChatMemberProcessor(message).process_left_chat_member()
