from django.contrib import admin

from tgbot.models import User, UserActionLog, Translation, KnownUserTranslation, CurrentUserQuiz


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'username', 'first_name', 'last_name',
        'language_code', 'deep_link',
        'created_at', 'updated_at', "is_blocked_bot",
    ]
    list_filter = ["is_blocked_bot", "is_moderator"]
    search_fields = ('username', 'user_id')


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ['native_text', 'translated_text']


@admin.register(KnownUserTranslation)
class KnownUserTranslationAdmin(admin.ModelAdmin):
    list_display = ['user', 'translation']


@admin.register(CurrentUserQuiz)
class CurrentUserQuizAdmin(admin.ModelAdmin):
    list_display = ['user', 'known_translation']


@admin.register(UserActionLog)
class UserActionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'created_at']
