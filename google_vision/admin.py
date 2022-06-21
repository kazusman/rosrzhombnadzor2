from django.contrib import admin

from google_vision.models import *


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):

    list_display = ("id", "message", "created_at")

    list_display_links = list_display

    list_filter = ("created_at",)

    exclude = ("response",)

    readonly_fields = ("created_at", "pretty_json", "message")


@admin.register(RecognitionType)
class RecognitionTypeAdmin(admin.ModelAdmin):

    list_display = ("id", "type", "is_main")
    list_display_links = list_display
