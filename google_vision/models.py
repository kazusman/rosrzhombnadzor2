from django.db import models
from django.template.defaultfilters import truncatechars
from bot.models import Message, ON_DELETE_VALUE
from django.conf import settings


class Request(models.Model):

    response = models.JSONField(
        verbose_name='Google API Response'
    )

    message = models.ForeignKey(
        to=Message,
        on_delete=ON_DELETE_VALUE[settings.DEBUG],
        verbose_name='Message',
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )

    @property
    def response_preview(self) -> str:
        return truncatechars(str(self.response), 50)

    response_preview.fget.short_description = 'Response preview'

    class Meta:
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'

    def __str__(self):
        return self.response_preview


class RecognitionType(models.Model):

    type = models.CharField(
        max_length=32,
        verbose_name='Type'
    )

    is_main = models.BooleanField(
        verbose_name='Is main?',
        default=False,
        choices=settings.BOOLEAN_CHOICES
    )

    class Meta:
        verbose_name = 'Recognition type'
        verbose_name_plural = 'Recognition types'

    def __str__(self):
        return f'{self.type} | {self.is_main}'
