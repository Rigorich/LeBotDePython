import telegram

from tgbot.models import User, Translation, KnownUserTranslation

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
