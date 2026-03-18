import tkinter as tk
import datetime
import re

class TicketForm:
    def __init__(self, master, db, application_window, creation_time=None, ticket_number=None):
        self.master = master
        self.db = db
        self.application_window = application_window
        self.creation_time = creation_time
        self.ticket_number = ticket_number
        self.validate_fio_callback = None
        self.validate_phone_number_callback = None
        self.master.configure(background="#82A6CB")

        photo = tk.PhotoImage(file='ikon.png')
        master.wm_iconphoto(False, photo)

        self.ticket_number_label = tk.Label(
            master,font="Verdana 9 normal roman", text="Запись №:", background="#82A6CB")
        self.ticket_number_label.grid(row=0, column=0, sticky="e")

        self.ticket_number_entry = tk.Label(
            master,font="Verdana 9 normal roman", text=str(self.ticket_number), width=20, background="#82A6CB")
        self.ticket_number_entry.grid(row=0, column=1)

        self.label_client = tk.Label(
            master,font="Verdana 9 normal roman", text="ФИО клиента:", background="#82A6CB")
        self.label_client.grid(row=1, column=0, sticky="e")

        self.entry_client = tk.Entry(master)
        self.entry_client.grid(row=1, column=1)

        self.label_pol = tk.Label(
            master,font="Verdana 9 normal roman", text="Пол:", background="#82A6CB")
        self.label_pol.grid(row=2, column=0, sticky="e")

        self.pol_var = tk.StringVar(master)
        self.pol_var.set("Не указано")
        self.pol_options = ["Мужской", "Женский"]
        self.pol_dropdown = tk.OptionMenu(
            master, self.pol_var, *self.pol_options)
        self.pol_dropdown.grid(row=2, column=1)
        self.pol_dropdown.configure(background="#82A6CB")

        self.label_phone = tk.Label(
            master,font="Verdana 9 normal roman", text="Номер телефона:", background="#82A6CB")
        self.label_phone.grid(row=3, column=0, sticky="e")

        self.phone_number = tk.StringVar(master)
        self.entry_phone = tk.Entry(master, textvariable=self.phone_number)
        self.entry_phone.grid(row=3, column=1)


        self.label_service = tk.Label(
            master,font="Verdana 9 normal roman", text="Услуга:", background="#82A6CB")
        self.label_service.grid(row=4, column=0, sticky="e")

        self.service_var = tk.StringVar(master)
        self.service_options = ["Пилинг", "Мезотерапия", "Плазмолифтинг",
                                "Ботулинотерапия", "Биоревитализация",  "Чистка лица"]
        self.service_var.set("Не указано")
        self.service_dropdown = tk.OptionMenu(
            master, self.service_var, *self.service_options)
        self.service_dropdown.grid(row=4, column=1)
        self.service_dropdown.configure(background="#82A6CB")

        self.label_status = tk.Label(
            master,font="Verdana 9 normal roman", text="Статус:", background="#82A6CB")
        self.label_status.grid(row=5, column=0, sticky="e")

        self.status_var = tk.StringVar(master)
        self.status_var.set("Не указано")
        self.status_options = ["Услуга оказана", "Услуга не оказана"]
        self.status_dropdown = tk.OptionMenu(
            master, self.status_var, *self.status_options)
        self.status_dropdown.grid(row=5, column=1)
        self.status_dropdown.configure(background="#82A6CB")

        self.btn_submit = tk.Button(
            master,font="Verdana 10 bold roman", text="Сохранить", command=self.submit, background="#214177", fg="white")
        self.btn_submit.grid(row=6, columnspan=2)

        
    def set_create_ticket_callback(self, callback):
        self.create_ticket_callback = callback


    def set_validate_phone_number_callback(self, callback):
            self.validate_phone_number_callback = callback

    def set_validate_fio_callback(self, callback):
        self.validate_fio_callback = callback

    def submit(self):
        if not self.entry_client.get():
            tk.messagebox.showerror("Ошибка", "Введите ФИО клиента")
            return
        if self.validate_fio_callback:
            if not self.validate_fio_callback(self.entry_client.get()):
                return
        phone_number = self.entry_phone.get()
        if not self.validate_phone_number_callback:
            tk.messagebox.showerror("Ошибка", "Введите номер телефона")
            return
        if not re.match(r'^\+?\d{11}$', phone_number):
            tk.messagebox.showerror("Ошибка", "Неверный формат номера телефона")
            return
        ticket_number = self.ticket_number
        created_at = self.creation_time.strftime(
            '%d.%m.%Y %H:%M:%S') if self.creation_time else datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')

        ticket_data = {
            "ticket_number": self.ticket_number,
            "client": self.entry_client.get(),
            "phone": self.entry_phone.get(),
            "service": self.service_var.get(),
            "status": self.status_var.get(),
            "pol": self.pol_var.get(),
            "created_at": created_at,
            "completion_date": None
        }
        self.db.insert_ticket(ticket_data)
        self.application_window.update_ticket_info()
        self.master.destroy()
