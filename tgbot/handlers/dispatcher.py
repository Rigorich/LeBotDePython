"""
    Telegram event handlers
"""

import telegram
from telegram import Update
from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
)

from dtb.settings import TELEGRAM_TOKEN

from tgbot.handlers import admin, commands, translation, repeat, static_text
from tgbot.handlers.admin import broadcast_command_with_message, broadcast_decision_handler
from tgbot.handlers.manage_data import CONFIRM_DECLINE_BROADCAST
from tgbot.models import User, CurrentUserQuiz


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """

    dp.add_handler(CommandHandler("start", commands.start))

    dp.add_handler(CommandHandler("stop", commands.stop))

    dp.add_handler(CommandHandler("stats", commands.stats))

    dp.add_handler(CommandHandler("new", translation.new_word))

    dp.add_handler(CommandHandler("repeat", repeat.show_quiz))

    # Admin help command
    dp.add_handler(CommandHandler("admin", admin.admin))

    # CRUD translation commands
    dp.add_handler(MessageHandler(Filters.regex(rf'^/create_translation.*'), translation.db_create))
    dp.add_handler(MessageHandler(Filters.regex(rf'^/read_translation.*'), translation.db_read))
    dp.add_handler(MessageHandler(Filters.regex(rf'^/update_translation.*'), translation.db_update))
    dp.add_handler(MessageHandler(Filters.regex(rf'^/delete_translation.*'), translation.db_delete))

    # broadcast command
    dp.add_handler(MessageHandler(Filters.regex(rf'^/broadcast.*'), broadcast_command_with_message))
    dp.add_handler(CallbackQueryHandler(broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}"))

    # just text
    dp.add_handler(MessageHandler(Filters.text, text_handler))

    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(
    #     Filters.document, <function_handler>,
    # ))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(
    #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,
    # ))

    return dp


def text_handler(update: Update, context):
    u = User.get_user(update, context)
    text = update.message.text

    quiz = CurrentUserQuiz.objects.filter(user=u).first()

    if quiz is not None:
        return repeat.check(update, context)
    if text.startswith("/"):
        return update.message.bot.send_message(chat_id=u.user_id, text=static_text.unknown_command)


def run_pooling():   # pragma: no cover
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = telegram.Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")
    updater.start_polling()
    updater.idle()


def stop_pooling():   # pragma: no cover
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    updater.stop()


# Global variable - best way I found to init Telegram bot
bot = telegram.Bot(TELEGRAM_TOKEN)
dispatcher = setup_dispatcher(Dispatcher(bot, None, workers=0, use_context=True))
TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
