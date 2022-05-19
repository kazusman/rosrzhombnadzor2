from bot.models import User
from random import randint


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

    @staticmethod
    def get_gay_percent() -> str:
        gayness = randint(0, 100)
        if gayness == 0:
            result = "вообще базированный натурал без капли гейства"
        else:
            result = f"на {gayness}% гей"
        answer = f"Кстати, внеплановая проверка на гейство показала, что ты {result}, поздравляю!"
        return answer

    @staticmethod
    def get_dick_length() -> str:
        length = randint(0, 100)
        if not length:
            return "У тебя нет хуя, в курсе?"
        return f"У тебя хуй {length} см, в курсе?"
