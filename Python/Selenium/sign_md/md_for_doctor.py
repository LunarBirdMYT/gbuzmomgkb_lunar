"""
07/12/2021 update: Исправлена ошибка count_error с вызовом внутри функции
  --- Дополнительные изменения и улучшения
09/12/2021 update: В случае если пропал интернет и нет окна после клика
на медзапись, новая функция check_open_window будет производить счет каждые
3 секунды до 40*3 = 120 секунд и кликнет на МД еще раз
  --- Добавлен ощий лог на выполнение функций
10/12/2021 update: Ошибка для завершенного случая, если пациент ранее был
на диспансерном учете, теперь вместо сохранения - отмена
  --- Добавлено ожидание исчезновения дисплей блока при поиске ФИО
  --- Проверка на отсутсвие пациента
  --- Налаживание циклов и выводов ошибок
12/12/2021 update: исключен лог с функциями, вместо него добавлено сохранение
в файл, если мед.записей 2 и более
17/12/2021 update: Разработана функция подписи множества Мд в одном ТАП
20/12/2021 update: Разработана функция на проверку МД 1.0
"""


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # NOQA
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
import datetime
import openpyxl


login = input('Введите логин для входа:\n').strip()
password = input('Введите пароль:\n').strip()
last_date = input('Введите дату окончания периода(ддммгггг):\n').strip()
number_row = 0


def now():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return now


# Лог ФИО пациентов по врачу
def log_journal_user(any_text):
    log_journal = open(f'{login} log.txt', 'a+')
    text = str(any_text)
    print(f'[{now()}] {text}', file=log_journal)
    log_journal.close()


# Лог отловли двух медзаписей
def log_any_error(any_text):
    log = open(f'log_any_error_for_{login}.txt', 'a+')
    text = str(any_text)
    print(f'[{now()}] {text}', file=log)
    log.close()


# Функция на проверку наличия мед.записи
def no_md(browser, all_windows):
    time.sleep(1)
    browser.implicitly_wait(1)
    try:
        WebDriverWait(browser, 120).until(
                            EC.visibility_of_element_located((By.XPATH,
                                                              "//span[text()")))

        browser.find_element_by_xpath("//div[text()")
        browser.close()
        browser.switch_to.window(all_windows[0])
        click_on_cancel = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable((By.XPATH,
                                                        "//span[text()")))
        click_on_cancel.click()
        return True

    except NoSuchElementException:
        return False


# Функция проверки отправлена или нет
def it_send_in_remd(browser, all_windows):
    browser.implicitly_wait(1)
    try:
        WebDriverWait(browser, 120).until(
                            EC.visibility_of_element_located((By.XPATH,
                                                              "//span[text()")))

        browser.find_element_by_xpath("//span")
        browser.close()
        browser.switch_to.window(all_windows[0])
        click_on_cancel = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable((By.XPATH,
                                                        "//span")))
        click_on_cancel.click()
        return True

    except NoSuchElementException:
        return False


# Проверка подписана ли мед.запись и требуется ли только подписать и отправить
def md_is_signed(browser, all_windows):
    browser.implicitly_wait(1)
    try:
        WebDriverWait(browser, 120).until(
                            EC.visibility_of_element_located((By.XPATH,
                                                              "//span")))

        browser.find_element_by_xpath("//span")
        return True

    except NoSuchElementException:
        return False


# Если где-то всплывёт окно с вариантами выбора да/нет
def if_yes_on_page(browser):
    browser.implicitly_wait(1)
    try:
        browser.find_element_by_xpath("//span")
        click_on_yes = browser.find_element_by_xpath("//span")
        click_on_yes.click()

    except NoSuchElementException:
        pass
    except Exception:
        #  Exception as e print(f'**eeeeeror  \n{e}')
        pass


# Проверка завершен ли случай
def if_compledCase(browser):
    browser.implicitly_wait(1)
    try:
        browser.find_element_by_xpath("//label")
        click_on_compledCase = WebDriverWait(browser, 10).until(
                     EC.element_to_be_clickable((By.XPATH,
                                                 "//span[text()")))
        click_on_compledCase.click()

        click_on_save = WebDriverWait(browser, 10).until(
                     EC.element_to_be_clickable((By.XPATH,
                                                 "//span[text()")))
        click_on_save.click()
        # Для кликов по всем "да"
        if_yes_on_page(browser)
        time.sleep(1)
        if_yes_on_page(browser)
        time.sleep(1)
        if_yes_on_page(browser)
        return True

    except NoSuchElementException:
        click_on_save = WebDriverWait(browser, 10).until(
                     EC.element_to_be_clickable((By.XPATH,
                                                 "//span[text()")))
        click_on_save.click()
        # Для кликов по всем "да"
        if_yes_on_page(browser)
        time.sleep(1)
        if_yes_on_page(browser)
        time.sleep(1)
        if_yes_on_page(browser)
        return False
        pass


def return_fio_from_exel(login, number_row):
    def open_book():
        try:
            book_in = openpyxl.open(f'{login}.xlsx', read_only=True)
            return book_in
        except Exception:
            print(input(f'Файл {login}.xlsx не найден\nСохраните файл в директории со скриптом\nДля продолжения нажмите Enter...'))

    book = open_book()
    sheet = book.active
    return_fio = sheet.cell(row=15+number_row, column=4).value
    book.close()
    if return_fio is not None:
        return return_fio
    else:
        input('++++++++\nПоследняя строка отработана.\nИспользуйте Ctrl+С, для завершения')


def input_fio_put_find(browser, login, number_row):
    try:
        browser.implicitly_wait(2)
        # Находим поле и вводим в него данные
        WebDriverWait(browser, 120).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          "//input")))

        input_str = WebDriverWait(browser, 120).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    "//input")))
        input_str.click()
        input_str.send_keys(f'{return_fio_from_exel(login, number_row)}')
        log_journal_user(f"[INFO] ФИО Пациента: {return_fio_from_exel(login, number_row)}")

        # Нажимаем найти
        WebDriverWait(browser, 120).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          "//input")))
        click_find_in_start = WebDriverWait(browser, 120).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    "//input")))
        click_find_in_start.click()

        input_str = WebDriverWait(browser, 120).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    "//input")))
        input_str.click()
        input_str.clear()
        time.sleep(2)
    except Exception as e:
        log_journal_user('[INFO] Ошибка при попытке ввести ФИО в поле ввода')
        if 'element click intercepted' in e:
            print('Экран закрывает поле ввода')
        time.sleep(3)


# Функция для проверки, что новое окно открылось после клика по МД
def check_open_window(count_time_sleep=0):
    time.sleep(3)
    # print(count_time_sleep)
    return count_time_sleep


def block_invisible(browser):
    browser.implicitly_wait(0)
    WebDriverWait(browser, 120).until(
        EC.invisibility_of_element_located((By.XPATH,
                                            "//div")))


def several_md(browser, all_windows):
    browser.implicitly_wait(0)
    try:
        WebDriverWait(browser, 2).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//data")))
        find_all_md = browser.find_elements_by_xpath("//data")
        if len(find_all_md) < 2:
            return False
        else:
            return True
    except Exception:
        pass


def md_in_2020(browser):
    browser.implicitly_wait(0)
    try:
        WebDriverWait(browser, 0.1).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//dat")))
        WebDriverWait(browser, 0.1).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "//span[@title")))
        return True
    except NoSuchElementException:
        return False
    except Exception:
        # log_journal_user(f'[{now()}] [ATT] Ошибка при проверке МД 1.0 \n{e}')
        return False


def for_action_several_md(browser, all_windows, login, number_row):
    browser.implicitly_wait(0)
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//datl")))
        time.sleep(1)
        find_all_not_send_md = len(browser.find_elements_by_xpath("//data"))
        if find_all_not_send_md == 0:
            pass
        elif find_all_not_send_md == 1:
            one_md = browser.find_element_by_xpath("//dat//span")
            actionChains = ActionChains(browser)
            actionChains.double_click(one_md).perform()

            click_on_allActions = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button")))
            click_on_allActions.click()

            click_on_sendRemd = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button")))
            click_on_sendRemd.click()

            time.sleep(2)

            WebDriverWait(browser, 120).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button")))
        else:
            WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//da")))
            many_md = browser.find_elements_by_xpath("//dataМД']")
            count_md = len(many_md)

            # print(f'Всего не отправлено: {find_all_not_send_md}')
            # try:
            for i in range(find_all_not_send_md):
                # print(f'--эелемент i = {i}')
                if i == 0:
                    actionChains = ActionChains(browser)
                    actionChains.double_click(many_md[i]).perform()

                    click_on_allActions = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    "//button")))
                    click_on_allActions.click()

                    click_on_sendRemd = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    "//button")))
                    click_on_sendRemd.click()

                    time.sleep(2)

                    click_on_cancel = WebDriverWait(browser, 120).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    "//button")))
                    print(f'[{now()}] [INFO] Мед.запись успешно подписана')
                    time.sleep(1)
                    click_on_cancel.click()
                    count_md -= 1  # После подписи общее количество должно быть меньше на одну
                else:
                    WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable((By.XPATH,
                                                        "//data")))
                    many_md_after = browser.find_elements_by_xpath("//datat")
                    # После подписи общее количество должно равняться раннему
                    if len(many_md_after) > count_md:
                        count_after_action_str = len(many_md_after) - count_md
                        # print(f'Сейчас не отправлено {len(many_md_after)} \nюзаем элемент в списке {count_after_action_str}')
                        actionChains = ActionChains(browser)
                        actionChains.double_click(many_md_after[count_after_action_str]).perform()

                    try:
                        click_on_allActions = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable((By.XPATH,
                                                        "//button")))
                        click_on_allActions.click()
                                                        
                        click_on_sendRemd = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable((By.XPATH,
                                                        "//button[text()")))
                        click_on_sendRemd.click()

                    except Exception as e:
                        log_any_error(f"[ATT] Ошибка на  пациентеc несколькими МД: \n{return_fio_from_exel(login, number_row)}\n{e}")
                        if 'element click intercepted' in str(e):
                            time.sleep(8)
                            click_on_allActions = WebDriverWait(browser, 10).until(
                                EC.element_to_be_clickable((By.XPATH,
                                                            "//button")))
                            click_on_allActions.click()
                                                            
                            click_on_sendRemd = WebDriverWait(browser, 10).until(
                                EC.element_to_be_clickable((By.XPATH,
                                                            "//button[text()=")))
                            click_on_sendRemd.click()

                        time.sleep(2)

                        click_on_cancel = WebDriverWait(browser, 120).until(
                            EC.element_to_be_clickable((By.XPATH,
                                                        "//button[text()")))
                        print(f'[{now()}] [INFO] Мед.запись успешно подписана')
                        click_on_cancel.click()
                        time.sleep(1)
                        count_md -= 1
                    else:
                        actionChains = ActionChains(browser)
                        # print('Элементы равны, используем нулевой')
                        actionChains.double_click(many_md_after[0]).perform()

                    try:
                        click_on_allActions = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable((By.XPATH,
                                                        "//button[text()")))
                        click_on_allActions.click()

                        click_on_sendRemd = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable((By.XPATH,
                                                        "//button[text()")))
                        click_on_sendRemd.click()

                    except Exception as e:
                        log_any_error(f"[ATT] Ошибка на  пациентеc несколькими МД: \n{return_fio_from_exel(login, number_row)}\n{e}")
                        if 'element click intercepted' in str(e):
                            time.sleep(8)
                            click_on_allActions = WebDriverWait(browser, 10).until(
                                EC.element_to_be_clickable((By.XPATH,
                                                            "//button[text()")))
                            click_on_allActions.click()

                            click_on_sendRemd = WebDriverWait(browser, 10).until(
                                EC.element_to_be_clickable((By.XPATH,
                                                            "//button[text()")))
                            click_on_sendRemd.click()

                        time.sleep(2)

                        click_on_cancel = WebDriverWait(browser, 120).until(
                            EC.element_to_be_clickable((By.XPATH,
                                                        "//button[text()")))
                        print(f'[{now()}] [INFO] Мед.запись успешно подписана')
                        click_on_cancel.click()
                        time.sleep(1)
                        count_md -= 1

    except Exception as e:
        log_any_error(f"[ATT] Ошибка на  пациентеc несколькими МД: \n{return_fio_from_exel(login, number_row)}\n{e}")


def med_doc_send_REMD(login, password, number_row, last_date):
    try:
        link = 'http://'

        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_extension('./1.2.8_0/1.2.8_0.zip')

        browser = webdriver.Chrome(chrome_options=options)
        browser.get(link)

        # Находим поле ввода и вводим логин
        input_login = browser.find_element_by_id('Login')
        input_login.send_keys(login)

        # Находим поле ввода и вводим пароль
        input_password = browser.find_element_by_id('Password')
        input_password.send_keys(password)

        # Находим кнопку входа и кликаем
        button_in = browser.find_element_by_xpath(
            '//input[@value="Войти"]')
        button_in.click()

        # Задаем ожидание элементов в секундах
        browser.implicitly_wait(15)

        # Кликаем по нопочке закрыть в начале
        button_in = browser.find_element_by_xpath(
            '//div')
        button_in.click()

        # Кликаем сразу же по емиас в любом случае, если зашли в ЛК врача
        button_from_lk = WebDriverWait(browser, 120).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//span[text()")))
        browser.execute_script("return arguments[0].scrollIntoView(true);",
                               button_from_lk)
        button_from_lk.click()

        # Ждем пока появится кнопочка и кликаем
        time.sleep(1)
        WebDriverWait(browser, 120).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "//")))

        button_med_doc = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//")))
        browser.execute_script("return arguments[0].scrollIntoView(true);",
                               button_med_doc)
        button_med_doc.click()

        # time.sleep(3)
        # Указываем "период с" как начальную дату
        date_from = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "//div")))

        date_from = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//input")))

        date_from.click()
        browser.find_element_by_id('Show_TAP_DateFrom').clear()
        date_from.click()
        date_from.send_keys('01.01.2021')

        date_to = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//input")))

        date_to.click()
        browser.find_element_by_id('Show').clear()
        date_to.click()
        date_to.send_keys(last_date)

        # Проверка на случай окна с РЭМД
        count_window = len(browser.window_handles)
        if count_window != 1:
            browser.switch_to.window(browser.window_handles[1])
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
        # input('Тестовая пауза')
        browser.implicitly_wait(15)
        # Если не из личного кабинета
        count_window = len(browser.window_handles)
        if count_window != 1:
            browser.switch_to.window(browser.window_handles[1])
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
        # input('Тестовая пауза')
        browser.implicitly_wait(15)

        count_error = 0

        def func_on_action(browser, login, number_row, count_error):
            cikl_el = True
            while cikl_el:
                try:
                    input_fio_put_find(browser, login, number_row)
                    block_invisible(browser)

                    try:
                        WebDriverWait(browser, 10).until(
                                    EC.visibility_of_element_located((By.XPATH,
                                                                      "//")))
                    except Exception:
                        print('[INFO] Строк с пациентами нет')
                    list_button = browser.find_elements_by_xpath("//")
                    browser.implicitly_wait(15)
                    count_element_page = -1
                    if len(list_button) == 0:
                        number_row += 1
                        continue
                    for element_in_page in list_button:
                        count_element_page += 1
                        time.sleep(1)
                        block_invisible(browser)

                        try:
                            element_in_page.click()
                        except StaleElementReferenceException:
                            list_button_except = browser.find_elements_by_xpath("//")
                            element_in_page_scale = list_button_except[count_element_page]
                            block_invisible(browser)
                            element_in_page_scale.click()
                        except Exception:
                            element_in_page.click()

                        try:
                            click_on_red = WebDriverWait(browser, 120).until(
                                        EC.element_to_be_clickable((By.XPATH,
                                                                    "//")))
                            browser.execute_script("return arguments[0].scrollIntoView(true);",
                                                   click_on_red)
                        except TimeoutException:
                            element_in_page.click()
                            WebDriverWait(browser, 120).until(
                                        EC.visibility_of_element_located((By.XPATH,
                                                                          "//")))
                            click_on_red = WebDriverWait(browser, 120).until(
                                        EC.element_to_be_clickable((By.XPATH,
                                                                    "//")))
                            browser.execute_script("return arguments[0].scrollIntoView(true);",
                                                   click_on_red)

                        try:
                            block_invisible(browser)
                            click_on_red.click()
                        except TimeoutException:
                            click_on_red.click()
                        except Exception as e:
                            log_journal_user(f'[ATT] Какая-то ошибка на click_on_red и не тайм экс \n{e}')

                        # Ждем появления тапа и мед.записи
                        click_on_MD = WebDriverWait(browser, 120).until(
                                    EC.element_to_be_clickable((By.XPATH,
                                                                "//")))
                        click_on_MD.click()

                        # Открывается новая вкладка, поэтому переходим в неё
                        count_window = len(browser.window_handles)
                        count_time_sleep = 0
                        while check_open_window(count_time_sleep) < 15 and count_window == 1:
                            count_time_sleep += 1
                            count_window = len(browser.window_handles)
                            if count_time_sleep == 10:
                                click_on_MD = WebDriverWait(browser, 120).until(
                                    EC.element_to_be_clickable((By.XPATH,
                                                                "//")))
                                click_on_MD.click()
                            if count_time_sleep == 14:
                                browser.quit()
                                med_doc_send_REMD(login, password, number_row, last_date)
                        all_windows = browser.window_handles
                        new_window = all_windows[1]
                        browser.switch_to.window(new_window)

                        def action_with_md(browser, all_windows, count_element_page, number_row):
                            # Функция для проверки кол-ва мед.записей
                            if several_md(browser, all_windows):
                                for_action_several_md(browser, all_windows, login, number_row)
                                browser.close()
                                browser.switch_to.window(all_windows[0])
                                click_on_cancel = WebDriverWait(browser, 10).until(
                                                    EC.element_to_be_clickable((By.XPATH,
                                                                                "//")))
                                click_on_cancel.click()

                            # Функция для проверки МД 1.0
                            elif md_in_2020(browser):
                                log_journal_user(f'[{now()}] [ATT] Обнаружена МД 1.0')
                                browser.close()
                                browser.switch_to.window(all_windows[0])

                                click_on_cancel = WebDriverWait(browser, 10).until(
                                                    EC.element_to_be_clickable((By.XPATH,
                                                                                "//span")))
                                click_on_cancel.click()
                            elif no_md(browser, all_windows):
                                print(f'[{now()}] [INFO] Мед.записи нет')
                            elif it_send_in_remd(browser, all_windows):
                                print(f'[{now()}] [INFO] Запись уже отправлена в РЭМД')
                            elif md_is_signed(browser, all_windows):
                                def click_on_md(browser, all_windows):
                                    try:
                                        click_on_str_MD = WebDriverWait(browser, 10).until(
                                                EC.element_to_be_clickable((By.XPATH,
                                                                            "//")))
                                        actionChains = ActionChains(browser)
                                        actionChains.double_click(click_on_str_MD).perform()

                                        click_on_allActions = WebDriverWait(browser, 10).until(
                                                EC.element_to_be_clickable((By.XPATH,
                                                                            "//button")))
                                        click_on_allActions.click()

                                        click_on_sendRemd = WebDriverWait(browser, 10).until(
                                                EC.element_to_be_clickable((By.XPATH,
                                                                            "//butt")))
                                        click_on_sendRemd.click()

                                        time.sleep(2)

                                        WebDriverWait(browser, 120).until(
                                                EC.element_to_be_clickable((By.XPATH,
                                                                            "//")))
                                        print(f'[{now()}] [INFO] Мед.запись успешно подписана')
                                        time.sleep(1)
                                        browser.close()

                                        browser.switch_to.window(all_windows[0])

                                        click_on_cancel = WebDriverWait(browser, 10).until(
                                                                EC.element_to_be_clickable((By.XPATH,
                                                                                            "//")))
                                        click_on_cancel.click()

                                    except StaleElementReferenceException as e:
                                        print(f'Возникла ошибка скалы) \n{e}')
                                        time.sleep(2)
                                        click_on_md(browser, all_windows)
                                    except TimeoutException as e:
                                        log_journal_user(f'[INFO] Ошибка по ожиданию исчезновения кружка после подписи\n{e}')
                                        browser.refresh()
                                        browser.back()
                                        click_on_md(browser, all_windows)
                                    except Exception as e:
                                        print(f'[{now()}] [ATT] Возникла ошибка в цикле клика по мед.записи \n{e}')
                                        time.sleep(1)
                                        browser.back()
                                        action_with_md(browser, all_windows, number_row)

                                click_on_md(browser, all_windows)
                            else:
                                def sign_md(browser, all_windows, count_element_page):
                                    browser.implicitly_wait(15)
                                    try:
                                        browser.close()
                                        log_journal_user("Окно с мд без подписи закрыто, переключение на all_windows[0]")
                                        browser.switch_to.window(all_windows[0])
                                        was_compledCase = if_compledCase(browser)

                                        new_dom = browser.find_elements_by_xpath("//")
                                        new_element_page = new_dom[count_element_page]
                                        WebDriverWait(browser, 120).until(
                                                    EC.element_to_be_clickable((By.XPATH,
                                                                                "//")))
                                        new_element_page.click()

                                        click_on_red = WebDriverWait(browser, 120).until(
                                                        EC.visibility_of_element_located((By.XPATH,
                                                                                          "//")))
                                        browser.execute_script("return arguments[0].scrollIntoView(true);",
                                                               click_on_red)
                                        click_on_red.click()

                                        # Ждем появления тапа и мед.записи
                                        click_on_MD = WebDriverWait(browser, 120).until(
                                                        EC.element_to_be_clickable((By.XPATH,
                                                                                    "//")))
                                        click_on_MD.click()

                                        # Открывается новая вкладка, поэтому переходим в неё
                                        count_window = len(browser.window_handles)
                                        count_time_sleep = 0
                                        while check_open_window(count_time_sleep) < 15 and count_window == 1:
                                            count_time_sleep += 1
                                            count_window = len(browser.window_handles)
                                            if count_time_sleep == 10:
                                                click_on_MD = WebDriverWait(browser, 120).until(
                                                    EC.element_to_be_clickable((By.XPATH,
                                                                                "//")))
                                                click_on_MD.click()
                                            if count_time_sleep == 14:
                                                browser.quit()
                                                med_doc_send_REMD(login, password, number_row, last_date)
                                        all_windows_def = browser.window_handles
                                        new_window = all_windows_def[1]
                                        last_window = all_windows_def[0]
                                        browser.switch_to.window(new_window)

                                        click_on_str_MD = WebDriverWait(browser, 10).until(
                                                    EC.element_to_be_clickable((By.XPATH,
                                                                                "//")))
                                        actionChains = ActionChains(browser)  # NOQA
                                        actionChains.double_click(click_on_str_MD).perform()

                                        click_on_medical_scr = WebDriverWait(browser, 120).until(
                                                        EC.element_to_be_clickable((By.XPATH,
                                                                                    "//button[text()")))
                                        click_on_medical_scr.click()
                                        time.sleep(7)
                                        click_on_medical_see = WebDriverWait(browser, 120).until(
                                                        EC.element_to_be_clickable((By.XPATH,
                                                                                    "//button")))
                                        click_on_medical_see.click()

                                        time.sleep(3)

                                        click_on_medical_see = WebDriverWait(browser, 120).until(
                                                        EC.element_to_be_clickable((By.XPATH,
                                                                                    "//button[text(")))
                                        click_on_medical_see.click()

                                        if md_is_signed(browser, all_windows):
                                            click_on_str_MD = WebDriverWait(browser, 10).until(
                                                        EC.element_to_be_clickable((By.XPATH,
                                                                                    "//dat")))

                                            actionChains = ActionChains(browser)  # NOQA
                                            actionChains.double_click(click_on_str_MD).perform()

                                            click_on_all_actions = WebDriverWait(browser, 10).until(
                                                        EC.element_to_be_clickable((By.XPATH,
                                                                                    "//button[")))
                                            click_on_all_actions.click()

                                            click_on_send_remd = WebDriverWait(browser, 10).until(
                                                        EC.element_to_be_clickable((By.XPATH,
                                                                                    "//button[te")))
                                            click_on_send_remd.click()

                                            time.sleep(2)

                                            WebDriverWait(browser, 120).until(
                                                        EC.element_to_be_clickable((By.XPATH,
                                                                                    "//button[")))
                                        print(f'[{now()}] [INFO] Мед.запись успешно подписана при отсутствии подписи ранее')
                                        log_journal_user('[INFO] Мед.запись успешно подписана при отсутствии подписи ранее')
                                        time.sleep(1)
                                        browser.close()
                                        log_journal_user('Окно с мд после подписи закрыто, переключение на last_window')

                                        browser.switch_to.window(last_window)

                                        if was_compledCase:
                                            click_on_compled_case = WebDriverWait(browser, 10).until(
                                                        EC.element_to_be_clickable((By.XPATH,
                                                                                    "//span")))
                                            click_on_compled_case.click()

                                            click_on_save = WebDriverWait(browser, 10).until(
                                                        EC.element_to_be_clickable((By.XPATH,
                                                                                    "//spa")))
                                            click_on_save.click()

                                            def patient_on_du_early(browser):
                                                try:
                                                    browser.find_element_by_xpath("//div[te]")
                                                    on_du = browser.find_element_by_xpath("//span[text(")
                                                    on_du.click()

                                                    click_on_cancel = WebDriverWait(browser, 10).until(
                                                        EC.element_to_be_clickable((By.XPATH,
                                                                                    "//span[text")))
                                                    click_on_cancel.click()

                                                except NoSuchElementException:
                                                    pass

                                            patient_on_du_early(browser)

                                            # Для кликов по всем "да"
                                            if_yes_on_page(browser)
                                            time.sleep(1)
                                            if_yes_on_page(browser)
                                            time.sleep(1)
                                            if_yes_on_page(browser)
                                        else:
                                            click_on_cancel = WebDriverWait(browser, 10).until(
                                                 EC.element_to_be_clickable((By.XPATH,
                                                                             "//span")))
                                            click_on_cancel.click()

                                    except Exception as e:
                                        print(f'Ошибка при попытке подписать МД\n{e}')
                                        log_journal_user('Ошибка при попытке подписать МД\n{e}\nпереключение на all_windows[0]')
                                        browser.close()
                                        browser.switch_to.window(last_window)
                                        click_on_cancel = WebDriverWait(browser, 10).until(
                                                            EC.element_to_be_clickable((By.XPATH,
                                                                                        "//span")))
                                        click_on_cancel.click()

                                sign_md(browser, all_windows, count_element_page)
                        action_with_md(browser, all_windows, count_element_page, number_row)
                    number_row += 1

                except Exception as e:
                    print('__test_eRRor')
                    print(f'[{now()}] [ATT] Возникла ошибка \n{e}')
                    count_error += 1

                    if count_error < 11:
                        if 'I/O operation on closed file' in str(e):
                            print('После if I/O operation on closed')
                            time.sleep(5)
                            return_fio_from_exel(login, number_row)
                            func_on_action(browser, login, number_row, count_error)
                            continue
                        else:
                            print('После елса в цикле каунта меньше 11')
                            browser.quit()
                            time.sleep(5)
                            med_doc_send_REMD(login, password, number_row, last_date)
                            continue
                    else:
                        print('Больше соунта 11')
                        browser.quit()
                        time.sleep(5)
                        med_doc_send_REMD(login, password, number_row, last_date)
                        continue
                    continue

        func_on_action(browser, login, number_row, count_error)

    except Exception as e:
        print('***Some eRRor')
        print(f'{e}')

    finally:
        print('Закрываем браузер')
        time.sleep(1)
        browser.quit()


med_doc_send_REMD(login, password, number_row, last_date)
