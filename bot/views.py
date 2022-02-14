from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
from bot.config import bot
from django.conf import settings
from telebot import types  # noqa
from bot.communication import audios, commands, documents, photos, stickers, text_messages, video_notes  # noqa
from bot.communication import videos, voices, animations, inline_buttons  # noqa


def set_webhook(_) -> HttpResponseRedirect:

    """
    Удаляем имеющийся вебхук и устанавливаем новый на URL, указанную в .env. Токен бота в конце используется
    для того, чтобы исключить возможность обращения к webhook-url сторонних лиц, так как они этот токен не знают

    :return: HttpResponseRedirect to admin page
    """

    bot.delete_webhook()
    bot.set_webhook(f'{settings.PROJECT_URL}/bot/new_update/{settings.TELEGRAM_BOT_TOKEN}/')
    return HttpResponseRedirect('/admin/')


@csrf_exempt
def new_update(request: WSGIRequest) -> HttpResponse:

    """
    Обрабатываем входящие запросы от телеграм, которые обрабатываются модулями из директории communication приложения
    bot

    :return: HttResponse со статусом 200, если нет ошибок и мы получили POST запрос. 404, если тип запроса любой другой
    """

    if request.method == 'POST':
        json_string = request.body.decode('UTF-8')
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)
