from dtb.settings import ENABLE_DECORATOR_LOGGING
from django.utils import timezone
from tgbot.models import UserActionLog, User
import logging


def handler_logging():
    """ Turn on this decorator via ENABLE_DECORATOR_LOGGING variable in dtb.settings """
    def decor(func):
        def handler(update, context, *args, **kwargs):
            user = User.get_user(update, context)
            action = f"{update.message.text}"
            UserActionLog.objects.create(user_id=user.user_id, action=action, created_at=timezone.now())
            logging.info(f"{'@'+user.username if user.username is not None else user.user_id} -> {action}")
            return func(update, context, *args, **kwargs)
        return handler if ENABLE_DECORATOR_LOGGING else func
    return decor
