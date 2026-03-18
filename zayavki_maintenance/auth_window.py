import tkinter as tk
from tkinter import messagebox
from database import Database
from application_window import ApplicationWindow
from special_window import SpecialWindow  # Импортируем класс SpecialWindow
from datetime import datetime  # Импортируем datetime для работы с датой и временем
from vip_window import VipWindow
from registr_window import RegistrWindow
from client_window import ClientWindow

from tkinter import *
from tkinter.ttk import *


class AuthWindow:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg="#D5F1E1")
        self.master.title("Заявки.ру/Авторизация")
        self.db = Database("users.db")  # Создаем экземпляр базы данных

        self.label_username = tk.Label(
            master, text="👤 Имя пользователя:", font="Verdana 12 normal roman", bg="#D5F1E1")
        self.label_username.pack(pady=2)

        self.entry_username = tk.Entry(master)
        self.entry_username.pack(pady=7)

        self.label_password = tk.Label(
            master, text="🔒 Пароль:", font="Verdana 12 normal roman", bg="#D5F1E1")
        self.label_password.pack(pady=2)

        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.pack(pady=7)

        # Переменная для хранения состояния флажка
        self.show_password_var = tk.BooleanVar()

        # Создаем флажок "Показать пароль" и привязываем его к функции toggle_password_visibility
        self.checkbox_show_password = tk.Checkbutton(master, text="Показать пароль", font="Verdana 8 italic roman",
                                                     bg="#D5F1E1", variable=self.show_password_var, command=self.toggle_password_visibility)
        self.checkbox_show_password.pack(pady=7)

        self.btn_login = tk.Button(master, text="Войти", font="Verdana 14 normal roman",
                                   bg="#79A1D2", fg="white", relief=RAISED, borderwidth=5, command=self.login)
        self.btn_login.pack(pady=7)

        self.btn_login = tk.Button(master, text="Зарегистрироваться", command=self.reg,
                                   font="Tahoma 12 normal roman", foreground="white", background="#79A1D2")
        self.btn_login.pack()

        master.geometry('350x300')
        master.resizable(1, 1)
        master.eval('tk::PlaceWindow . center')

        self.label_datetime = tk.Label(master, text="")
        self.label_datetime.pack()

        self.update_datetime()  # Начинаем обновление времени

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.db.check_credentials(username, password):
            self.master.withdraw()  # Скрыть окно авторизации
            if username == "slloika":
                self.open_special_window(username)
            elif username == "VIP":
                self.open_vip_window(username)
            elif username == "meow":
                self.open_application_window(username)
            else:
                self.open_client_window(username)
        else:
            messagebox.showerror(
                "Ошибка", "Неверное имя пользователя или пароль")

    def reg(self):
        reg_window = tk.Toplevel(self.master)
        reg_window.title("Главное окно приложения")

        RegistrWindow(reg_window, self.db, self.master)

    def toggle_password_visibility(self):
        if self.show_password_var.get():  # Если флажок установлен
            self.entry_password.config(show="")  # Показываем пароль
        else:
            self.entry_password.config(show="*")  # Скрываем пароль

    def open_application_window(self, username):
        application_window = tk.Toplevel(self.master)
        application_window.title("Заявки.ру / окно администратора 1 ")

        # Передача ссылки на главное окно
        ApplicationWindow(application_window, self.db, username, self.master)

    def open_special_window(self, username):
        special_window = tk.Toplevel(self.master)
        special_window.title("Заявки.ру / специальное окно администратора 2")

        # Передаем экземпляр базы данных в конструктор SpecialWindow
        special_window_instance = SpecialWindow(
            special_window, username, self, self.db)

        # Получаем все заявки из базы данных и отображаем их в специальном окне
        tickets = self.db.get_all_tickets()
        special_window_instance.display_tickets(tickets)

    def open_client_window(self, username):
        client_window = tk.Toplevel(self.master)
        client_window.title("Клиентское окно")

        # Передача ссылки на главное окно
        ClientWindow(client_window, self.db, username, self.master)

    def open_vip_window(self, username):
        vip_window = tk.Toplevel(self.master)
        vip_window.title("Заявки.ру / vip окно для пользователя 3")

        # Передаем экземпляр базы данных в конструктор SpecialWindow
        vip_window_instance = VipWindow(
            vip_window, username, self, self.db)

        # Получаем все заявки из базы данных и отображаем их в специальном окне
        tickets = self.db.get_all_tickets()
        vip_window_instance.display_tickets(tickets)

    def update_datetime(self):
        current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(
            text=current_datetime, bg="#D5F1E1", font="Verdana 11 normal roman")
        # Вызываем метод снова через 1000 мс (1 секунда)
        self.master.after(1000, self.update_datetime)

    def show(self):
        self.master.deiconify()


def main():
    root = tk.Tk()
    auth_window = AuthWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
