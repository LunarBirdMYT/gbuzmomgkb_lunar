# Подключаем модуль для Телеграма
import time
import config
import telebot
from telebot import types


# def token():
#     token = ''
#     with open('tok.txt') as f:
#         token = f.read().strip()
#     return token

# # Указываем токен
# bot = telebot.TeleBot(token())

# Токен мгкб бота
bot = telebot.TeleBot(config.TOKEN)


# Если пользователя нет в спсике, то бот не активен
@bot.message_handler(func=lambda message: message.from_user.id not in config.USERS,
                     content_types=['document', 'text', 'photo'])
def if_not_partner(message):
    # Добавляем обращенца в файл с пользователями
    new_user_id = message.from_user.id
    name = message.from_user.first_name
    surname = message.from_user.last_name
    username = message.from_user.username
    user_in_bd = f'{new_user_id}-R-_{name}-R-_{surname}-R-_{username}'
    with open('users_bot_mgkb.txt', 'r', encoding='utf-8-sig') as users_db:
        list_users = [stri.strip() for stri in users_db.readlines()]
        if user_in_bd not in list_users:
            with open('users_bot_mgkb.txt', 'a+', encoding='utf-8-sig') as users_db:
                print(user_in_bd, file=users_db)
                bot.send_message(config.USERS[0], f'У нас тут новый изверь\n{user_in_bd}')
    del new_user_id, name, surname, username, user_in_bd

    # Если пользователь не сотрудник, то уведомляем его
    bot.send_message(message.chat.id,
                     'Вы не являетесь сотрудником МГКБ. Доступ ограничен! Свяжитесь с руководителем ОВСиПИС для получения доступа.')


# Начальная команда
@bot.message_handler(func=lambda message: message.text == 'Главное меню')
@bot.message_handler(commands=['start'])
def start(message):
    kb_1 = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)
    button = types.KeyboardButton
    kb_1.add(button(text='Linux🐧'),
             button(text='Windows🪟'),
             button(text='Веб ресурсы'))
    bot.send_message(message.chat.id,
                     'С чем работаем?',
                     reply_markup=kb_1)


# По части линукси
@bot.message_handler(func=lambda message: message.text == 'Linux🐧')
def linux(message):
    kb_linux = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)
    button = types.KeyboardButton
    kb_linux.add(button(text='Ассистент🐧'),
                 button(text='VipNet🐧'),
                 button(text='Принтер HP 🐧'))
    bot.send_message(message.chat.id,
                     'Выберите желаемый продукт...',
                     reply_markup=kb_linux)


@bot.message_handler(func=lambda message: message.text == 'К выбору пакета ассистента')
@bot.message_handler(func=lambda message: message.text == 'Ассистент🐧')
def assistant_for_linux(message):
    kb_type_assistant = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                  one_time_keyboard=True)
    button = types.KeyboardButton
    kb_type_assistant.add(button(text='deb 🐧'),
                          button(text='rpm 🐧'))
    bot.send_message(message.chat.id,
                     'Какой пакет прислать?',
                     reply_markup=kb_type_assistant)


@bot.message_handler(func=lambda message: message.text == 'deb 🐧')
def assistant_deb(message):
    kb_type_assistant_deb = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                      one_time_keyboard=True)
    button = types.KeyboardButton
    kb_type_assistant_deb.add(button(text='К выбору пакета ассистента'),
                              button(text='Главное меню'))
    bot.send_document(message.chat.id, '-J-1AjBA',
                      reply_markup=kb_type_assistant_deb)
    bot.send_message(message.chat.id,
                     'sudo apt-get install /путь до ассистента///')


@bot.message_handler(func=lambda message: message.text == 'rpm 🐧')
def assistant_rpm(message):
    kb_type_assistant_rpm = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                      one_time_keyboard=True)
    button = types.KeyboardButton
    kb_type_assistant_rpm.add(button(text='К выбору пакета ассистента'),
                              button(text='Главное меню'))
    bot.send_document(message.chat.id, '',
                      reply_markup=kb_type_assistant_rpm)
    bot.send_message(message.chat.id,
                     'sudo apt-get install /путь до ассистента///')


@bot.message_handler(func=lambda message: message.text == 'Меню VipNet🐧')
@bot.message_handler(func=lambda message: message.text == 'VipNet🐧')
def menu_vipnet(message):
    kb_menu_vipnet = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=True,
                                               row_width=2)
    button = types.KeyboardButton
    kb_menu_vipnet.add(button(text='Установка VipNet🐧'),
                       button(text='Удаление VipNet🐧'),
                       button(text='Проблемы с VipNet🐧'),
                       button(text='Главное меню'))
    bot.send_message(message.chat.id,
                     'Какой вариант Вам подойдёт сегодня?',
                     reply_markup=kb_menu_vipnet)


@bot.message_handler(func=lambda message: message.text == 'Установка VipNet🐧')
def install_vipnet(message):
    kb_vipnet_install = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                  one_time_keyboard=True)
    button = types.KeyboardButton
    kb_vipnet_install.add(button(text='Меню VipNet🐧'),
                          button(text='Главное меню'))
    bot.send_message(message.chat.id,
                     """
Вы можете запустить приложенный файл на рабочем месте и установить Vipnet,
а можете следовать инструкции по самостоятельной установке:
sudo apt-get update
cd /opt
sudo sh /opt/

Затем обновляем випнет:
cd /opt/
sudo sh /opt/

Поздравляю, Вы со всем, возможно, успешно справились!
                     """)
    bot.send_document(message.chat.id,
                      '',
                      reply_markup=kb_vipnet_install)


@bot.message_handler(func=lambda message: message.text == 'Удаление VipNet🐧')
def delete_vipnet(message):
    kb_delete_vipnet = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                 one_time_keyboard=True)
    button = types.KeyboardButton
    kb_delete_vipnet.add(button(text='Меню VipNet🐧'),
                         button(text='Главное меню'))
    bot.send_message(message.chat.id,
                     """
Вы можете запустить приложенный файл на рабочем месте и удалить Vipnet,
а можете следовать инструкции по самостоятельному удалению:
Копируем лицензию на всякий случай в домашний каталог
cp /opt/

sudo apt-get remove 'itcs-*'

Следует убедиться, что все файлы были удалены(если ноль, то файлов нет):
ls -l /opt/itcs/ | grep ".prg\|.CRG" | wc -l

Если все файлы удалены, то перезагружаемся, если нет, то Вам нужна помощь.
                     """)
    bot.send_document(message.chat.id,
                      '-',
                      reply_markup=kb_delete_vipnet)


@bot.message_handler(func=lambda message: message.text == 'Меню проблем с Vipnet🐧')
@bot.message_handler(func=lambda message: message.text == 'Проблемы с VipNet🐧')
def vipnet_gudes(message):
    kb_troubles_vipnet = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                   one_time_keyboard=True)
    button = types.KeyboardButton
    kb_troubles_vipnet.add(button(text='sign Error🐧'),
                           button(text='Пароль к контейнеру🐧'),
                           button(text='Главное меню'))
    bot.send_message(message.chat.id, 'Укажите проблему...',
                     reply_markup=kb_troubles_vipnet)


# Функция для возвращения к ошибкам с випнет
def vipnet_gudes_return(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True)
    button = types.KeyboardButton
    kb.add(button(text='Меню проблем с Vipnet🐧'),
           button(text='Главное меню'))
    return kb


# Проблемы при работе с випнет
@bot.message_handler(func=lambda message: message.text == 'sign Error🐧')
def sign_error(message):
    kb_for_troubles = vipnet_gudes_return(message)
    bot.send_message(message.chat.id,
                     """
Рекомендации от Алексея Долгих:
По ошибке sign error:
Переустановить vipnet pki, но лучше:
Обязательно проверьте, что лицензия для ViPNet CSP установлена командой:
/opt/itcs/
В выводе должен присутствовать статус State: Valid
Если нет valid:
/opt/itcs//
Перезагрузиться
                     """)
    bot.send_document(message.chat.id,
                      '',
                      reply_markup=kb_for_troubles)


@bot.message_handler(func=lambda message: message.text == 'Пароль к контейнеру🐧')
def password_on_vipnet(message):
    kb_for_troubles = vipnet_gudes_return(message)
    bot.send_photo(message.chat.id,
                   '')
    bot.send_message(message.chat.id,
                     """
Из-за того что контейнер имеет в названии пробел, скобки и кириллицу на
линукс не может переместиться закрытая часть контейнера.
                     """)
    time.sleep(1)

    bot.send_photo(message.chat.id,
                   '-')
    bot.send_message(message.chat.id,
                     """
На АРМ под windows запустить ViPNet CSP выбрать контейнер для копирования
и нажать на "Копировать в" После откроется окно "инициализация контейнера
ключей". В поле Имя контейнера можно сменить имя.
Скобки и знаки препинания не использовать

                     """)
    bot.send_photo(message.chat.id,
                   '-',
                   reply_markup=kb_for_troubles)


@bot.message_handler(func=lambda message: message.text == 'Принтер HP 🐧')
def install_hp(message):
    kb_install_hp = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                              one_time_keyboard=True)
    button = types.KeyboardButton
    kb_install_hp.add(button(text='Главное меню'))
    bot.send_message(message.chat.id,
                     """
Вы можете запустить приложенный файл на рабочем месте и установить принтер HP,
а можете следовать инструкции по самостоятельной установке:
Обновляем apt-кеш и устанавливаем пакеты:

sudo ap
sudo apPDs
Запускаем установку принтера:

sudo hp-setup –i
Далее отвечаем на вопросы при установке.
                     """)
    bot.send_document(message.chat.id,
                      '',
                      reply_markup=kb_install_hp)


# По части винды
@bot.message_handler(func=lambda message: message.text == 'Меню Windows🪟')
@bot.message_handler(func=lambda message: message.text == 'Windows🪟')
def windows_menu(message):
    kb_windows = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           one_time_keyboard=True)
    button = types.KeyboardButton
    kb_windows.row(button('Касперский🪟'),
                   button('Ассистент🪟'))
    kb_windows.row(button('Сертификаты ЕГИСЗ и ЕПГУ🪟'),
                   button('КриптоПро 4.99🪟'))
    kb_windows.row(button('Проверка версии ЭРС от ФСС🪟'),
                   button('Главное меню'))
    bot.send_message(message.chat.id,
                     'Выберите желаемый продукт...',
                     reply_markup=kb_windows)


@bot.message_handler(func=lambda message: message.text == 'Касперский🪟')
def install_kasp(message):
    kb_kasp = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                        one_time_keyboard=True)
    button = types.KeyboardButton
    kb_kasp.add(button('Меню Windows🪟'),
                button('Главное меню'))
    bot.send_document(message.chat.id,
                      '-ZEp-',
                      reply_markup=kb_kasp)


@bot.message_handler(func=lambda message: message.text == 'Ассистент🪟')
def install_ass(message):
    kb_kasp = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                        one_time_keyboard=True)
    button = types.KeyboardButton
    kb_kasp.add(button('Меню Windows🪟'),
                button('Главное меню'))
    bot.send_document(message.chat.id,
                      '',
                      reply_markup=kb_kasp)


@bot.message_handler(func=lambda message: message.text == 'Сертификаты ЕГИСЗ и ЕПГУ🪟')
def sert_egisz_and_epgu_for_windows(message):
    kb_sert = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                        one_time_keyboard=True)
    button = types.KeyboardButton
    kb_sert.add(button('Windows🪟'),
                button('Главное меню'))
    bot.send_message(message.chat.id,
                     'На всякий случай выкладываю сертификаты, которые нужно установить на АРМ с виндой, чтобы всё работало корректно. Оба корневых нужно установить в хранилище "Доверенные корневце центры сертификации", егисз и госуслуги можно устанавливать в хранилище по-умолчанию')
    time.sleep(1)
    bot.send_document(message.chat.id,
                      '-E_olMKgJAQ')
    time.sleep(0.5)
    bot.send_document(message.chat.id,
                      '')
    time.sleep(0.5)
    bot.send_document(message.chat.id,
                      '')
    time.sleep(0.5)
    bot.send_document(message.chat.id,
                      '',
                      reply_markup=kb_sert)


@bot.message_handler(func=lambda message: message.text == 'КриптоПро 4.99🪟')
def install_crypto_pro(message):
    kb_crypto_pro = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                              one_time_keyboard=True)
    button = types.KeyboardButton
    kb_crypto_pro.add(button('Меню Windows🪟'),
                      button('Главное меню'))
    bot.send_document(message.chat.id,
                      '')
    time.sleep(0.5)
    bot.send_document(message.chat.id,
                      '',
                      reply_markup=kb_crypto_pro)


@bot.message_handler(func=lambda message: message.text == 'Проверка версии ЭРС от ФСС🪟')
def install_check_fss(message):
    kb_check_fss = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                              one_time_keyboard=True)
    button = types.KeyboardButton
    kb_check_fss.add(button('Меню Windows🪟'),
                      button('Главное меню'))
    bot.send_document(message.chat.id,
                      '-')
    time.sleep(0.5)
    bot.send_message(message.chat.id,
                     '''
Прога написана на Python3. По сути это самораспаковывающийся архив, поэтому
Винда будет воспринимать его как вирус -> нужно разрешить исполнение.
В директории запуска появляется файл с датой версии, по умолчанию 06.04.2022(fss.version).
По кнопке "Проверить" обращается к сайту ФСС и проверяет дату последней версии на сайте,
после скачивания новой версии перезаписывая информацию о дате старой версии.
''',
                     reply_markup=kb_check_fss)


@bot.message_handler(func=lambda message: message.text == 'Веб ресурсы')
def web_resources(message):
    kb_web_res = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           one_time_keyboard=True)
    button = types.KeyboardButton
    kb_web_res.add(button('Главное меню'),
                   button('Плагин для работы с ЕПГУ'),
                   button('Ссылки на веб ресурсы'))
    bot.send_message(message.chat.id,
                     'Что Вас интересует?',
                     reply_markup=kb_web_res)


@bot.message_handler(func=lambda message: message.text == 'Плагин для работы с ЕПГУ')
def plagin_for_epgu(message):
    kb_plagin_epgu = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=True)
    button = types.KeyboardButton
    kb_plagin_epgu.add(button('Главное меню'),
                       button('Веб ресурсы'))
    bot.send_message(message.chat.id,
                     'Вы можете скачать необходимый плагин по ссылке: https://',
                     reply_markup=kb_plagin_epgu)


@bot.message_handler(func=lambda message: message.text == 'Ссылки на веб ресурсы')
def link_on_webpage(message):
    kb_on_webpage = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=True)
    button = types.KeyboardButton
    kb_on_webpage.add(button('Главное меню'))
    bot.send_message(message.chat.id,
                     """
ГАСУ: https://

ЕМИАС Поликлиника: http://
ЕМИАС Поликлиника, шаблоны: https://
ЕМИАС Стационар: http://

ЕЦУР: https://

ЕРИС ЛЛО 2022: http://


                     """,
                     reply_markup=kb_on_webpage)


@bot.message_handler(commands=['help'])
def help_func(message):
    bot.send_message(message.chat.id,
                     """
Приветствую, коллега(если нет, то за Вами уже выехали 😈).

Данный бот призван облегчить работу сотрудникам ИТ Мытищинской ГКБ.
Запустите его при помощи команды /start.
Останавливать бота не нужно, рассылка какой-либо информации не планируется.
""")


# Добавляем в черный список пользователя
@bot.message_handler(func=lambda message: message.from_user.id == config.USERS[0]
                     and 'Добавь' in message.text)
def add_black_list(message):
    add_user_list = int(message.text.split()[1])
    config.USERS.append(add_user_list)

    bot.send_message(message.chat.id,
                     f'Человек с id {add_user_list} добавлен в USERS')


@bot.message_handler(func=lambda message: message.from_user.id == config.USERS[0],
                     content_types=['document', 'text', 'photo'])
def send_admin(message):
    bot.send_message(message.chat.id, message)


while True:
    try:
        print('Бот пашет за копейки...')
        bot.polling(none_stop=True)
        print('Бот уволился')
    except Exception as e:
        if "HTTPSConnectionPool" in str(e):
            time.sleep(30)
        with open('logs_error.txt', 'a+') as logs:
            print(f'Error:\n{str(e)}', file=logs)
        time.sleep(5)
