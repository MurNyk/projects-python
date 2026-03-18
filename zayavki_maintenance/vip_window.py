import tkinter as tk
from datetime import datetime
from ticket_edit_status_form import TicketEditStatusForm

from tkinter import *
from tkinter.ttk import *


class VipWindow:
    def __init__(self, master, username, auth_window, db):
        self.master = master
        photo = tk.PhotoImage(file='img/icon.png')
        master.wm_iconphoto(False, photo)
        self.master.configure(bg="#FFFF99")
        self.username = username
        self.auth_window = auth_window  # Ссылка на окно авторизации
        self.db = db  # Ссылка на экземпляр базы данных

        self.search_frame3 = tk.Frame(master, bg="#FFFF99")
        self.search_frame3.pack(fill=tk.BOTH, pady=10)

        self.btn_logout = tk.Button(
            self.search_frame3, text="Выйти", font="Georgia 12 normal roman", bg="#FFD700", fg="#7B001C", command=self.logout)
        self.btn_logout.pack(side=tk.RIGHT, padx=15, pady=2)

        self.label_welcome = tk.Label(
            self.search_frame3, text=f"Добро пожаловать, {username}!", font="Georgia 12 normal roman", bg="#FFFF99")
        self.label_welcome.pack(padx=15, pady=2)

        self.label_datetime = tk.Label(self.search_frame3, text="")
        self.label_datetime.pack(fill=tk.BOTH, padx=15)

        self.search_frame4 = tk.Frame(master, bg="#FFFF99")
        self.search_frame4.pack(fill=tk.BOTH, pady=15)

        self.search_label = tk.Label(
            self.search_frame4, text="Поиск:", font="Georgia 12 normal roman", bg="#FFFF99")
        self.search_label.pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(
            self.search_frame4, bg="white")
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(self.search_frame4, text="Найти", font="Verdana 10 normal roman",
                                       bg="#FFD700", fg="#7B001C", relief="ridge", borderwidth=2, command=self.search_tickets_wrapper)
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.update_datetime()  # Начинаем обновление времени

        master.geometry('650x750')
        master.resizable(1, 1)

    def update_datetime(self):
        current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(
            text=current_datetime, bg="#FFFF99", font="Georgia 11 normal roman")
        # Вызываем метод снова через 1000 мс (1 секунда)

        self.master.after(1000, self.update_datetime)

    def display_tickets(self, tickets):
        for ticket in tickets:

            # Создаем виджеты для отображения информации о заявке
            ticket_info = f"Заявка №: {ticket[1]}\nОборудование: {ticket[2]}\nТип неисправности: {ticket[3]}\nОписание проблемы: {ticket[4]}\nКлиент: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
            if ticket[8]:  # Проверяем, есть ли дата выполнения заявки
                ticket_info += f"\nДата выполнения: {ticket[8]}"
            label = tk.Label(self.master, text=ticket_info,
                             font="Georgia 12 normal roman", bg="#FFFF99")
            label.pack(pady=10)

            # Добавляем "Оценку заявки"
            label = tk.Label(
                self.master, text=f"Ваша оценка заявки от 0 до 100", bg="#FFFF99", font="Georgia 10 normal roman")
            label.pack()

            def update_label(value):
                label.config()
            scale = tk.Scale(self.master, from_=0, to=100,
                             orient="horizontal", command=update_label, font="Georgia 10 normal roman", bg="#FFD700", fg="#7B001C")
            scale.pack(pady=10)

           
    def update_tickets_display(self):
        # Очищаем текущее отображение заявок, кроме приветственного сообщения и имени пользователя
        for widget in self.master.winfo_children():
            if widget not in (self.label_datetime, self.search_frame3, self.search_frame4):
                widget.destroy()

        tickets = self.db.get_all_tickets()

        # Отображаем заявки
        self.display_tickets(tickets)

    def search_tickets_wrapper(self):
        search_query = self.search_entry.get()
        tickets = self.db.search_tickets(search_query)
        self.update_tickets_display(tickets)


    def logout(self):
        self.master.destroy()
        self.auth_window.show()
