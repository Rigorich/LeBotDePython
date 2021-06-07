"""
    Celery tasks. Some of them will be launched periodically from admin panel via django-celery-beat
"""

import time

import telegram
from telegram import MessageEntity

from dtb.celery import app
from dtb.settings import TELEGRAM_TOKEN
from celery.utils.log import get_task_logger

from tgbot.models import User


logger = get_task_logger(__name__)

@app.task(ignore_result=True)
def broadcast_message(user_ids, message, entities=None, parse_mode=None):
    """ It's used to broadcast message to big amount of users """
    logger.info(f"Going to send message: '{message}' to {len(user_ids)} users")
    bot = telegram.Bot(TELEGRAM_TOKEN)
    for user_id in user_ids:
        try:
            if entities:
                entities = [
                    MessageEntity(type=entity['type'],
                                  offset=entity['offset'],
                                  length=entity['length']
                                  )
                    for entity in entities
                ]

            m = bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode=parse_mode,
                entities=entities,
            )
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}. Reason: {e}")
        else:
            User.objects.filter(user_id=user_id).update(is_blocked_bot=False)
            logger.info(f"Broadcast message was sent to {user_id}")
        time.sleep(0.1)
    logger.info("Broadcast finished!")
