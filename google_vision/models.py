import json
from django.conf import settings
from django.db import models
from pygments import highlight
from pygments.lexers.data import JsonLexer
from pygments.formatters.html import HtmlFormatter
from bot.models import Message
from bot.models import ON_DELETE_VALUE
from django.utils.safestring import mark_safe


class Request(models.Model):

    response = models.JSONField(verbose_name="Google API Response")

    message = models.ForeignKey(
        to=Message,
        on_delete=ON_DELETE_VALUE[settings.DEBUG],
        verbose_name="Message",
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def pretty_json(self):
        response = json.dumps(self.response, indent=2, ensure_ascii=False)
        formatter = HtmlFormatter(style='colorful')
        response = highlight(response, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        return mark_safe(style + response)

    pretty_json.short_description = 'Pretty json'
    pretty_json.allow_tags = True

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"

    def __str__(self):
        return str(self.response)[:50]


class RecognitionType(models.Model):

    type = models.CharField(max_length=32, verbose_name="Type")

    is_main = models.BooleanField(
        verbose_name="Is main?", default=False, choices=settings.BOOLEAN_CHOICES
    )

    class Meta:
        verbose_name = "Recognition type"
        verbose_name_plural = "Recognition types"

    def __str__(self):
        return f"{self.type} | {self.is_main}"
