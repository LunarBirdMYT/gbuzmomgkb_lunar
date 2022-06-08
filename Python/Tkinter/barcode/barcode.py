import tkinter as tk
import tkinter.messagebox
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class BarcodeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        # Главное окно.
        self.title('Обработка штрих-кода')
        self.geometry('1000x360')
        self.resizable(width=False, height=False)
        self.iconbitmap(resource_path("images/icon.ico"))

        # Создатьрамки, чтобы сгруппировать элементы интерфейса.
        frame_0_0 = tk.Label(self,
                             text="Считать штрих-код",
                             font=("Microsoft Sans Serif", 16))
        frame_0_0.grid(row=0, column=0, sticky= tk.E, padx=10, pady=15)

        self.frame_0_1 = tk.Entry(self, width=40,
                                  font=("Microsoft Sans Serif", 16))
        self.frame_0_1.grid(row=0, column=1)
        self.bind_all("<Key>", self._onKeyRelease, "+")

        frame_0_2 = tk.Button(self,
                              text="Очистить",
                              font=("Microsoft Sans Serif", 16),
                              command=self.clear_barcode_entry)
        frame_0_2.grid(row=0, column=2, padx=15, pady=15)

        frame_1_1 = tk.Label(self,
                             text="Введите количество символов ISN(серийный номер):",
                             font=("Microsoft Sans Serif", 16))
        frame_1_1.grid(row=1, column=1, sticky=tk.E)

        symbols_on_spin = tk.DoubleVar(value=13)
        self.frame_1_2 = tk.Spinbox(width=7,
                               from_=0,
                               to_=100,
                               textvariable=symbols_on_spin,
                               font=("Microsoft Sans Serif", 16))
        self.frame_1_2.grid(row=1, column=2, pady=15)

        frame_2_2 = tk.Button(self,
                              text="Распознать",
                              bg='OliveDrab1',
                              font=("Microsoft Sans Serif", 16),
                              command=self.convert)
        frame_2_2.grid(row=2, column=2, pady=15)

        frame_3_0 = tk.Label(self,
                             text="GTIN:",
                             font=("Microsoft Sans Serif", 16))
        frame_3_0.grid(row=3, column=0, pady=15, sticky=tk.E)
        # Вывод GTIN
        self.frame_3_1 = tk.Label(self,
                             text="",
                             font=("Microsoft Sans Serif", 16))
        self.frame_3_1.grid(row=3, column=1, pady=15, sticky=tk.W)
        frame_3_2 = tk.Button(self,
                              text='Скопировать GTIN',
                              bg='orange',
                              command=self.copy_gtin,
                              font=("Microsoft Sans Serif", 16))
        frame_3_2.grid(row=3, column=2, pady=15)

        frame_4_0 = tk.Label(self,
                             text="Серийный номер(ISN):",
                             font=("Microsoft Sans Serif", 15))
        frame_4_0.grid(row=4, column=0, pady=15, padx=5, sticky=tk.E)
        # Вывод ISN
        self.frame_4_1 = tk.Label(self,
                             text="",
                             font=("Microsoft Sans Serif", 16))
        self.frame_4_1.grid(row=4, column=1, pady=15, sticky=tk.W)
        frame_4_2 = tk.Button(self,
                              text='Скопировать ISN',
                              bg='orange',
                              command=self.copy_isn,
                              font=("Microsoft Sans Serif", 16))
        frame_4_2.grid(row=4, column=2, pady=15)


    def clear_barcode_entry(self):
        self.frame_0_1.delete(0, 'end')
        self.frame_0_1.update()

    def _onKeyRelease(self, event):
        ctrl  = (event.state & 0x4) != 0
        if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
            event.widget.event_generate("<<Cut>>")
        if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
            event.widget.event_generate("<<Paste>>")
        if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")

    def convert(self):
        # Получить значение, введеное пользователем в эелемент штрихкод.
        str_in = str(self.frame_0_1.get().strip())
        
        # Разбиваем общий код на нужные нам элементы.
        self.gtin = str_in[2:16]
        self.frame_3_1['text'] = str(self.gtin)
        
        # длина серийника.
        count_in = int(self.frame_1_2.get())
        len_serial_number = count_in + 16
        self.isn = str_in[16:len_serial_number]
        self.frame_4_1['text'] = str(self.isn)

    # Функции копирования GTIN & ISN. 
    def copy_gtin(self):
        self.clipboard_clear()
        self.clipboard_append(self.gtin)
        
    def copy_isn(self):
        self.clipboard_clear()
        self.clipboard_append(self.isn)


# Создать экземпляр класса BarcodeGUI.
if __name__ == "__main__":
    app = BarcodeGUI()
    app.mainloop()
