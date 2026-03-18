import tkinter as tk
from tkinter import messagebox
from database import Database
from client_window import ClientWindow 
from datetime import datetime 

from tkinter import *
from tkinter.ttk import *



class RegistrWindow:
    def __init__(self, master, db, root):
        admin_pass = "rootds123"
        self.master = master
        self.root = root
        self.master.title("Регистрация")
        self.db = db  # Создаем экземпляр базы данных
        self.master.configure(background="#D5F1E1")
        x = (master.winfo_screenwidth() - master.winfo_reqwidth()) / 2
        y = (master.winfo_screenheight() - master.winfo_reqheight()) / 2
        master.wm_geometry("+%d+%d" % (x, y)) 
        master.geometry('300x300')
        master.resizable(0, 0)


        self.label_username = tk.Label(master, text="Имя пользователя:", font="helvetica 14", foreground="#1F1E20", background="#D5F1E1")
        self.label_username.pack()

        self.entry_username = tk.Entry(master, foreground="#1F1E20")
        self.entry_username.pack()

        self.label_password = tk.Label(master, text="Пароль:", font="helvetica 14", foreground="#1F1E20", background="#D5F1E1")
        self.label_password.pack()

        self.entry_password = tk.Entry(master, show="*", foreground="#1F1E20")
        self.entry_password.pack()

        self.show_password_var = tk.BooleanVar()  # Переменная для хранения состояния флажка

        # Создаем флажок "Показать пароль" и привязываем его к функции toggle_password_visibility
        self.checkbox_show_password = tk.Checkbutton(master, text="Показать пароль", variable=self.show_password_var, command=self.toggle_password_visibility, foreground="#1F1E20", background="#D5F1E1")
        self.checkbox_show_password.pack()

        self.btn_login = tk.Button(master, text="Зарегистрироваться", command=self.auth, font="helvetica 10", foreground="#1F1E20", background="#79A1D2")
        self.btn_login.pack()

        self.label_datetime = tk.Label(master, text="", foreground="#1F1E20", background="#D5F1E1")
        self.label_datetime.pack()

        self.update_datetime()  # Начинаем обновление времени


    def auth(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if not self.db.check_credentials(username, password):
            if username != "" and password != "":
                self.db.insert_user(username, password)
                self.master.withdraw()
                self.open_client_window(username)
            else:
                  messagebox.showerror("Ошибка", "Введены некоректные данные")     
        else:
            messagebox.showerror("Ошибка", "Такой пользователь уже существует")

    def toggle_password_visibility(self):
        if self.show_password_var.get():  # Если флажок установлен
            self.entry_password.config(show="")  # Показываем пароль
        else:
            self.entry_password.config(show="*")  # Скрываем пароль

    def open_client_window(self, username):
        client_window = tk.Toplevel(self.master)
        client_window.title("Клиентское окно")

        ClientWindow(client_window, self.db, username, self.root)  # Передача ссылки на главное окно

    def update_datetime(self):
        current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(text=current_datetime)
        self.master.after(1000, self.update_datetime)  # Вызываем метод снова через 1000 мс (1 секунда)

    def show(self):
        self.master.destroy()
        self.root.deiconify()

