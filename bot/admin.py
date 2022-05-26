from django.contrib import admin

from bot.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "telegram_id",
        "username",
        "first_name",
        "last_name",
        "sex",
        "coins",
        "created_at",
        "date_of_birth",
        "is_deleted",
    )

    list_display_links = list_display

    list_filter = (
        "telegram_id",
        "username",
        "first_name",
        "last_name",
        "sex",
        "coins",
        "created_at",
        "is_deleted",
    )

    readonly_fields = ("created_at",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):

    list_display = ("id", "user", "status", "created_at")

    list_display_links = list_display

    list_filter = ("user", "created_at")

    readonly_fields = ("created_at",)


@admin.register(StartAnswer)
class StartAnswerAdmin(admin.ModelAdmin):

    list_display = ("id", "short_answer_preview", "created_at")

    list_display_links = list_display

    list_filter = ("created_at",)

    readonly_fields = ("created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "message_type",
        "is_forwarded",
        "created_at",
        "message_id",
        "content_text_preview",
    )

    list_display_links = list_display

    list_filter = ("user", "message_type", "is_forwarded", "created_at")

    readonly_fields = ("created_at",)


@admin.register(NotFoundAnswer)
class NotFoundAnswerAdmin(admin.ModelAdmin):

    list_display = ("id", "text_preview")

    list_display_links = list_display


@admin.register(FunnyAction)
class FunnyActionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "word_position",
        "trigger_word",
        "answer_preview",
        "is_interpolation_needed",
        "is_need_to_reply",
        "is_need_to_send_quiet",
        "is_case_sensitive",
        "answer_probability",
    )

    list_display_links = list_display

    list_filter = (
        "word_position",
        "is_interpolation_needed",
        "is_need_to_reply",
        "is_need_to_send_quiet",
        "is_case_sensitive",
        "answer_probability",
    )


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "message",
        "bet_target_user",
        "amount",
        "is_funny",
        "created_at",
        "is_declined",
    )

    list_display_links = list_display

    list_filter = ("user", "bet_target_user", "is_funny", "created_at", "is_declined")

    readonly_fields = ("created_at", "message")


@admin.register(Anekdot)
class AnekdotAdmin(admin.ModelAdmin):

    list_display = ("id", "anek_preview")

    list_display_links = list_display

    readonly_fields = ("created_at",)


@admin.register(Donate)
class DonateAdmin(admin.ModelAdmin):

    list_display = ("id", "from_user", "to_user", "amount", "created_at")

    list_display_links = list_display

    list_filter = ("from_user", "to_user", "created_at")

    readonly_fields = ("created_at",)


@admin.register(DemotivatorText)
class DemotivatorTextAdmin(admin.ModelAdmin):

    list_display = ("id", "text")
    list_display_links = list_display
