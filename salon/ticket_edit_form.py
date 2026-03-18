import tkinter as tk
from datetime import datetime

class TicketEditForm:
    def __init__(self, master, db, ticket_id, parent_window):
        self.master = master
        self.db = db
        self.ticket_id = ticket_id
        self.parent_window = parent_window
        self.update_client_info_callback = None

        photo = tk.PhotoImage(file='ikon.png')
        master.wm_iconphoto(False, photo)

        self.master.configure(background="#82A6CB")

        self.ticket_data = self.db.get_ticket_by_id(ticket_id)

        self.label_ticket_number = tk.Label(
            master,font="Verdana 9 normal roman", text="Запись №:", background="#82A6CB")
        self.label_ticket_number.grid(row=0, column=0, sticky="e")

        self.entry_ticket_number = tk.Entry(master)
        self.entry_ticket_number.insert(tk.END, self.ticket_data[1])
        self.entry_ticket_number.grid(row=0, column=1)

        self.label_client = tk.Label(
            master,font="Verdana 9 normal roman", text="ФИО клиента:", background="#82A6CB")
        self.label_client.grid(row=1, column=0, sticky="e")

        self.entry_client = tk.Entry(master)
        self.entry_client.insert(tk.END, self.ticket_data[2])
        self.entry_client.grid(row=1, column=1)

        self.label_pol = tk.Label(
            master,font="Verdana 9 normal roman", text="Пол:", background="#82A6CB")
        self.label_pol.grid(row=2, column=0, sticky="e")

        self.pol_var = tk.StringVar(master)
        self.pol_var.set(self.ticket_data[3])
        self.pol_options = ["Муж", "Жен"]
        self.pol_dropdown = tk.OptionMenu(
            master, self.pol_var, *self.pol_options)
        self.pol_dropdown.grid(row=2, column=1)
        self.pol_dropdown.configure(background="#82A6CB")

        self.label_phone = tk.Label(
            master,font="Verdana 9 normal roman", text="Номер телефона:", background="#82A6CB")
        self.label_phone.grid(row=3, column=0, sticky="e")

        self.entry_phone = tk.Entry(master)
        self.entry_phone.insert(tk.END, self.ticket_data[4])
        self.entry_phone.grid(row=3, column=1)

        self.label_service = tk.Label(
            master,font="Verdana 9 normal roman", text="Услуга:", background="#82A6CB")
        self.label_service.grid(row=4, column=0, sticky="e")

        self.service_var = tk.StringVar(master)
        self.service_var.set(self.ticket_data[5])
        self.service_options = ["Пилинг", "Мезотерапия", "Плазмолифтинг",
                                "Ботулинотерапия", "Биоревитализация",  "Чистка лица"]
        self.service_dropdown = tk.OptionMenu(
            master, self.service_var, *self.service_options)
        self.service_dropdown.grid(row=4, column=1)
        self.service_dropdown.configure(background="#82A6CB")

        self.label_status = tk.Label(
            master,font="Verdana 9 normal roman", text="Статус:", background="#82A6CB")
        self.label_status.grid(row=5, column=0, sticky="e")

        self.status_var = tk.StringVar(master)
        self.status_var.set(self.ticket_data[6])
        self.status_options = ["Услуга оказана", "Услуга не оказана"]
        self.status_dropdown = tk.OptionMenu(
            master, self.status_var, *self.status_options)
        self.status_dropdown.grid(row=5, column=1)
        self.status_dropdown.configure(background="#82A6CB")

        self.btn_submit = tk.Button(
            master,font="Verdana 10 bold roman", text="Применить изменения", command=self.save, background="#214177", fg="white")
        self.btn_submit.grid(row=6, columnspan=2)

    def set_update_client_info_callback(self, callback):
        self.update_client_info_callback = callback

    def set_validate_fio_callback(self, callback):
        self.validate_fio_callback = callback

    
    def set_validate_phone_number_callback(self, callback):
            self.validate_phone_number_callback = callback

    def save(self):
        ticket_number = self.entry_ticket_number.get()
        client = self.entry_client.get()
        phone = self.entry_phone.get()
        service = self.service_var.get()
        pol = self.pol_var.get()
        status = self.status_var.get()

        ticket_data = {
            "ticket_number": self.entry_ticket_number.get(),
            "client": self.entry_client.get(),
            "phone": self.entry_phone.get(),
            "service": self.service_var.get(),
            "pol": self.pol_var.get(),
            "status": self.status_var.get()
        }

        if ticket_data['status'] == "Услуга оказана":
            ticket_data['completion_date'] = datetime.now().strftime(
                "%d.%m.%Y %H:%M:%S")

        self.db.update_ticket(self.ticket_id, ticket_data)
        self.parent_window.update_ticket_info()
        self.master.withdraw()  
