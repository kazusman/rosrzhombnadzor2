import os
from datetime import datetime
from datetime import timedelta

from django.conf import settings
from pytz import timezone

from bot.config import bot
from bot.models import Bet
from bot.models import Donate
from bot.models import User
from bot.service import get_readable_balance
from bot.service import get_years_decade
from bot.service import text


def give_money():

    users = User.objects.filter(is_deleted=False)
    for user in users:
        new_balance = user.coins + 5000
        user.coins = new_balance
        user.save()
    bot.send_message(settings.CHAT_ID, "Начислил по 5 000 Ржомбакоинов всем причастным")


def happy_birthday_messages():

    current_date = datetime.now(timezone(settings.TIME_ZONE)).date()
    users = User.objects.filter(
        date_of_birth__day=current_date.day, date_of_birth__month=current_date.month
    )
    if len(users) != 0:
        for user in users:
            user.coins = user.coins + 10000
            user.save()
            message = bot.send_message(
                settings.CHAT_ID,
                f"@{user.username}, с днюхой тебя нахуй. С "
                f"{get_years_decade(user)} с чем-то летием блять\n\n🍺🍺🍺",
            )
            bot.send_message(
                settings.CHAT_ID,
                "Начислил 10 000 Ржомбакоинов, но это как на день рождения",
                reply_to_message_id=message.id,
            )


def send_daily_stat():

    current_datetime = datetime.now(timezone(settings.TIME_ZONE))
    yesterday_datetime = current_datetime - timedelta(days=1)
    yesterday_bets = Bet.objects.filter(
        created_at__gt=yesterday_datetime, created_at__lt=current_datetime
    )
    yesterday_donates = Donate.objects.filter(
        created_at__gt=yesterday_datetime, created_at__lt=current_datetime
    )
    if len(yesterday_bets) != 0 or len(yesterday_donates) != 0:
        stat_text = ""
        users = User.objects.filter(is_deleted=False).order_by("-coins")
        for user in users:
            stat_text += f"{user.username if user.username is not None else user.first_name}: " \
                         f"{get_readable_balance(user.coins)}\n"
        bot.send_message(settings.CHAT_ID, text.DAILY_STAT.format(stat_text))


def set_eight_march_avatar():
    message = bot.send_message(settings.CHAT_ID, "С 8 марта, девачьки")
    with open(
        os.path.join(settings.BASE_DIR, "bot", "templates", "8_march.jpg"), "rb"
    ) as avatar:
        bot.set_chat_photo(settings.CHAT_ID, avatar)
    file_path = bot.get_file(message.chat.photo.big_file_id)
    previous_photo_bytes = bot.download_file(file_path)
    with open(
        os.path.join(settings.BASE_DIR, "bot", "templates", "previous.jpg"), "w"
    ) as old_avatar:
        old_avatar.write(previous_photo_bytes)


def set_nine_march_avatar():
    with open(
        os.path.join(settings.BASE_DIR, "bot", "templates", "previous.jpg"), "rb"
    ) as avatar:
        bot.set_chat_photo(settings.CHAT_ID, avatar)
