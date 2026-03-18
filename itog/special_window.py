import tkinter as tk
from datetime import datetime
from ticket_edit_status_form import TicketEditStatusForm

from tkinter import *
from tkinter.ttk import *


class SpecialWindow:
    def __init__(self, master, username, auth_window, db):
        self.master = master
        photo = tk.PhotoImage(file='img/icon.png')
        master.wm_iconphoto(False, photo)
        self.master.configure(bg="#D5F1E1")
        self.username = username
        self.auth_window = auth_window  # Ссылка на окно авторизации
        self.db = db  # Ссылка на экземпляр базы данных

        self.search_frame2 = tk.Frame(master, bg="#D5F1E1")
        self.search_frame2.pack(fill=tk.BOTH, pady=10)

        self.btn_logout = tk.Button(
            self.search_frame2, text="Выйти", font="Verdana 12 normal roman", bg="#3C5B91", fg="white", relief="groove", borderwidth=7, command=self.logout)
        self.btn_logout.pack(side=tk.RIGHT, padx=15, pady=2)

        self.label_welcome = tk.Label(
            self.search_frame2, text=f"Добро пожаловать, {username}!", font="Verdana 12 normal roman", bg="#D5F1E1")
        self.label_welcome.pack(padx=15, pady=2)

        self.label_datetime = tk.Label(
            self.search_frame2, text="", font="Verdana 8 normal roman", bg="#D5F1E1")
        self.label_datetime.pack(fill=tk.BOTH, padx=15)

        self.search_frame1 = tk.Frame(master, bg="#D5F1E1")
        self.search_frame1.pack(fill=tk.BOTH, pady=15)

        self.search_label = tk.Label(
            self.search_frame1, text="Поиск:", font="Verdana 12 normal roman", bg="#D5F1E1")
        self.search_label.pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(
            self.search_frame1, bg="white")
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(self.search_frame1, text="Найти", font="Verdana 10 normal roman",
                                       bg="#3C5B91", fg="white", relief="ridge", borderwidth=2, command=self.search_tickets_wrapper)
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.update_datetime()  # Начинаем обновление времени

        master.geometry('650x750')
        master.resizable(1, 1)

    def update_datetime(self):
        current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(
            text=current_datetime, bg="#D5F1E1", font="Verdana 11 normal roman")
        # Вызываем метод снова через 1000 мс (1 секунда)
        self.master.after(1000, self.update_datetime)

    def display_tickets(self, tickets):
        for ticket in tickets:
            # Создаем виджеты для отображения информации о заявке
            ticket_info = f"Заявка №: {ticket[1]}\nОборудование: {ticket[2]}\nТип неисправности: {ticket[3]}\nОписание проблемы: {ticket[4]}\nКлиент: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
            if ticket[8]:  # Проверяем, есть ли дата выполнения заявки
                ticket_info += f"\nДата выполнения: {ticket[8]}"
            label = tk.Label(self.master, text=ticket_info,
                             font="Verdana 12 normal roman", bg="#D5F1E1")
            label.pack()

            # Добавляем кнопку "Редактировать" для каждой заявки
            edit_button = tk.Button(self.master, text="Редактировать", command=lambda t=ticket[0]: self.edit_ticket_status(
                t), font="Verdana 12 normal roman", bg="#79A1D2", fg="white")
            edit_button.pack(padx=10, pady=10)

    def update_tickets_display(self):
        # Очищаем текущее отображение заявок, кроме приветственного сообщения и имени пользователя
        for widget in self.master.winfo_children():
            if widget not in (self.search_frame2, self.search_frame1,self.label_datetime):
                widget.destroy()

        tickets = self.db.get_all_tickets()

        # Отображаем заявки
        self.display_tickets(tickets)

    def search_tickets_wrapper(self):
        search_query = self.search_entry.get()
        tickets = self.db.search_tickets(search_query)
        self.update_tickets_display(tickets)

    def edit_ticket_status(self, ticket_id):
        # Открываем окно изменения статуса заявки
        ticket_edit_status_window = tk.Toplevel(self.master)
        ticket_edit_status_window.title("Изменение статуса заявки")
        ticket_edit_status_form = TicketEditStatusForm(
            ticket_edit_status_window, self.db, ticket_id, self)

    def logout(self):
        self.master.destroy()
        self.auth_window.show()


root = Tk()
root.title("Заявки.ру")
root.geometry("250x200")
root.attributes("-toolwindow", 0.5)
root.eval('tk::PlaceWindow . center')
root.configure(bg="#D5F1E1")


def Close():
    root.destroy()


exit_button_image = PhotoImage(file='img/image.png')
exit_button = Button(root, image=exit_button_image,
                     text="Пожалуйста, авторизуйтесь", command=Close)
exit_button.pack(anchor="center", expand=1)


root.mainloop()
