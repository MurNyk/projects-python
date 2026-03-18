import tkinter as tk
import datetime
from ticket_form import TicketForm
from ticket_edit_form import TicketEditForm
import statistics_window

from tkinter import *
from tkinter.ttk import *


class ApplicationWindow:

    def __init__(self, master, db, current_user, root):
        self.master = master
        photo = tk.PhotoImage(file='img/icon.png')
        master.wm_iconphoto(False, photo)
        self.master.configure(bg="#D5F1E1")
        self.root = root  # Сохраняем ссылку на главное окно
        self.db = db
        self.current_user = current_user

        self.top_frame = tk.Frame(self.master, bg="#D5F1E1")
        self.top_frame.pack(fill=tk.BOTH, pady=6)

        self.btn_logout = tk.Button(
            self.top_frame, text="Выйти", font="Verdana 12 normal roman", bg="#3C5B91", fg="white", relief="groove", borderwidth=7, command=self.logout)
        self.btn_logout.pack(side=tk.RIGHT, padx=15, pady=2)

        self.btn_statistics = tk.Button(self.top_frame, text="Статистика", font="Verdana 12 normal roman",
                                        bg="#79A1D2", fg="white", relief="raised", borderwidth=5, command=self.open_statistics_window)
        self.btn_statistics.pack(side=tk.LEFT, padx=15, pady=2)

        self.frame = tk.Frame(self.master, bg="#D5F1E1")
        self.frame.pack(fill=tk.BOTH, padx=15)

        self.btn_create_ticket = tk.Button(
            self.frame, text="Создать заявку", font="Verdana 12 bold roman", bg="#79A1D2", fg="white", relief="raised", borderwidth=5, command=self.create_ticket)
        self.btn_create_ticket.pack(side=tk.LEFT)

        # Добавляем поля для поиска
        self.search_frame = tk.Frame(master, bg="#D5F1E1")
        self.search_frame.pack(fill=tk.BOTH, pady=15)

        self.search_label = tk.Label(
            self.search_frame, text="Поиск:", font="Verdana 12 normal roman", bg="#D5F1E1")
        self.search_label.pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(
            self.search_frame, bg="white")
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(self.search_frame, text="Найти", font="Verdana 10 normal roman",
                                       bg="#3C5B91", fg="white", relief="ridge", borderwidth=2, command=self.search_tickets)
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.label_ticket_info = tk.Label(
            master, text="", font="Verdana 12 normal roman", bg="#D5F1E1")
        self.label_ticket_info.pack()

        self.label_user_info = tk.Label(
            master, text=f"Админ: {self.current_user}", font="Verdana 12 normal roman", bg="#D5F1E1")
        self.label_user_info.pack()

        self.label_datetime = tk.Label(
            master, text="", font="Verdana 12 normal roman", bg="#D5F1E1")
        self.label_datetime.pack()

        self.ticket_labels = []
        self.edit_buttons = []
        self.delete_buttons = []

        self.update_ticket_info()
        self.update_datetime()

        master.geometry('650x550')
        master.resizable(1, 1)

    def create_ticket(self):
        current_datetime = datetime.datetime.now()  # Получаем текущее время
        latest_ticket = self.db.get_latest_ticket()
        ticket_window = tk.Toplevel(self.master)
        ticket_window.title("Форма заявки")
        # Передаем текущее время в форму заявки
        ticket_form = TicketForm(
            ticket_window, self.db, self, creation_time=current_datetime)

    def open_statistics_window(self):
        statistics_window.create_statistics_window(self.db)

    def edit_ticket(self, ticket_id):
        ticket = self.db.get_ticket_by_id(ticket_id)
        ticket_window = tk.Toplevel(self.master)
        ticket_window.title("Редактирование заявки")
        ticket_edit_form = TicketEditForm(
            ticket_window, self.db, ticket_id, self)

    def delete_ticket(self, ticket_id):
        self.db.delete_ticket(ticket_id)
        self.update_ticket_info()

    def search_tickets(self):
        search_query = self.search_entry.get()
        self.update_ticket_info(search_query=search_query)

    def update_ticket_info(self, search_query=None):
        self.remove_edit_buttons()
        self.remove_delete_buttons()

        for label in self.ticket_labels:
            label.destroy()

        if search_query:
            tickets = self.db.search_tickets(search_query)
        else:
            tickets = self.db.get_all_tickets()

        ticket_frame = tk.Frame(self.master, borderwidth=4, relief="raised",  bg="#D5F1E1")
        ticket_frame.pack()
        self.ticket_labels.append(ticket_frame)
        ticket_frame.grid_rowconfigure(0, weight=1)
        ticket_frame.grid_columnconfigure(0, weight=1)
        tickets_list = tk.Canvas(ticket_frame,  bg="#D5F1E1", width=420)
        tickets_list.pack(side=LEFT)
        scroll_bar = tk.Scrollbar(
            ticket_frame, orient="vertical", command=tickets_list.yview)
        scroll_bar.pack(side=LEFT, fill="y")
        tickets_list.configure(yscrollcommand=scroll_bar.set)

        frame_tickets = tk.Frame(tickets_list, bg="#D5F1E1")
        tickets_list.create_window((0, 0), window=frame_tickets, anchor=NW)

        for ticket in tickets:
            ticket_info = f"Заявка №: {ticket[1]}\nОборудование: {ticket[2]}\nТип неисправности: {ticket[3]}\nОписание проблемы: {ticket[4]}\nКлиент: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
            if ticket[8]:  # Проверяем, есть ли информация о дате и времени выполнения заявки
                ticket_info += f"\nДата и время выполнения: {ticket[8]}"
            label = tk.Label(frame_tickets, text=ticket_info,
                             font="Verdana 12 normal roman", bg="#D5F1E1")
            label.pack()
            self.ticket_labels.append(label)

            edit_button = tk.Button(
                frame_tickets, text="Редактировать", command=lambda t=ticket[0]: self.edit_ticket(t), font="Verdana 12 normal roman", bg="#79A1D2", fg="white")
            edit_button.pack(pady=5)
            self.edit_buttons.append(edit_button)

            delete_button = tk.Button(
                frame_tickets, text="Удалить", command=lambda t=ticket[0]: self.delete_ticket(t), font="Verdana 12 normal roman", bg="#79A1D2", fg="white")
            delete_button.pack(pady=5)
            self.delete_buttons.append(delete_button)

        frame_tickets.update_idletasks()
        tickets_list.config(scrollregion=tickets_list.bbox("all"))

        if tickets:
            self.label_ticket_info.config(text="Заявки")
        else:
            self.label_ticket_info.config(text="Нет созданных заявок")

    def remove_edit_buttons(self):
        for button in self.edit_buttons:
            button.destroy()
        self.edit_buttons = []

    def remove_delete_buttons(self):
        for button in self.delete_buttons:
            button.destroy()
        self.delete_buttons = []

    def update_datetime(self):
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(text=current_datetime)
        # Обновляем каждую секунду
        self.master.after(1000, self.update_datetime)

    def logout(self):
        self.master.destroy()
        self.root.deiconify()  # Отобразить окно аутентификации
