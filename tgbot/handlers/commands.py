import telegram
from tgbot.handlers.utils import handler_logging
from tgbot.handlers import static_text

from tgbot.models import User, Translation, KnownUserTranslation, CurrentUserQuiz


@handler_logging()
def start(update, context):
    update.message.reply_text(text=static_text.start_message)


def stop(update, context):
    u = User.get_user(update, context)
    update.message.reply_text(text=static_text.stop_accepted,
                              reply_markup=telegram.ReplyKeyboardRemove())
    CurrentUserQuiz.objects.filter(user=u).delete()


def stats(update, context):
    """ Show stats about known words """

    u = User.get_user(update, context)

    known_translations = KnownUserTranslation.objects.filter(user=u)\
        .select_related('translation').order_by('translation__native_text')
    known_words = "\n".join([str(kn_tr.translation) for kn_tr in known_translations])
    text = f"{static_text.known_words} ({known_translations.count()}): \n{known_words}"

    update.message.reply_text(text=text)
