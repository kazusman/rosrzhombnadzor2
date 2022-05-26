from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import truncatechars


ON_DELETE_VALUE = {True: models.CASCADE, False: models.RESTRICT}

MESSAGE_TYPE_CHOICES = [
    ("text", "Text"),
    ("photo", "Photo"),
    ("video", "Video"),
    ("audio", "Audio"),
    ("document", "Document"),
    ("sticker", "Sticker"),
    ("voice", "Voice"),
    ("video_note", "Video note"),
    ("animation", "GIF"),
]

WORD_POSITION_CHOICES = [
    ("start", "Предложение начинается на"),
    ("clean_start", "Является первым словом в предложении"),
    ("end", "Предложение заканчивается на"),
    ("clean_end", "Является последним словом в предложении"),
    ("all", "Полностью равно"),
    ("any", "В любом месте"),
]

ANSWER_TYPES = [
    ("text", "Text"),
    ("photo", "Photo"),
    ("video", "Video"),
    ("audio", "Audio"),
    ("sticker", "Sticker"),
    ("document", "Document"),
    ("voice", "Voice"),
    ("animation", "GIF"),
    ("video_note", "Video note"),
]


def percent_probability_validator(value):
    if 1 > value > 100:
        raise ValidationError(
            f"Ты мне мозги не еби, я спрашиваю СКОЛЬКО? Какие нахуй {value} процентов, дядя?"
        )


class User(models.Model):

    telegram_id = models.BigIntegerField(verbose_name="Telegram ID", unique=True)

    username = models.CharField(
        max_length=32, verbose_name="Username", null=True, blank=True
    )

    first_name = models.CharField(
        max_length=64, verbose_name="First name", null=True, blank=True
    )

    last_name = models.CharField(
        max_length=64, verbose_name="Last name", null=True, blank=True
    )

    sex = models.CharField(
        max_length=1,
        verbose_name='Sex',
        choices=[("m", "Male"), ("f", "Female"), ("h", "Helicopter")],
        default="h"
    )

    coins = models.FloatField(verbose_name="Coins", default=10000)

    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)

    date_of_birth = models.DateField(
        verbose_name="Date of birth", null=True, blank=True
    )

    is_deleted = models.BooleanField(
        default=False, verbose_name="Is user deleted?", choices=settings.BOOLEAN_CHOICES
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.telegram_id} | {self.username}"


class Status(models.Model):

    user = models.ForeignKey(
        to=User, on_delete=ON_DELETE_VALUE[settings.DEBUG], verbose_name="User"
    )

    status = models.CharField(max_length=64, verbose_name="Status")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"

    def __str__(self):
        return f"{self.user} | {self.status}"


class StartAnswer(models.Model):

    answer = models.TextField(verbose_name="Answer")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    @property
    def short_answer_preview(self) -> str:
        return truncatechars(self.answer, 50)

    short_answer_preview.fget.short_description = "Answer preview"

    class Meta:
        verbose_name = "Start answer"
        verbose_name_plural = "Start answers"

    def __str__(self):
        return self.short_answer_preview


class Message(models.Model):

    user = models.ForeignKey(
        to=User, on_delete=ON_DELETE_VALUE[settings.DEBUG], verbose_name="User"
    )

    message_type = models.CharField(
        max_length=32, verbose_name="Message type", choices=MESSAGE_TYPE_CHOICES
    )

    is_forwarded = models.BooleanField(
        verbose_name="Is forwarded?", choices=settings.BOOLEAN_CHOICES, default=False
    )

    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)

    message_text = models.TextField(verbose_name="Message text", null=True, blank=True)

    content_hash = models.CharField(
        verbose_name="MD5 content hash", max_length=128, null=True, blank=True
    )

    file_id = models.CharField(
        verbose_name="File ID", max_length=128, null=True, blank=True
    )

    message_id = models.IntegerField(verbose_name="Message ID")

    text_on_image = models.TextField(
        verbose_name="Text from image", null=True, blank=True
    )

    recognition_type = models.CharField(
        max_length=32, null=True, blank=True, verbose_name="Recognition type"
    )

    json_body = models.JSONField(null=True, blank=True, verbose_name="JSON Body")

    @property
    def content_text_preview(self):
        if self.text_on_image is None:
            return "-"
        return truncatechars(self.text_on_image, 50)

    content_text_preview.fget.short_description = "Content text preview"

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.user} | {self.message_type}"


class NotFoundAnswer(models.Model):

    text = models.TextField(verbose_name="Text")

    class Meta:
        verbose_name = "Not found meme answer"
        verbose_name_plural = "Not found meme answers"

    @property
    def text_preview(self) -> str:
        return truncatechars(self.text, 50)

    text_preview.fget.short_description = "Text preview"

    def __str__(self):
        return self.text_preview


class FunnyAction(models.Model):

    word_position = models.CharField(
        max_length=64, verbose_name="Word position", choices=WORD_POSITION_CHOICES
    )

    trigger_word = models.TextField(verbose_name="Trigger word")

    answer_type = models.CharField(
        verbose_name="Answer type", max_length=32, default="text", choices=ANSWER_TYPES
    )

    answer_text = models.TextField(verbose_name="Answer text", null=True, blank=True)

    file_id = models.CharField(
        verbose_name="File ID", max_length=128, null=True, blank=True
    )

    is_interpolation_needed = models.BooleanField(
        default=False,
        verbose_name="Is interpolation needed?",
        choices=settings.BOOLEAN_CHOICES,
    )

    is_need_to_reply = models.BooleanField(
        default=False, choices=settings.BOOLEAN_CHOICES, verbose_name="Need to reply?"
    )

    is_need_to_send_quiet = models.BooleanField(
        default=False,
        choices=settings.BOOLEAN_CHOICES,
        verbose_name="Need to send quiet?",
    )

    is_case_sensitive = models.BooleanField(
        default=False,
        choices=settings.BOOLEAN_CHOICES,
        verbose_name="Is case sensitive",
    )

    answer_probability = models.IntegerField(
        validators=[percent_probability_validator], verbose_name="Answer probability"
    )

    @property
    def answer_preview(self) -> str:
        return truncatechars(self.answer_text, 50)

    answer_preview.fget.short_description = "Answer preview"

    class Meta:
        verbose_name = "Funny action"
        verbose_name_plural = "Funny actions"

    def __str__(self):
        return self.word_position


class Bet(models.Model):

    user = models.ForeignKey(
        to=User, on_delete=ON_DELETE_VALUE[settings.DEBUG], verbose_name="Bet author"
    )

    message = models.ForeignKey(
        to=Message, on_delete=ON_DELETE_VALUE[settings.DEBUG], verbose_name="Message"
    )

    bet_target_user = models.ForeignKey(
        to=User,
        on_delete=ON_DELETE_VALUE[settings.DEBUG],
        verbose_name="Bet target user",
        related_name="target_bet_user",
        null=True,
    )

    amount = models.FloatField(verbose_name="Amount", null=True)

    is_funny = models.BooleanField(
        verbose_name="Is funny?", null=True, choices=settings.BOOLEAN_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    bot_message_id = models.IntegerField(verbose_name="Bot message ID", null=True)

    is_declined = models.BooleanField(
        default=False, verbose_name="Is declined?", choices=settings.BOOLEAN_CHOICES
    )

    declined_at = models.DateTimeField(verbose_name="Declined at", null=True)

    class Meta:
        verbose_name = "Bet"
        verbose_name_plural = "Bets"

    def __str__(self):
        return f"{self.user} | {self.bet_target_user}"


class Anekdot(models.Model):

    anek = models.TextField(unique=True, verbose_name="Anekdot")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    @property
    def anek_preview(self):
        return truncatechars(self.anek, 50)

    anek_preview.fget.short_description = "Anek preview"

    class Meta:
        verbose_name = "Anekdot"
        verbose_name_plural = "Anekdots"

    def __str__(self):
        return self.anek_preview


class Donate(models.Model):

    from_user = models.ForeignKey(
        to=User, on_delete=ON_DELETE_VALUE[settings.DEBUG], verbose_name="From user"
    )

    to_user = models.ForeignKey(
        to=User,
        on_delete=ON_DELETE_VALUE[settings.DEBUG],
        verbose_name="To user",
        related_name="to_user",
        null=True,
    )

    amount = models.FloatField(verbose_name="Amount", null=True)

    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)

    class Meta:
        verbose_name = "Donate"
        verbose_name_plural = "Donates"

    def __str__(self):
        return f"{self.from_user} to {self.to_user}"


class DemotivatorText(models.Model):

    text = models.CharField(
        max_length=80,
        verbose_name="Demotivator text",
    )

    class Meta:
        verbose_name = "Demotivator text"
        verbose_name_plural = "Demotivator texts"

    def __str__(self):
        return self.text


class SearchRequest(models.Model):

    user = models.ForeignKey(
        to=User, on_delete=ON_DELETE_VALUE[settings.DEBUG], verbose_name="User"
    )

    search_text = models.TextField(verbose_name="Search text")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Search text")

    class Meta:
        verbose_name = "Search request"
        verbose_name_plural = "Search requests"

    def __str__(self):
        return truncatechars(self.search_text, 50)
