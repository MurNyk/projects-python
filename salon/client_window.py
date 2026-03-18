import tkinter as tk
from tkinter import ttk
from datetime import datetime


class ClientWindow:
    def __init__(self, master, application_window, client_name, db):
        self.master = master
        self.application_window = application_window
        self.client_name = client_name
        self.db = db

        self.top_frame = tk.Frame(self.master, bg="#BDD8F1")
        self.top_frame.pack(fill=tk.X, pady=6)

        self.label_datetime = tk.Label(
            self.top_frame, font="Verdana 9 normal roman",text="", bg="#BDD8F1")
        self.label_datetime.pack(anchor=tk.CENTER)

        self.btn_logout = tk.Button(
            master, font="Verdana 9 normal roman",text="Выйти", command=self.logout, bg="#214177", fg="white")
        self.btn_logout.pack()

        self.n_frame = tk.Frame(self.master, bg="#BDD8F1")
        self.n_frame.pack(fill=tk.BOTH, pady=10, padx=15)

        self.service_filter_label = tk.Label(
            self.n_frame, font="Verdana 9 normal roman",text="Услуга:", bg="#BDD8F1")
        self.service_filter_label.pack(side=tk.LEFT)

        self.service_filter_combobox = ttk.Combobox(
            self.n_frame, values=["Пилинг", "Мезотерапия", "Плазмолифтинг", "Ботулинотерапия", "Биоревитализация",  "Чистка лица", "Все"], state="readonly")
        self.service_filter_combobox.current(3) 
        self.service_filter_combobox.pack(side=tk.LEFT)

        self.service_filter_button = tk.Button(
            self.n_frame, font="Verdana 9 normal roman",text="Фильтровать по услуге ↕️", command=self.filter_by_service, bg="#3667A6", fg="white")
        self.service_filter_button.pack(side=tk.LEFT)

        self.u_frame = tk.Frame(self.master, bg="#BDD8F1")
        self.u_frame.pack(fill=tk.BOTH, pady=10)

        self.canvas = tk.Canvas(
            master, width=70, height=300, background="#BDD8F1", highlightthickness=0)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(
            master, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.canvas.yview, bg="#BDD8F1")

        self.frame = tk.Frame(self.canvas, bg="#BDD8F1")
        self.canvas.create_window((35, 0), window=self.frame, anchor=tk.NW)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.frame.bind("<Configure>", lambda event,
                        canvas=self.canvas: self.on_frame_configure(canvas))

        tickets = self.db.get_tickets_by_client(self.client_name)
        self.display_tickets(tickets)

        self.update_datetime()

        self.master.configure(background="#BDD8F1")
        photo = tk.PhotoImage(file='ikon.png')
        master.wm_iconphoto(False, photo)
        self.master.geometry("500x350")
        master.resizable(0, 0)

    def apply_filters(self):
        tickets = self.db.get_all_tickets()

        # Apply service filter
        service = self.service_filter_combobox.get()
        if service != "Все":
            tickets = [t for t in tickets if t[5] == service]

        self.display_tickets(tickets)

    def filter_by_service(self):
        service = self.service_filter_combobox.get()
        if service == "Все":
            tickets = self.db.get_tickets_by_client(self.client_name)
        else:
            tickets = self.db.get_tickets_by_client_and_service(self.client_name, service)
        self.display_tickets(tickets)

    def update_datetime(self):
        current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(font="Verdana 9 normal roman",text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def display_tickets(self, tickets):
        for widget in self.frame.winfo_children():
            widget.destroy()

        if tickets:
            for ticket in tickets:
                ticket_info = f"Запись №: {ticket[1]}\nФИО клиента: {ticket[2]}\nПол: {ticket[3]}\nНомер телефона: {ticket[4]}\nУслуга: {ticket[5]}\nСтатус: {ticket[6]}\nДата/время создания записи: {ticket[7]}\n"
                if ticket[8]:
                    ticket_info += f"Дата и время оказания услуги: {ticket[8]}"

                label = tk.Label(self.frame, font="Verdana 9 normal roman",text=ticket_info,
                                 bg="#BDD8F1", padx=15)
                label.pack(pady=1)
        else:
            no_results_label = tk.Label(
                self.frame, font="Verdana 9 normal roman",text="Записи не найдены для этого клиента.", background="#BDD8F1")
            no_results_label.pack()

        self.canvas.configure(scrollregion=self.canvas.bbox(
            "all"), background="#BDD8F1")

    def search_tickets_wrapper(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        client_name = self.entry_client_name.get().strip()

        if client_name:
            tickets = self.db.search_tickets_by_client(client_name)
            if tickets:
                self.display_tickets(tickets) 
                self.canvas.configure(scrollregion=self.canvas.bbox(
                    "all"), background="#BDD8F1")
            else:
                no_results_label = tk.Label(
                    self.frame, font="Verdana 9 normal roman",text="Записи не найдены.", background="#BDD8F1")
                no_results_label.pack()
        else:
            no_results_label = tk.Label(
                self.frame, font="Verdana 9 normal roman",text="Введите данные для поиска.", background="#BDD8F1")
            no_results_label.pack()

    def logout(self):
        self.master.destroy()
        self.auth_window.show()

    def _on_mousewheel(self, event):
        if self.canvas is not None:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_frame_configure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"), background="#BDD8F1")
