import re

import telegram

from tgbot.handlers import static_text
from tgbot.models import User
from tgbot.utils import extract_user_data_from_update
from tgbot.handlers.utils import handler_logging
from tgbot.handlers.keyboard_utils import keyboard_confirm_decline_broadcasting
from tgbot.handlers.manage_data import CONFIRM_DECLINE_BROADCAST, CONFIRM_BROADCAST
from tgbot.tasks import broadcast_message

from dtb.settings import ADMIN_ID


@handler_logging()
def admin(update, context) -> 'telegram.Message':
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)

    if u.user_id == ADMIN_ID:
        u.is_admin = True
        u.save()

    if not u.is_admin:
        return update.message.reply_text(static_text.no_access)

    return update.message.reply_text(static_text.secret_admin_commands)


@handler_logging()
def broadcast_command_with_message(update, context) -> 'telegram.Message':
    """ Type /broadcast <some_text>. Then check your message in Markdown format and broadcast to users."""
    u = User.get_user(update, context)
    user_id = extract_user_data_from_update(update)['user_id']

    if not u.is_admin:
        return update.message.reply_text(static_text.no_access)

    text = f"{update.message.text.replace(f'/broadcast', '', 1).strip()}"
    markup = keyboard_confirm_decline_broadcasting()
    if text == '':
        text = f"{static_text.empty_message}\n{static_text.broadcast_help}"
        markup = None

    try:
        return context.bot.send_message(
            text=text,
            chat_id=user_id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=markup
        )
    except telegram.error.BadRequest as e:
        place_where_mistake_begins = re.findall(r"offset (\d{1,})$", str(e))
        text_error = static_text.error_with_markdown
        if len(place_where_mistake_begins):
            text_error += f"{static_text.specify_word_with_error}'{text[int(place_where_mistake_begins[0]):].split(' ')[0]}'"
        return context.bot.send_message(
            text=text_error,
            chat_id=user_id
        )


def broadcast_decision_handler(update, context):  # callback_data: CONFIRM_DECLINE_BROADCAST from manage_data.py
    """ Entered /broadcast <some_text>.
        Shows text in Markdown style with two buttons:
        Confirm and Decline
    """
    broadcast_decision = update.callback_query.data[len(CONFIRM_DECLINE_BROADCAST):]
    entities_for_celery = update.callback_query.message.to_dict().get('entities')
    text = update.callback_query.message.text
    if broadcast_decision == CONFIRM_BROADCAST:
        admin_text = f"{static_text.message_is_sent}"
        user_ids = list(User.objects.all().values_list('user_id', flat=True))
        broadcast_message(user_ids=user_ids, message=text, entities=entities_for_celery)
    else:
        admin_text = static_text.declined_message_broadcasting

    context.bot.edit_message_text(
        text=admin_text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
    )
