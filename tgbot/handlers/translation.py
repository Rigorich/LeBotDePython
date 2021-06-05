import telegram

from tgbot.handlers import static_text
from tgbot.models import User, Translation, KnownUserTranslation
from tgbot.utils import extract_user_data_from_update

from tgbot.handlers.static_text import no_new_words


def new_word(update, context):
    """ Entered /new command"""

    u = User.get_user(update, context)
    t = Translation.get_unknown_translation_for_user(u)
    if t is None:
        context.bot.send_message(
            chat_id=u.user_id,
            text=no_new_words,
            reply_markup=telegram.ReplyKeyboardMarkup([
                [telegram.KeyboardButton(text="/repeat"),
                 telegram.KeyboardButton(text="/stop"), ]
            ], resize_keyboard=True),
        )
        return
    context.bot.send_message(
        chat_id=u.user_id,
        text=str(t),
        reply_markup=telegram.ReplyKeyboardMarkup([
            [telegram.KeyboardButton(text="/new"),
             telegram.KeyboardButton(text="/repeat"),
             telegram.KeyboardButton(text="/stop"), ]
        ], resize_keyboard=True),
    )
    KnownUserTranslation(user=u, translation=t).save()


def db_create(update, context):
    u = User.get_user(update, context)
    user_id = extract_user_data_from_update(update)['user_id']

    if not u.is_admin:
        return

    text = update.message.text.replace(f'/create_translation', '').strip()

    words = [w.strip() for w in text.split(':') if w.strip() != ""]
    if len(words) != 2:
        text = static_text.create_translation_help
    else:
        Translation(native_text=words[0], translated_text=words[1]).save()
        text = f"{words[0]} - {words[1]}"

    context.bot.send_message(
        text=text,
        chat_id=user_id,
    )


def db_read(update, context):
    u = User.get_user(update, context)
    user_id = extract_user_data_from_update(update)['user_id']

    if not u.is_admin:
        return

    text = update.message.text.replace(f'/read_translation', '').strip()
    if text == "":
        text = static_text.read_translation_help
    else:
        if text.isdigit():
            tr = Translation.objects.filter(id=int(text)).first()
        else:
            tr = Translation.objects.filter(native_text=text).first()
        if tr is None:
            text = static_text.nothing_found
        else:
            text = f"#{tr.id} : \n" \
                   f"{tr.native_text} - {tr.translated_text}"

    context.bot.send_message(
        text=text,
        chat_id=user_id,
    )


def db_update(update, context):
    u = User.get_user(update, context)
    user_id = extract_user_data_from_update(update)['user_id']

    if not u.is_admin:
        return

    text = update.message.text.replace(f'/update_translation', '').strip()

    words = [w.strip() for w in text.split(':') if w.strip() != ""]
    if len(words) != 3 or not words[0].isdigit():
        text = static_text.update_translation_help
    else:
        tr = Translation.objects.filter(id=int(words[0])).first()
        tr.native_text = words[1]
        tr.translated_text = words[2]
        tr.save()
        text = str(tr)

    context.bot.send_message(
        text=text,
        chat_id=user_id,
    )


def db_delete(update, context):
    u = User.get_user(update, context)
    user_id = extract_user_data_from_update(update)['user_id']

    if not u.is_admin:
        return

    text = update.message.text.replace(f'/delete_translation', '').strip()
    if text == "" or not text.isdigit():
        text = static_text.read_translation_help
    else:
        tr = Translation.objects.filter(id=int(text)).first()
        if tr is None:
            text = static_text.nothing_found
        else:
            tr.delete()
            text = f"DELETED: \n" \
                   f"{tr.native_text} - {tr.translated_text}"

    context.bot.send_message(
        text=text,
        chat_id=user_id,
    )
