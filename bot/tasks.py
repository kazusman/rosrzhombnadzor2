from celery import shared_task

from bot.service.jobs import give_money
from bot.service.jobs import happy_birthday_messages
from bot.service.jobs import send_daily_stat
from bot.service.jobs import set_eight_march_avatar
from bot.service.jobs import set_nine_march_avatar
from bot.service.jobs import kick_lazy_users


@shared_task
def give_weekly_coins():
    give_money()


@shared_task
def send_happy_birthday():
    happy_birthday_messages()


@shared_task
def daily_stat():
    send_daily_stat()


@shared_task
def eight_march_avatar():
    set_eight_march_avatar()


@shared_task
def nine_march_avatar():
    set_nine_march_avatar()


@shared_task
def lazy_users_check():
    kick_lazy_users()
