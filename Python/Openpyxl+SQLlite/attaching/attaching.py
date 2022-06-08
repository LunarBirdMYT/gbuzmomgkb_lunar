"""
update 20/11/2021:
-- Оптимизация с PEP-8
-- Оптимизирована функция list_1
update 04/03/2022:
-- Переход на копирование данных в SQLite базу
"""

# import time
import datetime
import openpyxl
import os
import sqlite3


# Заготовка для даты сегодня
today = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
# print(today.strftime("%d.%m.%Y"))

# start = time.time()


try:
    # Открываем книгу только для чтения.
    book = openpyxl.open("01. Мониторинг прикрепления..xlsx", read_only=True)
    # Задаем активный лист, по умолчанию текущий.
    sheet = book.active

    # Создаем вложенные списки по всем элементам таблицы xlxs.
    row_book = []
    for row in sheet.iter_rows(values_only=True):
        row_book.append(list(row))

    # print(row_book)

except Exception as e_open_book:
    print(f'Ошибка: \n{e_open_book}')
    print('Файл "01. Мониторинг прикрепления..xlsx" не найден')
    print(input('___Нажмите Enter___'))
finally:
    # Закрываем книгу
    book.close()

print('Обработка начата, ожидайте!')


# Создаем директорию с сегодняшним днём и перемещаем файл туда
def now_add_folder_and_replace_book():
    # текущий день и преобразование к виду ДД.ММ.ГГГГ
    now = datetime.datetime.now()
    now = now.strftime("%d.%m.%Y")

    if not os.path.isdir(now):
        os.mkdir(now)  # Создане директории
    # os.rmdir("27.06.2021")  # Удаление директории

    # Перемещение файла в папку с текущей датой.
    os.replace('01. Мониторинг прикрепления..xlsx',
               f'{now}/01. Мониторинг прикрепления..xlsx')


# Формируем будущие спсики по необходимым критериям через вложенки
def list_1(el1, el2, el3, el4):
    # Соответсвенно 1 - подразделение, 2 - тип участка, 3- врач, 4- кол-во пац.
    list_app = list([el1, el2, el3, el4])
    return list_app


# Отыскиваем Мытищи среди этого всего г...
mytishi_row = []
os_rep = True
for i in row_book:
    try:
        # if i[1] == '01' and i[4] == '[280101] ГБУЗ МО Мытищинская ГКБ':
        #     print(i)
        if i[0] == ' ' and i[4] == '[280101] ГБУЗ МО Мытищинская ГКБ':
            mytishi_row.append(list_1(i[6], i[7], i[10], i[18]))
    except IndexError:
        pass
    except Exception as e:
        print(f'Ошибка: \n{e}')
        os_rep = False
        print(input('***** Ошибка в данных! Пересохраните эксель файл! ******'))
if os_rep:
    now_add_folder_and_replace_book()
# Разбиваем по поликлиникам
# print(mytishi_row[0:2])

list_dgp1 = []
list_dgp2 = []
list_dgp4 = []
list_dgp6 = []
list_gp1 = []
list_gp2 = []
list_gp3 = []
list_gp5 = []
list_gp6 = []
list_gp7 = []
list_gp7_ped = []

for j in mytishi_row:
    if 'Детская поликлиника №1' in j[0]:
        list_dgp1.append(j)
    if 'Детская поликлиника №2' in j[0]:
        list_dgp2.append(j)
    if 'Детская поликлиника №4' in j[0]:
        list_dgp4.append(j)
    if 'Педиатрическое отделение поликлиники №6' in j[0] \
            or ('КВХ' in j[0] and 'Педиатрический' in j[1]) \
            or ('Поведники' in j[0] and 'Педиатрический' in j[1]):
        list_dgp6.append(j)
    if 'Поликлиника №1' in j[0]:
        list_gp1.append(j)
    if 'Поликлиника №2' in j[0]:
        list_gp2.append(j)
    if 'Поликлиника №3' in j[0]:
        list_gp3.append(j)
    if 'Поликлиника №5' in j[0]:
        list_gp5.append(j)
    if 'Поликлиника №6' in j[0] \
            or ('КВХ' in j[0] and 'Терапевтический' in j[1]) \
            or ('Поведники' in j[0] and 'Терапевтический' in j[1]):
        list_gp6.append(j)
    if 'Поликлиника №7' in j[0] and ('Врача общей практики (семейного врача)' in j[1]
                                     or 'Терапевтический (в т.ч. цеховой)' in j[1]):
        list_gp7.append(j)
    if 'Поликлиника №7' in j[0] and 'Педиатрический' in j[1]:
        list_gp7_ped.append(j)


# Фукнция для вычисления суммы населения
def sum_people(pol):
    leng_list = len(pol)
    list_sum = []
    for k in range(leng_list):
        list_sum.append(pol[k][3])

    return list_sum


# Погнали вычислять общее количество населения
people_dgp_1 = sum(sum_people(list_dgp1))
people_dgp_2 = sum(sum_people(list_dgp2))
people_dgp_4 = sum(sum_people(list_dgp4))
people_dgp_6 = sum(sum_people(list_dgp6))
people_gp_1 = sum(sum_people(list_gp1))
people_gp_2 = sum(sum_people(list_gp2))
people_gp_3 = sum(sum_people(list_gp3))
people_gp_5 = sum(sum_people(list_gp5))
people_gp_6 = sum(sum_people(list_gp6))
people_gp_7 = sum(sum_people(list_gp7))
people_dgp_7 = sum(sum_people(list_gp7_ped))
total_sum = people_dgp_1 + people_dgp_2 + people_dgp_4 + people_dgp_6\
    + people_gp_1 + people_gp_2 + people_gp_3 + people_gp_5 +\
    people_gp_6 + people_gp_7 + people_dgp_7

# Список на вывод
list_out = (today, people_dgp_1, people_dgp_2, people_dgp_4, people_dgp_6, people_dgp_7,
            people_gp_1, people_gp_2, people_gp_3, people_gp_5,
            people_gp_6, people_gp_7, total_sum)


# Функция для сохранения в БД
def operation_with_bd(list_out):
    try:
        # Создаем объект базы данных или присоединяемся к созданной
        conn = sqlite3.connect('attaching.db')

        # Создаем курсор для обращения к базе данных
        cur = conn.cursor()

        # Создаем таблицу
        cur.execute("""CREATE TABLE IF NOT EXISTS attachment_monitoring(
            date_report TEXT,
            gdp_1 INTEGER,
            gdp_2 INTEGER,
            gdp_4 INTEGER,
            ped_otd_pol_6 INTEGER,
            ped_otd_pol_7 INTEGER,
            gp_1 INTEGER,
            gp_2 INTEGER,
            gp_3 INTEGER,
            gp_5 INTEGER,
            gp_6 INTEGER,
            gp_7 INTEGER,
            total INTEGER);
            """)

        # Наполняем БД значениями
        cur.execute("INSERT INTO attachment_monitoring VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", list_out)

    finally:
        # Для сохранения данных используем коммит
        conn.commit()
        conn.close()


operation_with_bd(list_out)


# end = time.time()
# print(end - start)
print('Обработка завершена!!!')
print(input('___Нажмите Enter___'))
