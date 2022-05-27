from bot.models import User
from random import randint
from random import choice
from bot.models import Message
from datetime import datetime
from datetime import timedelta
from pytz import timezone
from django.conf import settings
from bot.service.text import RZHOMB_AWARD


class SmartAnswer:

    def __init__(self, user: User, message_text: str):
        self.user = user
        self.message_text = message_text

    # def example_method(self) -> str:
    #     Чтобы юзать атрибуты, в методе первым аргументом должен быть self
    #     Если атрибуты не нежны, декорируй метод @staticmethod и не передавай self в аргумент
    #
    #     user = self.user
    #     message_text = self.message_text

    @staticmethod
    def get_users_list() -> tuple[str, str]:
        users = User.objects.filter(is_deleted=False).order_by("-username")
        users_list = ""
        for user in users:
            current_user = f"@{user.username}"
            if not user.username:
                current_user = (
                    f"<a href='tg://user?id={user.telegram_id}'>{user.first_name}</a>"
                )
            users_list += current_user + " "
        return users_list, "text"

    def get_gay_percent(self) -> tuple[str, str]:
        natural = "натурал"
        lesborgay = ['гей', 'гейство', 'гейства']
        if self.user.sex == 'f':
            lesborgay = ['лесбиянка', 'лейсбийство', 'лесбийства']
        if self.user.sex == 'h':
            lesborgay = ['справляешься с боевыми задачами', 'пригодность технической эксплуатации', 'боеприпасов']
            natural = "развалюха"
        gayness = randint(0, 100)
        if gayness == 0:
            result = f"вообще базированный {natural} без капли {lesborgay[2]}"
        else:
            result = f"на {gayness}% {lesborgay[0]}"
        answer = f"Кстати, внеплановая проверка на {lesborgay[1]} показала, что ты {result}, поздравляю!"
        return answer, "text"

    def get_dick_length(self) -> tuple[str, str]:
        organ = 'хуя'
        param = "длина"
        unit = "см"
        if self.user.sex == 'f':
            organ = 'пизды'
            param = 'глубина'
        if self.user.sex == "h":
            organ = "несущего винта"
            param = 'диаметр'
            unit = "м"
        length = randint(0, 35)
        if not length:
            return f"У тебя нет {organ}, в курсе?", "text"
        return f"У тебя {param} {organ} {length} {unit}, в курсе?", "text"

    @staticmethod
    def get_confirmation() -> tuple[str, str]:
        return choice(["Подтверждаю", "Не подтверждаю"]), "text"

    def get_rzhomb_award(self) -> tuple[str, str]:
        if randint(1, 100) == 1:
            filter_datetime = datetime.now(timezone(settings.TIME_ZONE)) - timedelta(hours=24)
            rzhomb_messages = Message.objects.filter(user=self.user, message_text__icontains="ржомб",
                                                     created_at_gte=filter_datetime)
            if len(rzhomb_messages) < 10:
                self.user.coins = self.user.coins + 10000
                self.user.save()
                return RZHOMB_AWARD, "text"
            else:
                return "Ты мог бы получить награду, но слишком много раз за последние 24 часа написал слово ржомба," \
                       "поэтому нюхай бебру", "text"
        return "", "text"

    def get_bens_opinion(self) -> tuple[str, str]:
        if self.message_text.endswith("?"):
            videos = [
                "BAACAgIAAx0CZ5GD1AACCAtij1_db5K0QQJ_TYLE2qjDNUruOAACMhsAAohqeUjwsbuZC0NqaiQE",
                "BAACAgIAAx0CZ5GD1AACCAxij2ABB4B6mAnBa3oEUxlKph6oFAACNRsAAohqeUh6mdJCA3GiRCQE",
                "BAACAgIAAx0CZ5GD1AACCA1ij2AUmGMetmoPDrXHzVb3GuaKQwACNhsAAohqeUjmeeN6mDSwzyQE",
                "BAACAgIAAx0CZ5GD1AACCA5ij2Am7svYi7jAL_gjZ3H3tP2plwACNxsAAohqeUie2dLcegvhpSQE"
            ]
            return choice(videos), "video"
