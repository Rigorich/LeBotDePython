import telegram

from tgbot.models import User, Translation, KnownUserTranslation, CurrentUserQuiz

from tgbot.handlers.static_text import no_repeat_words, quiz_right_answer

from random import shuffle


QUIZ_WRONG_ANSWERS_COUNT = 3

def show_quiz(update, context):
    """ Entered /repeat command"""
    u = User.get_user(update, context)
    t = Translation.get_random_known_translation_for_user(u)
    if t is None:
        context.bot.send_message(
            chat_id=u.user_id,
            text=no_repeat_words,
            reply_markup=telegram.ReplyKeyboardMarkup([
                [telegram.KeyboardButton(text="/new"),
                 telegram.KeyboardButton(text="/stop"), ]
            ], resize_keyboard=True),
        )
        return
    quiz = get_quiz(u, t)
    context.bot.send_message(
        chat_id=u.user_id,
        text=f"{t.native_text} - ?",
        reply_markup=telegram.ReplyKeyboardMarkup(
            keyboard=[
                [telegram.KeyboardButton(text=w) for w in quiz],
                [telegram.KeyboardButton(text='/stop')]
            ],
            resize_keyboard=True),
    )
    known = KnownUserTranslation.objects.get(translation=t)
    CurrentUserQuiz(user=u, known_translation=known).save()


def get_quiz(user, translation):
    answers = [translation.translated_text]
    known_count = KnownUserTranslation.objects.filter(user=user).count()
    all_count = Translation.objects.count()
    unknown_count = all_count - known_count
    known_need = min(QUIZ_WRONG_ANSWERS_COUNT, known_count - 1)
    unknown_need = min(QUIZ_WRONG_ANSWERS_COUNT - known_need, unknown_count)
    for i in range(known_need):
        while True:
            wrong = Translation.get_random_known_translation_for_user(user).translated_text
            if wrong not in answers:
                answers.append(wrong)
                break
    known_translations_ids = KnownUserTranslation.objects.filter(user=user).values_list('translation', flat=True)
    unknown_translations = Translation.objects.exclude(id__in=known_translations_ids)[:unknown_need]
    for t in unknown_translations:
        answers.append(t.translated_text)
    shuffle(answers)
    return answers


def check(update, context):
    u = User.get_user(update, context)
    text = update.message.text

    quiz = CurrentUserQuiz.objects.filter(user=u).first()

    if quiz is None:
        return

    quiz_translation = quiz.known_translation.translation
    quiz.delete()

    if text == quiz_translation.translated_text:
        context.bot.send_message(
            chat_id=u.user_id,
            text=quiz_right_answer
        )
        show_quiz(update, context)
    else:
        context.bot.send_message(
            chat_id=u.user_id,
            text=str(quiz_translation),
            reply_markup=telegram.ReplyKeyboardMarkup([
                [telegram.KeyboardButton(text="/repeat"),
                 telegram.KeyboardButton(text="/stop"), ]
            ], resize_keyboard=True),
        )
