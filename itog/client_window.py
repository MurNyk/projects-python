import tkinter as tk
from tkinter import ttk, Canvas
import datetime
from client_ticket_form import ClientTicketForm
from ticket_edit_status_form import TicketEditStatusForm
import statistics_window
from tkinter import messagebox

from tkinter import *
from tkinter.ttk import *

class ClientWindow:
    def __init__(self, master, db, current_user, root):
        self.master = master
        self.root = root  # Сохраняем ссылку на главное окно
        self.db = db
        self.current_user = current_user

        photo = tk.PhotoImage(file = 'img/icon.png')
        master.wm_iconphoto(False, photo)

        self.master.configure(background="#D5F1E1")
        x = (master.winfo_screenwidth() - master.winfo_reqwidth()) / 2
        y = (master.winfo_screenheight() - master.winfo_reqheight()) / 2
        master.wm_geometry("+%d+%d" % (x, y))
        master.geometry('650x550')
        master.resizable(0, 0)

        master.grid_rowconfigure(3, weight=1)
        master.grid_columnconfigure(0, weight=1)


        self.header_frame = tk.Frame(master, width=800, background="#D5F1E1")
        self.header_frame.pack()

        self.label_user_info = tk.Label(self.header_frame, text=f"Пользователь: {self.current_user}", font="Verdana 12 normal roman", bg="#D5F1E1")
        self.label_user_info.pack(pady=15, side=LEFT)

        self.btn_logout = tk.Button(self.header_frame, text="Выйти", command=self.logout, font="Verdana 12 normal roman", bg="#3C5B91", fg="white", relief="groove", borderwidth=7)
        self.btn_logout.pack(side=tk.RIGHT, padx=15, pady=2)

        self.btn_create_ticket = tk.Button(self.header_frame, text="Создать заявку", command=self.create_ticket,font="Verdana 12 bold roman", bg="#79A1D2", fg="white", relief="raised", borderwidth=5)
        self.btn_create_ticket.pack(side=tk.LEFT)


        self.ticket_frame = tk.Frame(master)
        self.ticket_frame.pack(padx=5, pady=5)

        self.label_ticket_info = tk.Label(self.ticket_frame, text="", font="helvetica 14", foreground="#1F1E20", background="#D5F1E1")
        self.label_ticket_info.pack()


        self.footer_frame = tk.Frame(master, width=800)
        self.footer_frame.pack(padx=5, pady=5)

        self.label_datetime = tk.Label(self.footer_frame, text="",  font="Verdana 12 normal roman", bg="#D5F1E1")
        self.label_datetime.pack()

        self.ticket_labels = []
        self.edit_buttons = []

        self.update_ticket_info()
        self.update_datetime()


    def create_ticket(self):
        current_datetime = datetime.datetime.now()  # Получаем текущее время
        latest_ticket = self.db.get_latest_ticket()
        ticket_window = tk.Toplevel(self.master)
        ticket_window.title("Форма заявки")
        # Передаем текущее время в форму заявки
        ticket_form = ClientTicketForm(ticket_window, self.db, self, creation_time=current_datetime, username=self.current_user)

    def delete_ticket(self, ticket_id):
        ticket = self.db.get_ticket_by_id(ticket_id)
        if ticket[6] != "В работе":
            self.db.delete_ticket(ticket_id)
            self.update_ticket_info()
        else:
            messagebox.showerror("Ошибка", "Вы не можете удалить заявку на этапе ее выполнения. Для отмены заявки свяжитесь с нами по номеру: +7(132)(456)-78-96.")

    def update_ticket_info(self):

        for label in self.ticket_labels:
            label.destroy()

        tickets = self.db.search_by_user(self.current_user)


        ticket_frame = tk.Frame(self.master, borderwidth=4, relief="raised",  background="#D5F1E1")
        ticket_frame.pack()
        self.ticket_labels.append(ticket_frame)
        ticket_frame.grid_rowconfigure(0, weight=1)
        ticket_frame.grid_columnconfigure(0, weight=1)
        tickets_list = tk.Canvas(ticket_frame, bg="#D5F1E1", width=420)
        tickets_list.pack(side=LEFT)
        scroll_bar = tk.Scrollbar(ticket_frame, orient="vertical", command=tickets_list.yview)  
        scroll_bar.pack(side=LEFT, fill="y")
        tickets_list.configure(yscrollcommand=scroll_bar.set)

        frame_tickets = tk.Frame(tickets_list, bg="#D5F1E1")
        tickets_list.create_window((0, 0), window=frame_tickets, anchor=NW)
        
        for ticket in tickets:
            ticket_info = f"Заявка №: {ticket[1]}\nОборудование: {ticket[2]}\nТип неисправности: {ticket[3]}\nОписание проблемы: {ticket[4]}\nКлиент: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
            if ticket[8]:  # Проверяем, есть ли информация о дате и времени выполнения заявки
                ticket_info += f"\nДата и время выполнения: {ticket[8]}"
            label = tk.Label(frame_tickets, text=ticket_info, font="Verdana 12 normal roman", bg="#D5F1E1")
            label.pack()
            self.ticket_labels.append(label)

            edit_button = tk.Button(frame_tickets, text="Удалить", command=lambda t=ticket[0]: self.delete_ticket(t), font="Verdana 12 normal roman", bg="#79A1D2", fg="white")
            edit_button.pack(pady=5)
            self.edit_buttons.append(edit_button)


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

    def update_datetime(self):
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(text=current_datetime)
        self.master.after(1000, self.update_datetime)  # Обновляем каждую секунду
    
    def logout(self):
        self.master.destroy()
        self.root.deiconify()  # Отобразить окно аутентификации