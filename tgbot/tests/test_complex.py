import pytest
import json
import re

import telegram

from tgbot.handlers import admin, commands, translation, repeat, dispatcher
from tgbot.models import User

from settings import TELEGRAM_TOKEN, TESTER_ID

bot = telegram.Bot(TELEGRAM_TOKEN)


def anon_object(**kwargs): return type("object", (), kwargs)()

def create_update_and_context(text):
    json_str = '''
        {
            "update_id": 0,
            "message": {
                "message_id": 0,
                "date": 0,
                "chat": {
                    "id": $TESTER_CHAT_ID,
                    "type": "private"
                },
                "text": "$MESSAGE_TEXT",
                "from": {
                    "id": $TESTER_CHAT_ID,
                    "first_name": "Tester",
                    "is_bot": false
                }
            }
        }
        ''' \
        .replace('$TESTER_CHAT_ID', str(TESTER_ID)) \
        .replace('$MESSAGE_TEXT', str(text))
    update = telegram.Update.de_json(json.loads(json_str), bot)
    context = anon_object(bot=bot)
    return update, context


def put_command_into(command, handler):
    msgs = handler(*create_update_and_context(command))
    if msgs is not None:
        if type(msgs) != tuple:
            msgs = (msgs,)
        for m in msgs:
            bot.deleteMessage(chat_id=m.chat.id, message_id=m.message_id)
        return msgs[-1]


def execute_handler(handler):
    return put_command_into("", handler)


def find_translation(native_text):
    msg = put_command_into(f"/read_translation {native_text}", translation.db_read)
    db_id = re.search(r"[0-9]+", msg.text)
    if db_id is None:
        return None
    else:
        return db_id.group()


def test_clear_user():
    u = User.get_user_by_username_or_user_id(TESTER_ID)
    if u is not None:
        u.delete()
    u = User.get_user_by_username_or_user_id(TESTER_ID)


def test_start():
    put_command_into("/start", commands.start)


def test_id_search():
    u = User.get_user_by_username_or_user_id(TESTER_ID)
    bot.send_message(chat_id=u.user_id, text='Testing...')


def test_not_admin():
    u = User.get_user_by_username_or_user_id(TESTER_ID)
    u.is_admin = False
    u.save()


def test_admin_commands_limited():
    put_command_into("/admin", admin.admin)
    put_command_into("/create_translation", translation.db_create)
    put_command_into("/read_translation", translation.db_read)
    put_command_into("/update_translation", translation.db_update)
    put_command_into("/delete_translation", translation.db_delete)
    put_command_into("/broadcast test", admin.broadcast_command_with_message)


def test_admin():
    u = User.get_user_by_username_or_user_id(TESTER_ID)
    u.is_admin = True
    u.save()
    put_command_into("/admin", admin.admin)


def test_crud():
    put_command_into("/create_translation", translation.db_create)
    put_command_into("/read_translation", translation.db_read)
    put_command_into("/update_translation", translation.db_update)
    put_command_into("/delete_translation", translation.db_delete)
    put_command_into(f"/delete_translation {find_translation('A')}", translation.db_read)
    put_command_into("/create_translation A : a", translation.db_create)
    put_command_into(f"/read_translation {find_translation('A')}", translation.db_read)
    put_command_into("/create_translation C:d", translation.db_create)
    put_command_into("/create_translation B : b", translation.db_create)
    put_command_into(f"/update_translation {find_translation('C')} : C : c", translation.db_update)
    b_id = find_translation('B')
    put_command_into(f"/delete_translation {b_id}", translation.db_delete)
    put_command_into(f"/delete_translation {b_id}", translation.db_delete)
    put_command_into(f"/delete_translation -1", translation.db_delete)


def test_broadcast():
    put_command_into("/broadcast", admin.broadcast_command_with_message)
    put_command_into("/broadcast test", admin.broadcast_command_with_message)
    put_command_into("/broadcast *test", admin.broadcast_command_with_message)


@pytest.mark.parametrize('command_handler',
                         [repeat.show_quiz,
                          translation.new_word,
                          translation.new_word,
                          translation.new_word,
                          commands.stop])
def test_new(command_handler):
    execute_handler(command_handler)


def test_repeat():
    execute_handler(repeat.show_quiz)
    execute_handler(repeat.show_quiz)
    put_command_into("test", dispatcher.text_handler)
    msg = execute_handler(repeat.show_quiz)
    answer = msg.text.split(' ')[0].lower()
    put_command_into(answer, dispatcher.text_handler)
    execute_handler(commands.stop)


def test_stats():
    execute_handler(commands.stats)


def test_crud_clear():
    put_command_into(f"/delete_translation {find_translation('A')}", translation.db_delete)
    put_command_into(f"/delete_translation {find_translation('C')}", translation.db_delete)


def test_ending():
    bot.send_message(chat_id=TESTER_ID, text='End of testing')
    test_clear_user()
