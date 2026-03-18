import tkinter as tk
import datetime


class TicketForm:
    def __init__(self, master, db, application_window, creation_time=None):  # Добавлен аргумент creation_time
        self.master = master
        self.master.configure(bg="#D5F1E1")
        self.db = db
        self.application_window = application_window
        self.creation_time = creation_time

        self.label_ticket_number = tk.Label(master, text="Заявка №:",font="Tahoma 10 normal roman", bg="#D5F1E1")
        self.label_ticket_number.grid(row=0, column=0, sticky="e")

        self.entry_ticket_number = tk.Entry(master)
        self.entry_ticket_number.grid(row=0, column=1)

        self.label_equipment = tk.Label(master, text="Оборудование:", font="Tahoma 10 normal roman", bg="#D5F1E1")
        self.label_equipment.grid(row=1, column=0, sticky="e")

        self.entry_equipment = tk.Entry(master)
        self.entry_equipment.grid(row=1, column=1)

        self.label_fault_type = tk.Label(master, text="Тип неисправности:", font="Tahoma 10 normal roman", bg="#D5F1E1")
        self.label_fault_type.grid(row=2, column=0, sticky="e")

        self.entry_fault_type = tk.Entry(master)
        self.entry_fault_type.grid(row=2, column=1)

        self.label_problem_description = tk.Label(master, text="Описание проблемы:", font="Tahoma 10 normal roman", bg="#D5F1E1")
        self.label_problem_description.grid(row=3, column=0, sticky="e")

        self.entry_problem_description = tk.Entry(master)
        self.entry_problem_description.grid(row=3, column=1)

        self.label_client = tk.Label(master, text="Клиент:", font="Tahoma 10 normal roman", bg="#D5F1E1")
        self.label_client.grid(row=4, column=0, sticky="e")

        self.entry_client = tk.Entry(master)
        self.entry_client.grid(row=4, column=1)

        # Добавляем выбор статуса
        self.label_status = tk.Label(master, text="Статус:", font="Tahoma 10 normal roman", bg="#D5F1E1")
        self.label_status.grid(row=5, column=0, sticky="e")

        self.status_var = tk.StringVar(master)
        self.status_var.set("В ожидании")
        self.status_options = ["В ожидании", "В работе", "Выполнено"]
        self.status_dropdown = tk.OptionMenu(master, self.status_var, *self.status_options)
        self.status_dropdown.grid(row=5, column=1)

        self.btn_submit = tk.Button(master, text="Отправить",font="Tahoma 10 normal roman", bg="#3C5B91",fg="white", command=self.submit)
        self.btn_submit.grid(row=6, columnspan=2)

        master.geometry('300x220')
        master.resizable(0, 0)
        master.eval('tk::PlaceWindow . center')

    def submit(self):
        # Используем сохраненное время создания заявки, если оно было передано
        created_at = self.creation_time.strftime('%d.%m.%Y %H:%M:%S') if self.creation_time else datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')

        ticket_data = {
            "ticket_number": self.entry_ticket_number.get(),
            "equipment": self.entry_equipment.get(),
            "fault_type": self.entry_fault_type.get(),
            "problem_description": self.entry_problem_description.get(),
            "client": self.entry_client.get(),
            "status": self.status_var.get(),  # Получаем выбранный статус
            "created_at": created_at  # Используем сохраненное время создания заявки
        }
        self.db.insert_ticket(ticket_data)
        self.application_window.update_ticket_info()
        self.master.destroy()
