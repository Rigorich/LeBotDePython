start_message = 'Я ещё в бета-версии. \n' \
                'Но можете попробовать меня использовать: \n' \
                '/new — для изучения новых слов \n' \
                '/repeat — для повторения старых \n' \
                '/stats — для просмотра статистики \n' \
                '------ \n' \
                '/admin — команды администратора'

stop_accepted = "Ладушки!"

unknown_command = "Неизвестная команда"
no_access = "Нет доступа."
nothing_found = "Ничего не найдено"
empty_message = "Пустое сообщение"

confirm_broadcast = "Отправить✅"
decline_broadcast = "Отмена❌"
message_is_sent = "Сообщение доставлено✅\n\n"
declined_message_broadcasting = "Рассылка отменена❌\n\n"

error_with_markdown = "Can't parse your text in Markdown style."
specify_word_with_error = " You have mistake with the word "

no_new_words = "Вы просмотрели все слова!"
no_repeat_words = "Нет слов для повторения!"
known_words = "Изученные слова"

quiz_right_answer = "Верно!"

secret_admin_commands = "⚠️ Admin commands  ⚠\n" \
                        "\nДля изменения словаря:\n" \
                        "/create_translation\n" \
                        "/read_translation\n" \
                        "/update_translation\n" \
                        "/delete_translation\n" \
                        "\nРассылка:\n" \
                        "/broadcast\n"

broadcast_help = "Для рассылки сообщения всем пользователям:\n" \
                 "/broadcast \nСообщение для рассылки"

create_translation_help = "Для добавления новых переводов в словарь:\n" \
                          "/create_translation исходное_слово : переведённое_слово\n" \
                          "Обязательно использовать единственное двоеточие"
read_translation_help = "Для поиска перевода в словаре:\n" \
                        "/read_translation исходное_слово\n" \
                        "или\n" \
                        "/read_translation id_слова"
update_translation_help = "Для исправления перевода в словаре:\n" \
                          "/update_translation id_слова : исходное_слово : переведённое_слово\n" \
                          "Обязательно использовать два двоеточия"
delete_translation_help = "Для удаления перевода из словаря:\n" \
                          "/delete_translation id_слова"
