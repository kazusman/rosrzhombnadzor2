from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from telebot import types  # noqa

from bot.communication import animations
from bot.communication import audios
from bot.communication import chat_member
from bot.communication import commands
from bot.communication import documents
from bot.communication import inline_buttons
from bot.communication import photos
from bot.communication import stickers
from bot.communication import text_messages
from bot.communication import video_notes
from bot.communication import videos
from bot.communication import voices
from bot.config import bot


def set_webhook(_) -> HttpResponseRedirect:

    """
    Удаляем имеющийся вебхук и устанавливаем новый на URL, указанную в .env. Токен бота в конце используется
    для того, чтобы исключить возможность обращения к webhook-url сторонних лиц, так как они этот токен не знают

    :return: HttpResponseRedirect to admin page
    """

    bot.delete_webhook()
    bot.set_webhook(
        f"{settings.PROJECT_URL}/bot/new_update/{settings.TELEGRAM_BOT_TOKEN}/"
    )
    return HttpResponseRedirect("/admin/")


@csrf_exempt
def new_update(request: WSGIRequest) -> HttpResponse:

    """
    Обрабатываем входящие запросы от телеграм, которые обрабатываются модулями из директории communication приложения
    bot

    :return: HttResponse со статусом 200, если нет ошибок и мы получили POST запрос. 404, если тип запроса любой другой
    """

    if request.method == "POST":
        json_string = request.body.decode("UTF-8")
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)
