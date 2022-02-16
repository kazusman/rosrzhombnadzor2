from bot.models import User, Bet
from bot.config import bot
from bot.service import get_years_decade, get_readable_balance
from django.conf import settings
from datetime import datetime, timedelta
from pytz import timezone


def give_money():

    users = User.objects.filter(is_deleted=False)
    for user in users:
        new_balance = users.coins + 5000
        user.coins = new_balance
        users.save()
    bot.send_message(settings.CHAT_ID, 'Начислил по 5 000 Ржомбакоинов всем причастным')


def happy_birthday_messages():

    current_date = datetime.now(timezone(settings.TIME_ZONE)).date()
    users = User.objects.filter(date_of_birth__day=current_date.day, date_of_birth__month=current_date.month)
    if len(users) != 0:
        for user in users:
            user.coins = user.coins + 10000
            user.save()
            message = bot.send_message(settings.CHAT_ID, f'@{user.username}, с днюхой тебя нахуй. С '
                                                         f'{get_years_decade(user)} с чем-то летием блять\n\n🍺🍺🍺')
            bot.send_message(settings.CHAT_ID, 'Начислил 10 000 Ржомбакоинов, но это как на день рождения',
                             reply_to_message_id=message.id)


def send_daily_stat():

    current_datetime = datetime.now(timezone(settings.TIME_ZONE))
    yesterday_datetime = current_datetime - timedelta(days=1)
    yesterday_bets = Bet.objects.filter(created_at__gt=yesterday_datetime, created_at__lt=current_datetime)
    if len(yesterday_bets) != 0:
        stat_text = ''
        users = User.objects.filter(is_deleted=False).order_by('coins')
        for user in users:
            stat_text += f'{user.username}: {get_readable_balance(user.coins)}\n'
        bot.send_message(settings.CHAT_ID, stat_text)

