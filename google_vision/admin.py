from django.contrib import admin
from google_vision.models import *


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'message',
        'response_preview',
        'created_at'
    )

    list_display_links = list_display

    list_filter = (
        'created_at',
    )

    readonly_fields = (
        'created_at',
        'message'
    )
