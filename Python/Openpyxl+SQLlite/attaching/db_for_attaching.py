import sqlite3
import datetime


def operation_with_bd():
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
        # data = read_and_return_data_from_excel()

        # for element in data:
        #     cur.execute("INSERT INTO attachment_monitoring VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", element)

        # Для вывода данных
        cur.execute("SELECT * FROM attachment_monitoring;")
        rows = cur.fetchall()

        # Удаление строки после выборки определенного критерия
        # cur.execute("DELETE FROM attachment_monitoring WHERE date_report = '04.03.2022' AND total = 297967")

        # Всех строк таблицы
        # for row in rows:
        #     print(row)

        # Вывод доступных дат месяца, при поиске даты, которой нет в БД
        def print_month(date):
            date = datetime.datetime.strptime(date,
                                              "%Y-%m-%d %H:%M:%S").strftime("%m.%Y")
            list_date = []
            for date_bd in rows:
                date_in_for = datetime.datetime.strptime(date_bd[0],
                                                         "%Y-%m-%d %H:%M:%S").strftime("%m.%Y")
                if date == date_in_for:
                    list_date.append(date_bd[0])

            for date in list_date:
                print(date)

        # Последней переданной даты
        def print_input_date(date):
            date_search = datetime.datetime.strptime(date,
                                                     "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y")
            check_print = True  # Проверка была ли печать или даты нет в БД
            for date_bd in rows:
                date_in_for = datetime.datetime.strptime(date_bd[0],
                                                         "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y")
                if date_search == date_in_for:
                    check_print = False
                    print(f'{date_search} \n\
                          ДГП1:   {date_bd[1]}\n\
                          ДГП2:   {date_bd[2]}\n\
                          ДГП4:   {date_bd[3]}\n\
                          Пед.пол.6:   {date_bd[4]}\n\
                          Пед.пол.7:   {date_bd[5]}\n\
                          ГП1:   {date_bd[6]}\n\
                          ГП2:   {date_bd[7]}\n\
                          ГП3:   {date_bd[8]}\n\
                          ГП5:   {date_bd[9]}\n\
                          ГП6:   {date_bd[10]}\n\
                          ГП7:   {date_bd[11]}\n\
                          Всего:   {date_bd[12]}')

            if check_print:
                print('Указанный день в отчете не найден!\nВывожу список дат для указанного месяца:')
                print_month(date)

        # Печать последней даты
        def print_last_date():
            date = datetime.datetime.strptime(rows[-1][0],
                                              "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y")
            print(f'{date} \n\
                  ДГП1:   {rows[-1][1]}\n\
                  ДГП2:   {rows[-1][2]}\n\
                  ДГП4:   {rows[-1][3]}\n\
                  Пед.пол.6:   {rows[-1][4]}\n\
                  Пед.пол.7:   {rows[-1][5]}\n\
                  ГП1:   {rows[-1][6]}\n\
                  ГП2:   {rows[-1][7]}\n\
                  ГП3:   {rows[-1][8]}\n\
                  ГП5:   {rows[-1][9]}\n\
                  ГП6:   {rows[-1][10]}\n\
                  ГП7:   {rows[-1][11]}\n\
                  Всего:   {rows[-1][12]}')

        # Вывод прикрепленного насения по необходимой дате
        # print_input_date('2022-04-01 00:00:00')

        # Вывод прикрепленного насения по последней дате в списке
        print_last_date()

        # Вывод необходимого месяца, если нет точной даты
        # print_month('2022-04-01 00:00:00')

        # # Для вывода имени столбцев
        # cur.execute("SELECT * FROM attachment_monitoring;")
        # names = list(map(lambda x: x[0], cur.description))
        # print(names)

    finally:
        # Для сохранения данных используем коммит
        # conn.commit()
        conn.close()


operation_with_bd()
