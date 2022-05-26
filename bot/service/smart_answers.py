from bot.models import User
from random import randint
from random import choice


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
    def get_users_list() -> str:
        users = User.objects.filter(is_deleted=False).order_by("-username")
        users_list = ""
        for user in users:
            current_user = f"@{user.username}"
            if not user.username:
                current_user = (
                    f"<a href='tg://user?id={user.telegram_id}'>{user.first_name}</a>"
                )
            users_list += current_user + " "
        return users_list

    def get_gay_percent(self) -> str:
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
        return answer

    def get_dick_length(self) -> str:
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
            return f"У тебя нет {organ}, в курсе?"
        return f"У тебя {param} {organ} {length} {unit}, в курсе?"

    @staticmethod
    def get_confirmation() -> str:
        return choice(["Подтверждаю", "Не подтверждаю"])

    def get_rzhomb_award(self) -> str:
        if randint(1, 100) == 1:
            self.user.coins = self.user.coins + 10000
            self.user.save()
            answer = """
ПОЗДРАВЛЯЮ!
Вы получаете ЗОЛОТУЮ РЖОМБУ и 10 000 Ржомбкоинов в качестве приза!
Вероятность этого события - 1%!
████████████████████████████████████████
████████████████████████████████████████
██████▀░░░░░░░░▀████████▀▀░░░░░░░▀██████
████▀░░░░░░░░░░░░▀████▀░░░░░░░░░░░░▀████
██▀░░░░░░░░░░░░░░░░▀▀░░░░░░░░░░░░░░░░▀██
██░░░░░░░░░░░░░░░░░░░▄▄░░░░░░░░░░░░░░░██
██░░░░░░░░░░░░░░░░░░█░█░░░░░░░░░░░░░░░██
██░░░░░░░░░░░░░░░░░▄▀░█░░░░░░░░░░░░░░░██
██░░░░░░░░░░████▄▄▄▀░░▀▀▀▀▄░░░░░░░░░░░██
██▄░░░░░░░░░████░░░░░░░░░░█░░░░░░░░░░▄██
████▄░░░░░░░████░░░░░░░░░░█░░░░░░░░▄████
██████▄░░░░░████▄▄▄░░░░░░░█░░░░░░▄██████
████████▄░░░▀▀▀▀░░░▀▀▀▀▀▀▀░░░░░▄████████
██████████▄░░░░░░░░░░░░░░░░░░▄██████████
████████████▄░░░░░░░░░░░░░░▄████████████
██████████████▄░░░░░░░░░░▄██████████████
████████████████▄░░░░░░▄████████████████
██████████████████▄▄▄▄██████████████████
████████████████████████████████████████
████████████████████████████████████████
"""
            return answer
        return ""
