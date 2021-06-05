import telegram
from tgbot.handlers.utils import handler_logging
from tgbot.handlers import static_text

from tgbot.models import User, CurrentUserQuiz


@handler_logging()
def start(update, context):
    update.message.reply_text(text=static_text.start_message)

    from tgbot.models import Translation
    Translation(native_text="льзя", translated_text="можно").save()
    Translation(native_text="аки", translated_text="подобно").save()
    Translation(native_text="мнить", translated_text="думать").save()
    Translation(native_text="абы", translated_text="чтобы").save()
    Translation(native_text="благость", translated_text="доброта").save()
    Translation(native_text="яства", translated_text="еда").save()
    Translation(native_text="нудить", translated_text="принуждать").save()
    Translation(native_text="чело", translated_text="лоб").save()
    Translation(native_text="лобзати", translated_text="целовать").save()


def stop(update, context):
    u = User.get_user(update, context)
    update.message.reply_text(text="OK",
                              reply_markup=telegram.ReplyKeyboardRemove())
    CurrentUserQuiz.objects.filter(user=u).delete()
