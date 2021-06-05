import requests

from django.db import models
from tgbot import utils

import random


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    language_code = models.CharField(max_length=8, null=True, blank=True, help_text="Telegram client's lang")
    deep_link = models.CharField(max_length=64, null=True, blank=True)

    is_blocked_bot = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.user_id}'

    @classmethod
    def get_user_and_created(cls, update, context):
        """ python-telegram-bot's Update, Context --> User instance """
        data = utils.extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(user_id=data["user_id"], defaults=data)

        if created:
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(data["user_id"]).strip():  # you can't invite yourself
                    u.deep_link = payload
                    u.save()

        return u, created

    @classmethod
    def get_user(cls, update, context):
        u, _ = cls.get_user_and_created(update, context)
        return u

    @classmethod
    def get_user_by_username_or_user_id(cls, string):
        """ Search user in DB, return User or None if not found """
        username = str(string).strip().lower()
        if string.startswith('@'):
            return cls.objects.filter(username__iexact=username).first()
        elif username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        else:
            return None


class Translation(models.Model):
    native_text = models.CharField(max_length=256)
    translated_text = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.native_text} - {self.translated_text}'

    @classmethod
    def get_unknown_translation_for_user(cls, user):
        """ Search unknown word in DB, return None if not found """
        known_translations_ids = KnownUserTranslation.objects.filter(user=user).values_list('translation', flat=True)
        unknown_translation = Translation.objects.exclude(id__in=known_translations_ids).first()
        return unknown_translation

    @classmethod
    def get_random_known_translation_for_user(cls, user):
        """ Search known word in DB, return None if not found """
        known_translations_ids = KnownUserTranslation.objects.filter(user=user).values_list('translation', flat=True)
        known_count = known_translations_ids.count()
        if known_count == 0:
            return None
        random_index = random.randrange(known_count)
        random_id = known_translations_ids[random_index]
        random_known_translation = Translation.objects.get(pk=random_id)
        return random_known_translation


class KnownUserTranslation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)


class CurrentUserQuiz(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    known_translation = models.OneToOneField(KnownUserTranslation, on_delete=models.CASCADE)


class UserActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user: {self.user}, made: {self.action}, created at {self.created_at.strftime('(%H:%M, %d %B %Y)')}"
