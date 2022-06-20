import tkinter as tk
import tkinter.filedialog as fd
import os
import sys
from os import getcwd
import fss_parsing
import threading
import time


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class App(tk.Tk):
    def __init__(self, x32='', x64=''):
        super().__init__()
        self.title("Проверка новой версии ЭРС от ФСС")
        self.geometry("800x500")
        self.resizable(width=False, height=False)
        self.image = tk.PhotoImage(file=resource_path('images/background.png'))
        self.bg_logo = tk.Label(self, image=self.image)
        self.iconbitmap(resource_path("images/icon.ico"))
        self.x32 = x32
        self.x64 = x64
        self.directory = getcwd()
        self.version_after = ''

        self.fss_object = fss_parsing.ParsingFss()
        self.version_from_file = self.fss_object.version_in_file()

        text_now_version = tk.Label(self,
                                    text="Текущая версия: ",
                                    font=("Microsoft Sans Serif", 16))
        now_version = tk.Label(self,
                               text=self.version_from_file,
                               font=("Microsoft Sans Serif", 16))

        check_new_version = tk.Label(self,
                                     text="Проверить наличие новой версии ЭРС от ФСС?",
                                     font=("Microsoft Sans Serif", 16))
        button_check_version = tk.Button(self,
                                         text="Проверить",
                                         font=("Microsoft Sans Serif", 16),
                                         command=self.check_version)
        check_save_directory = tk.Label(self,
                                        text="Папка для сохранения установщика ЭРС(по умолчанию текущая):",
                                        font=("Microsoft Sans Serif", 16))
        self.set_directory_for_save = tk.Button(self,
                                                text="Сохранить в...",
                                                font=("Microsoft Sans Serif", 16),
                                                command=self.choose_directory)
        check_downloading_version = tk.Label(self,
                                             text="Выберите желаемую версию приложения с сайта ФСС:",
                                             font=("Microsoft Sans Serif", 16))

        self.is_x32 = tk.BooleanVar()
        self.is_x32.set(0)
        button_x32 = tk.Checkbutton(self,
                                    text="x32",
                                    font=("Microsoft Sans Serif", 16),
                                    variable=self.is_x32,
                                    onvalue=1, offvalue=0)
        self.is_x64 = tk.BooleanVar()
        self.is_x64.set(1)
        button_x64 = tk.Checkbutton(self,
                                    text="x64",
                                    font=("Microsoft Sans Serif", 16),
                                    variable=self.is_x64,
                                    onvalue=1, offvalue=0)

        button_download = tk.Button(self,
                                    text="Скачать",
                                    font=("Microsoft Sans Serif", 16),
                                    command=self.downloading)

        self.creator_text = tk.Label(self,
                                     text='Разработано ОВCиПИС ГБУЗ МО Мытищиская ГКБ 2022г.',
                                     font=('Arial', 8),
                                     fg='grey')

        # Упаковка элементов
        self.bg_logo.place(x=0, y=0, relwidth=1, relheight=1)
        text_now_version.place(x=10, y=10)
        now_version.place(x=190, y=10)
        check_new_version.place(x=10, y=46)
        button_check_version.place(x=640, y=86)
        check_save_directory.place(x=10, y=136)
        self.set_directory_for_save.place(x=620, y=176)
        check_downloading_version.place(x=10, y=226)
        button_x32.place(x=580, y=224)
        button_x64.place(x=670, y=224)
        button_download.place(x=655, y=264)
        self.creator_text.place(x=5, y=480)

    def check_version(self):
        # answer_after_parsing = (True/False,
        # текст с ответом/ошибкой, ссылка на 32, ссылка на 64, новая версия)
        # Уничтожение рамки ответа ошибок при загрузке
        try:
            self.message_in_downloading.destroy()
        except AttributeError:
            pass

        answer_after_parsing = self.fss_object.check_version_fss(self.version_from_file)
        if answer_after_parsing[0]:
            self.version_after = answer_after_parsing[4]
            self.x32, self.x64 = answer_after_parsing[2], answer_after_parsing[3]

            print_answer_after_parsing = tk.Label(self,
                                                  text=answer_after_parsing[1],
                                                  font=("Microsoft Sans Serif", 16),
                                                  bg="LimeGreen")
            print_answer_after_parsing.place(x=500, y=46)
            # Уничтожение рамки ошибок при загрузке
            try:
                self.print_errors.destroy()
            except AttributeError:
                pass
        else:
            self.print_errors = tk.Text(self, bg="#FFCCCC", width=80, height=7)
            self.print_errors.insert(tk.INSERT, answer_after_parsing[1])
            self.print_errors.place(x=10, y=86)

    def choose_directory(self):
        directory = fd.askdirectory(title="Открыть папку", initialdir=getcwd())
        if directory:
            self.set_directory_for_save["bg"] = "LimeGreen"
            self.set_directory_for_save["text"] = "Выбрана"
            self.directory = directory

    def final_text(self, thr, write_after_download: str):
        while thr.is_alive():
            self.message_in_downloading.insert(tk.INSERT, '.')
            self.message_in_downloading.update()
            time.sleep(2)
        else:
            self.message_in_downloading.insert(tk.INSERT, write_after_download)
            self.message_in_downloading.update()

    def x64_down(self, thr):
        thr.join()
        text = "\nСкачиваю версию для x64"
        self.message_in_downloading.insert(tk.INSERT, text)
        self.message_in_downloading.update()
        # Первый поток скачивает на фоне, второй выводит точки
        x64_thread = threading.Thread(target=self.fss_object.downoading_fss_64,
                                      args=(self.directory, self.x64),
                                      daemon=True)
        # self.fss_object.downoading_fss_64(self.directory, self.x64)
        x64_thread.start()
        text_after = "\nЗагрузка версии х64 успешно завершена!"
        final_text_thread = threading.Thread(target=self.final_text,
                                             args=(x64_thread, text_after))
        final_text_thread.start()

    def downloading(self):
        if self.x32 == '' and self.x64 == '':
            self.message_in_downloading = tk.Text(self,
                                                  bg="#FFCCCC",
                                                  width=110, height=11)
            text = "Вы не проверяли наличие обновлений. Проверьте, затем загружайте."
            self.message_in_downloading.insert(tk.INSERT, text)
            self.message_in_downloading.place(x=10, y=318)
        else:
            self.message_in_downloading = tk.Text(self,
                                                  bg="#CCFFCC",
                                                  width=110, height=11)
            self.message_in_downloading.insert(tk.INSERT,
                                               f"Файлы будут сохранены в директорию {self.directory}\n---")
            self.message_in_downloading.place(x=10, y=318)

            # Перезаписываем версию в файле, раз уже качаем
            self.fss_object.change_version_in_file(self.version_after)
            self.message_in_downloading.update()

            if self.is_x32.get() and self.is_x64.get():
                """
                Реализация механизма условной многопоточности здесь сводится к
                трем потокам:
                    1 - скачивает версию 32
                    2 - ждет, пока звершится скачивание, чтобы вывести готово
                    3 - ждет пока закончится 2-ой потом, чтобы запустить еще 2
                        4 - скачивает версию 64
                        5 - выводит информацию об успехе
                """
                text = "\nСкачиваю версию для x32"
                self.message_in_downloading.insert(tk.INSERT, text)
                self.message_in_downloading.update()
                x32_thread = threading.Thread(target=self.fss_object.downoading_fss_32,
                                              args=(self.directory, self.x32),
                                              daemon=True)
                # self.fss_object.downoading_fss_32(self.directory, self.x32)
                x32_thread.start()
                text_after = "\nЗагрузка версии х32 успешно завершена!"
                final_text_thread_x32 = threading.Thread(target=self.final_text,
                                                     args=(x32_thread, text_after),
                                                     daemon=True)
                final_text_thread_x32.start()
                
                # Создаем еще один поток, в котором создаются свои потоки
                # чтобы отслеживать предыдущие и не перемешиваться
                x64_thread = threading.Thread(target=self.x64_down,
                                              args=(final_text_thread_x32,),
                                              daemon=True)
                x64_thread.start()
            elif self.is_x32.get():
                text = "\nСкачиваю версию для x32"
                self.message_in_downloading.insert(tk.INSERT, text)
                self.message_in_downloading.update()
                x32_thread = threading.Thread(target=self.fss_object.downoading_fss_32,
                                              args=(self.directory, self.x32),
                                              daemon=True)
                # self.fss_object.downoading_fss_32(self.directory, self.x32)
                x32_thread.start()
                text_after = "\nЗагрузка версии х32 успешно завершена!"
                final_text_thread = threading.Thread(target=self.final_text,
                                                     args=(x32_thread, text_after),
                                                     daemon=True)
                final_text_thread.start()
            elif self.is_x64.get():
                text = "\nСкачиваю версию для x64"
                self.message_in_downloading.insert(tk.INSERT, text)
                self.message_in_downloading.update()
                # Первый поток скачивает на фоне, второй выводит точки
                x64_thread = threading.Thread(target=self.fss_object.downoading_fss_64,
                                      args=(self.directory, self.x64),
                                      daemon=True)
                # self.fss_object.downoading_fss_64(self.directory, self.x64)
                x64_thread.start()
                text_after = "\nЗагрузка версии х64 успешно завершена!"
                final_text_thread = threading.Thread(target=self.final_text,
                                                     args=(x64_thread, text_after),
                                                     daemon=True)
                final_text_thread.start()


if __name__ == "__main__":
    app = App()
    app.mainloop()
