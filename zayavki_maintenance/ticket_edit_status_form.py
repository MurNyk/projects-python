import tkinter as tk
from datetime import datetime


class TicketEditStatusForm:
    def __init__(self, master, db, ticket_id, parent_window):
        self.master = master
        self.master.configure(bg="#D5F1E1")
        self.db = db
        self.ticket_id = ticket_id
        self.parent_window = parent_window

        master.geometry('300x220')
        master.resizable(0, 0)

        self.ticket_data = self.db.get_ticket_by_id(ticket_id)

        self.frame123 = tk.Frame(self.master, bg="#D5F1E1")
        self.frame123.pack( padx=25, pady=30)

        self.label_status = tk.Label(
           self.frame123, text="Статус:", font="Verdana 12 normal roman", bg="#D5F1E1")
        self.label_status.grid(row=0, column=0, sticky="e")

        self.status_var = tk.StringVar(master)
        # Устанавливаем текущий статус заявки
        self.status_var.set(self.ticket_data[6])
        self.status_options = ["В ожидании", "В работе", "Выполнено"]
        self.status_dropdown = tk.OptionMenu(
            self.frame123, self.status_var, *self.status_options)
        self.status_dropdown.grid(row=0, column=1)

        self.btn_submit = tk.Button(
            self.frame123, text="Сохранить", font="Verdana 12 normal roman", bg="#3C5B91", fg="white", command=self.save)
        self.btn_submit.grid(row=1, columnspan=2)

    def save(self):
        ticket_data = {
            # Используем текущее значение equipment из self.ticket_data
            "equipment": self.ticket_data[2],
            "fault_type": self.ticket_data[3],
            "problem_description": self.ticket_data[4],
            "client": self.ticket_data[5],
            "status": self.status_var.get(),
            # Другие поля, если есть
        }

        if ticket_data['status'] == "Выполнено":
            ticket_data['completion_date'] = datetime.now().strftime(
                "%d.%m.%Y %H:%M:%S")

        self.db.update_ticket(self.ticket_id, ticket_data)
        self.parent_window.update_tickets_display()
        self.master.destroy()

        self.db.update_ticket(self.ticket_id, ticket_data)
        # Добавляем вызов метода обновления отображения заявок
        self.parent_window.update_tickets_display()
        self.master.destroy()
