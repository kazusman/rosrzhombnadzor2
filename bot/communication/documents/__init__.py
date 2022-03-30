from telebot import types  # noqa

from bot.communication.documents.service import DocumentProcessor
from bot.config import bot


@bot.message_handler(content_types=["document"])
def document_message(message: types.Message):

    DocumentProcessor(message).process_document_message()
