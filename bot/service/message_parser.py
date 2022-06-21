import time

from django.conf import settings
from bot.config import bot
from telebot.apihelper import ApiTelegramException


class Parser:

    def __init__(self, last_message_id: int):
        self.last_message_id = last_message_id

    def parse(self):
        for message_id in range(self.last_message_id + 1):
            try:
                #message = bot.forward_message(settings.PARSER_CHAT_ID, settings.CHAT_ID, 49998)
                message = bot.copy_message(settings.PARSER_CHAT_ID, settings.CHAT_ID, 49998)
                print(message)
            except ApiTelegramException as error:
                if str(error).endswith("the message can't be forwarded"):
                    continue
                else:
                    print(error)
