from django.conf import settings


def check_chat(func):

    def wrapper(*args, **kwargs):

        if args[0].chat_id == settings.CHAT_ID:
            return func(*args, **kwargs)
    return wrapper
