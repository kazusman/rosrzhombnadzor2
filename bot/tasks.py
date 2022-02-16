from celery import shared_task
from bot.service.jobs import give_money, happy_birthday_messages, send_daily_stat


@shared_task
def give_monthly_coins():
    give_money()


@shared_task
def send_happy_birthday():
    happy_birthday_messages()


@shared_task
def daily_stat():
    send_daily_stat()
