import tkinter as tk
from tkinter import ttk
import datetime
from ticket_form import TicketForm
from ticket_edit_form import TicketEditForm
from client_window import ClientWindow
import tkinter.messagebox
import re


from tkinter import *
from tkinter.ttk import *


class ApplicationWindow:
    def __init__(self, master, db, current_user, root):
        self.master = master
        self.root = root
        self.db = db
        self.current_user = current_user
        self.master.state("zoomed")

        self.top_frame = tk.Frame(self.master, bg="#82A6CB")
        self.top_frame.pack(fill=tk.BOTH)

        self.btn_create_ticket = tk.Button(
            self.top_frame, font="Verdana 9 normal roman", text="Добавить запись",fg="white", command=self.create_ticket, bg="#3667A6")
        self.btn_create_ticket.pack(side=tk.LEFT, padx=10)

        self.label_datetime = tk.Label(
            self.top_frame, font="Verdana 10 bold roman", text="", bg="#82A6CB", fg="white")
        self.label_datetime.pack(anchor=tk.CENTER, pady=(10, 0))

        self.btn_logout = tk.Button(
            self.top_frame, font="Verdana 9 bold roman", text="Выход", bg="#214177", fg="white", command=self.logout)
        self.btn_logout.pack(side=tk.RIGHT, padx=(0, 25), pady=(0, 30))

        self.search_frame = tk.Frame(master, bg="#BDD8F1")
        self.search_frame.pack(fill=tk.X, padx=15, pady=3)

        self.search_label = tk.Label(
            self.search_frame, font="Verdana 9 bold roman", text="Поиск:", bg="#BDD8F1")
        self.search_label.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(
            self.search_frame,  width=100)
        self.search_entry.pack(side=tk.LEFT)

        self.search_button = tk.Button(
            self.search_frame, font="Verdana 9 bold roman", text="Найти", command=self.search_tickets, bg="#214177", fg="white")
        self.search_button.pack(side=tk.LEFT)

        self.btn_history = tk.Button(
            self.search_frame, font="Verdana 9 normal roman", text="История поиска", command=self.show_search_history, bg="#3667A6", fg="white")
        self.btn_history.pack(side=tk.RIGHT, padx=5)

        
        self.rch_frame = tk.Frame(self.master, bg="#BDD8F1")
        self.rch_frame.pack(fill=tk.BOTH, pady=7, padx=15)

        self.rch_label = tk.Label(
            self.rch_frame, font="Verdana 9 bold roman", text="Выберите один или несколько фильтров", bg="#BDD8F1")
        self.rch_label.pack(side=tk.LEFT)

        self.filter_frame = tk.Frame(self.master, bg="#BDD8F1")
        self.filter_frame.pack(fill=tk.BOTH, pady=3, padx=15)

        self.gender_filter_label = tk.Label(
            self.filter_frame, font="Verdana 9 bold roman", text="Пол:", bg="#BDD8F1",fg="#214177")
        self.gender_filter_label.pack(side=tk.LEFT)

        self.gender_filter_male = tk.BooleanVar()
        self.gender_filter_female = tk.BooleanVar()
        self.gender_filter_all = tk.BooleanVar(value=True)

        self.gender_filter_male_checkbox = tk.Checkbutton(
            self.filter_frame, font="Verdana 9 normal roman", text="Мужской", variable=self.gender_filter_male, bg="#BDD8F1")
        self.gender_filter_male_checkbox.pack(side=tk.LEFT)

        self.gender_filter_female_checkbox = tk.Checkbutton(
            self.filter_frame, font="Verdana 9 normal roman", text="Женский", variable=self.gender_filter_female, bg="#BDD8F1")
        self.gender_filter_female_checkbox.pack(side=tk.LEFT)

        self.gender_filter_all_checkbox = tk.Checkbutton(
            self.filter_frame, font="Verdana 9 normal roman", text="Все", variable=self.gender_filter_all, bg="#BDD8F1", command=self.toggle_gender_filters)
        self.gender_filter_all_checkbox.pack(side=tk.LEFT)

        self.filter1_frame = tk.Frame(self.master, bg="#BDD8F1")
        self.filter1_frame.pack(fill=tk.BOTH, pady=3, padx=15)

        self.service_filter_label = tk.Label(
            self.filter1_frame, font="Verdana 9 bold roman", text="Услуга:", bg="#BDD8F1",fg="#214177")
        self.service_filter_label.pack(side=tk.LEFT)

        self.service_filter_piling = tk.BooleanVar()
        self.service_filter_mezoterapia = tk.BooleanVar()
        self.service_filter_plazmolifting = tk.BooleanVar()
        self.service_filter_botox = tk.BooleanVar()
        self.service_filter_biorevitalization = tk.BooleanVar()
        self.service_filter_cleaning = tk.BooleanVar()
        self.service_filter_all = tk.BooleanVar(value=True)

        self.service_filter_piling_checkbox = tk.Checkbutton(
            self.filter1_frame, font="Verdana 9 normal roman", text="Пилинг", variable=self.service_filter_piling, bg="#BDD8F1")
        self.service_filter_piling_checkbox.pack(side=tk.LEFT)

        self.service_filter_mezoterapia_checkbox = tk.Checkbutton(
            self.filter1_frame, font="Verdana 9 normal roman", text="Мезотерапия", variable=self.service_filter_mezoterapia, bg="#BDD8F1")
        self.service_filter_mezoterapia_checkbox.pack(side=tk.LEFT)

        self.service_filter_plazmolifting_checkbox = tk.Checkbutton(
            self.filter1_frame, font="Verdana 9 normal roman", text="Плазмолифтинг", variable=self.service_filter_plazmolifting, bg="#BDD8F1")
        self.service_filter_plazmolifting_checkbox.pack(side=tk.LEFT)

        self.service_filter_botox_checkbox = tk.Checkbutton(
            self.filter1_frame, font="Verdana 9 normal roman", text="Ботулинотерапия", variable=self.service_filter_botox, bg="#BDD8F1")
        self.service_filter_botox_checkbox.pack(side=tk.LEFT)

        self.service_filter_biorevitalization_checkbox = tk.Checkbutton(
            self.filter1_frame, font="Verdana 9 normal roman", text="Биоревитализация", variable=self.service_filter_biorevitalization, bg="#BDD8F1")
        self.service_filter_biorevitalization_checkbox.pack(side=tk.LEFT)

        self.service_filter_cleaning_checkbox = tk.Checkbutton(
            self.filter1_frame, font="Verdana 9 normal roman", text="Чистка лица", variable=self.service_filter_cleaning, bg="#BDD8F1")
        self.service_filter_cleaning_checkbox.pack(side=tk.LEFT)

        self.service_filter_all_checkbox = tk.Checkbutton(
            self.filter1_frame, font="Verdana 9 normal roman", text="Все", variable=self.service_filter_all, bg="#BDD8F1", command=self.toggle_service_filters)
        self.service_filter_all_checkbox.pack(side=tk.LEFT)

        self.filter2_frame = tk.Frame(self.master, bg="#BDD8F1")
        self.filter2_frame.pack(fill=tk.BOTH, pady=3, padx=15)

        self.date_filter_label = tk.Label(
            self.filter2_frame, font="Verdana 9 bold roman", text="Дата создания:", bg="#BDD8F1",fg="#214177")
        self.date_filter_label.pack(side=tk.LEFT)

        self.date_from_label = tk.Label(
            self.filter2_frame, font="Verdana 9 normal roman", text="От:", bg="#BDD8F1")
        self.date_from_label.pack(side=tk.LEFT)

        self.date_from_entry = tk.Entry(
            self.filter2_frame)
        self.date_from_entry.pack(side=tk.LEFT)

        self.date_to_label = tk.Label(
            self.filter2_frame, font="Verdana 9 normal roman", text="До:", bg="#BDD8F1")
        self.date_to_label.pack(side=tk.LEFT)

        self.date_to_entry = tk.Entry(
            self.filter2_frame)
        self.date_to_entry.pack(side=tk.LEFT)

        self.filter3_frame = tk.Frame(self.master, bg="#BDD8F1")
        self.filter3_frame.pack(fill=tk.BOTH, pady=10)

        self.filter_button = tk.Button(
            self.filter3_frame, font="Verdana 9 normal roman", text="Фильтровать", command=self.apply_filters, bg="#3667A6", fg="white")
        self.filter_button.pack(side=tk.LEFT, padx=15)

        clear_button = tk.Button(
            self.filter3_frame, font="Verdana 9 normal roman", text="Очистить фильтры", command=self.clear_filters, bg="#3667A6", fg="white")
        clear_button.pack(side=tk.LEFT)

        self.search_history = []  # initialize search history list


        self.label_frame = tk.Frame(self.master, bg="#BDD8F1")
        self.label_frame.pack(fill=tk.BOTH, pady=6)

        self.label_ticket_info = tk.Label(
            self.label_frame, font="Verdana 10 bold roman", text="", bg="#BDD8F1")
        self.label_ticket_info.pack(side=tk.LEFT, padx=200)

        self.sort_button = tk.Button(
            self.label_frame, font="Verdana 9 normal roman", text="Сортировать по ФИО ↓↑", command=self.sort_by_client, bg="#3667A6", fg="white")
        self.sort_button.pack(side=tk.LEFT, padx=(170, 0), pady=10)

        # направление сортировки (True - по алфавиту, False - наоборот)
        self.sort_direction = True

        self.sort_by_ticket_button = tk.Button(
            self.label_frame, font="Verdana 9 normal roman", text="Сортировать по  № записи ↓↑", command=self.sort_by_ticket, bg="#3667A6", fg="white")
        self.sort_by_ticket_button.pack(side=tk.LEFT, padx=(15, 0))

        # направление сортировки (True - по возрастанию, False - по убыванию)
        self.sort_ticket_direction = True

        
        self.btn_delete_all_tickets = tk.Button(
            self.label_frame, font="Verdana 9 normal roman", text="Удалить все записи", command=self.delete_all_tickets, bg="#214177", fg="white")
        self.btn_delete_all_tickets.pack(side=tk.RIGHT, padx=(0, 30))

        ###
        self.ticket_frame = tk.Frame(master, bg="#82A6CB")
        self.ticket_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(
            self.ticket_frame, orient=tk.VERTICAL, bg="#82A6CB", highlightthickness=0)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.ticket_frame, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.content_frame = tk.Frame(self.canvas, bg="#82A6CB")
        self.canvas.create_window(
            (120, 100), window=self.content_frame, anchor=tk.CENTER)

        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.canvas.yview)

        self.inner_frame = tk.Frame(self.canvas, bg="#82A6CB")
        self.canvas.create_window(
            (0, 0), window=self.inner_frame, anchor=tk.CENTER)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.content_frame.bind("<Configure>", lambda event,
                                canvas=self.canvas: self.on_frame_configure(canvas))

        self.ticket_labels = []
        self.edit_buttons = []
        self.delete_buttons = []

        self.update_ticket_info()
        self.update_datetime()

        self.master.configure(bg="#BDD8F1")
        self.master.geometry("1200x500")
        master.resizable(0, 0)
        photo = tk.PhotoImage(file='ikon.png')
        master.wm_iconphoto(False, photo)

    def toggle_gender_filters(self):
        if self.gender_filter_all.get():
            self.gender_filter_male.set(True)
            self.gender_filter_female.set(True)
        else:
            self.gender_filter_male.set(False)
            self.gender_filter_female.set(False)

    def toggle_service_filters(self):
        if self.service_filter_all.get():
            self.service_filter_piling.set(True)
            self.service_filter_mezoterapia.set(True)
            self.service_filter_plazmolifting.set(True)
            self.service_filter_botox.set(True)
            self.service_filter_biorevitalization.set(True)
            self.service_filter_cleaning.set(True)
        else:
            self.service_filter_piling.set(False)
            self.service_filter_mezoterapia.set(False)
            self.service_filter_plazmolifting.set(False)
            self.service_filter_botox.set(False)
            self.service_filter_biorevitalization.set(False)
            self.service_filter_cleaning.set(False)

    def clear_filters(self):
        self.gender_filter_male.set(False)
        self.gender_filter_female.set(False)
        self.gender_filter_all.set(True)
        self.service_filter_piling.set(False)
        self.service_filter_mezoterapia.set(False)
        self.service_filter_plazmolifting.set(False)
        self.service_filter_botox.set(False)
        self.service_filter_biorevitalization.set(False)
        self.service_filter_cleaning.set(False)
        self.service_filter_all.set(True)
        self.date_from_entry.delete(0, tk.END)
        self.date_to_entry.delete(0, tk.END)
        self.update_ticket_info()

    def sort_by_client(self):
        tickets = self.db.get_all_tickets()
        if self.sort_direction:
            tickets.sort(key=lambda x: x[2])  # сортировка по алфавиту
        else:
            tickets.sort(key=lambda x: x[2], reverse=True)
        self.display_tickets(tickets)
        self.sort_direction = not self.sort_direction  # сортировка в обратном направлении

    def sort_by_ticket(self):
        tickets = self.db.get_all_tickets()
        if self.sort_ticket_direction:
            tickets.sort(key=lambda x: x[1])  # сортировка по возрастанию
        else:
            tickets.sort(key=lambda x: x[1], reverse=True)
        self.display_tickets(tickets)
        self.sort_ticket_direction = not self.sort_ticket_direction    # сортировка по убыванию

    def filter_by_service(self):
        service = self.service_filter_combobox.get()
        if service == "Все":
            tickets = self.db.get_all_tickets()
        else:
            tickets = self.db.get_tickets_by_service(service)
        self.display_tickets(tickets)

    def update_ticket_info(self):
        self.remove_edit_buttons()
        self.remove_delete_buttons()

        for label in self.ticket_labels:
            label.destroy()

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tickets = self.db.get_all_tickets()

        for ticket in tickets:
            frame = tk.Frame(self.content_frame, bg="#82A6CB", padx=50)
            frame.pack(pady=1)
            ticket_info = f"Запись №: {ticket[1]}\nФИО клиента: {ticket[2]}\nПол: {ticket[3]}\nНомер телефона: {ticket[4]}\nУслуга: {ticket[5]}\nСтатус: {ticket[6]}\nДата/время создания записи: {ticket[7]}\n"
            if ticket[8]:
                ticket_info += f"Дата/время оказания услуги: {ticket[8]}"

            label = tk.Label(frame, font="Verdana 9 normal roman", text=ticket_info,
                             bg="#82A6CB", anchor=tk.W, justify=LEFT)
            label.grid(row=0, column=0, sticky=tk.W, padx=150, pady=10)

            edit_button = tk.Button(frame, font="Verdana 9 normal roman", text="Редактировать", bg="#3667A6",
                                    fg="white", command=lambda t=ticket[0]: self.edit_ticket(t))
            edit_button.grid(row=0, column=1, padx=2, pady=10)
            self.edit_buttons.append(edit_button)

            delete_button = tk.Button(frame, font="Verdana 9 normal roman", text="Удалить", bg="#3667A6",
                                      fg="white", command=lambda t=ticket[0]: self.delete_ticket(t))
            delete_button.grid(row=0, column=2, padx=10, pady=10)
            self.delete_buttons.append(delete_button)

            client_button = tk.Button(frame, font="Verdana 9 normal roman", text="Все записи клиента", bg="#214177",
                                      fg="white", command=lambda t=ticket[2]: self.open_client_window(t))
            client_button.grid(row=0, column=3, padx=25, pady=10)

        if tickets:
            self.label_ticket_info.config (text="Все записи",font="Verdana 10 bold roman", bg="#BDD8F1")
        else:
            self.label_ticket_info.config(
             font="Verdana 10 bold  roman", text="Нет созданных записей", bg="#BDD8F1")

    def open_client_window(self, client_name):
        client_window = tk.Toplevel(self.master)
        client_window.title("История записей")

        client_window_instance = ClientWindow(
            client_window, self, client_name, self.db)

    def remove_edit_buttons(self):
        for button in self.edit_buttons:
            button.destroy()
        self.edit_buttons = []

    def remove_delete_buttons(self):
        for button in self.delete_buttons:
            button.destroy()
        self.delete_buttons = []


    def _on_mousewheel(self, event):
        if self.canvas is not None:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_frame_configure(self, canvas):
        if canvas is not None:
            canvas.configure(scrollregion=canvas.bbox(tk.ALL), bg="#82A6CB")

    def create_ticket(self):
        current_datetime = datetime.datetime.now()
        latest_ticket = self.db.get_latest_ticket()
        if latest_ticket:
            ticket_number = int(latest_ticket[1]) + 1
        else:
            ticket_number = 1
        ticket_window = tk.Toplevel(self.master)
        ticket_window.title("Форма записи")
        ticket_form = TicketForm(
            ticket_window, self.db, self, creation_time=current_datetime, ticket_number=ticket_number)
        ticket_form.set_validate_phone_number_callback(self.validate_phone_number)
        ticket_form.set_validate_fio_callback(self.validate_fio)

        def create_ticket_callback(ticket_data):
            if self.validate_phone_number(ticket_data['phone_number']):
                self.db.create_ticket(ticket_data)
                self.update_ticket_info()
                ticket_window.destroy()
            else:
                tkinter.messagebox.showerror("Ошибка", "Неверный формат номера телефона")

        ticket_form.set_create_ticket_callback(create_ticket_callback)


    def validate_phone_number(self, phone_number):
        pattern = re.compile(r'^\+?\d{11,12}$')
        if not pattern.match(phone_number):
            tkinter.messagebox.showerror("Ошибка", "Неверный формат номера телефона")
            return False
        return True

    def edit_ticket(self, ticket_id):
        ticket = self.db.get_ticket_by_id(ticket_id)
        ticket_window = tk.Toplevel(self.master)
        ticket_window.title("Редактирование записи")
        ticket_edit_form = TicketEditForm(
            ticket_window, self.db, ticket_id, self)
        ticket_edit_form.set_validate_fio_callback(self.validate_fio)

        def update_client_info(client_fio, new_client_fio, new_client_phone):
            tickets = self.db.get_tickets_by_client_fio(client_fio)
            for ticket in tickets:
                self.db.update_ticket_client_info(
                    ticket[0], new_client_fio, new_client_phone)

        ticket_edit_form.set_update_client_info_callback(update_client_info)

    def validate_fio(self, fio):
        if any(char.isdigit() for char in fio):
            tkinter.messagebox.showerror("Ошибка", "ФИО клиента не должно содержать цифры")
            return False
        return True


    def delete_ticket(self, ticket_id):
        self.db.delete_ticket(ticket_id)
        self.update_ticket_info()

    def filter_by_gender(self):
        gender = self.gender_filter_combobox.get()
        if gender == "Все":
            tickets = self.db.get_all_tickets()
        else:
            tickets = self.db.get_tickets_by_gender(gender)
        self.display_tickets(tickets)

    def display_tickets(self, tickets):
        for label in self.ticket_labels:
            label.destroy()

        for button in self.edit_buttons:
            button.destroy()

        for button in self.delete_buttons:
            button.destroy()

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        for ticket in tickets:
            frame = tk.Frame(self.content_frame, bg="#82A6CB", padx=50)
            frame.pack(pady=1)
            ticket_info = f"Запись №: {ticket[1]}\nФИО клиента: {ticket[2]}\nПол: {ticket[3]}\nНомер телефона: {ticket[4]}\nУслуга: {ticket[5]}\nСтатус: {ticket[6]}\nДата/время создания записи: {ticket[7]}\n"
            if ticket[8]:
                ticket_info += f"Дата/время оказания услуги: {ticket[8]}"

            label = tk.Label(frame, font="Verdana 9 normal roman", text=ticket_info,
                             bg="#82A6CB", anchor=tk.W, justify=LEFT)
            label.grid(row=0, column=0, sticky=tk.W, padx=150,
                       pady=10) 

            edit_button = tk.Button(frame, font="Verdana 9 normal roman", text="Редактировать", bg="#3667A6",
                                    fg="white", command=lambda t=ticket[0]: self.edit_ticket(t))
            edit_button.grid(row=0, column=1, padx=2, pady=10)
            self.edit_buttons.append(edit_button)

            delete_button = tk.Button(frame, font="Verdana 9 normal roman", text="Удалить", bg="#3667A6",
                                      fg="white", command=lambda t=ticket[0]: self.delete_ticket(t))
            delete_button.grid(row=0, column=2, padx=10, pady=10)
            self.delete_buttons.append(delete_button)

            client_button = tk.Button(frame, font="Verdana 9 normal roman", text="Все записи клиента", bg="#214177",
                                      fg="white", command=lambda t=ticket[2]: self.open_client_window(t))
            client_button.grid(row=0, column=3, padx=25, pady=10)

        if tickets:
            self.label_ticket_info.config (text="Все записи",font="Verdana 10 bold roman", bg="#BDD8F1")
        else:
            self.label_ticket_info.config(
             font="Verdana 10 bold roman", text="Нет созданных записей", bg="#BDD8F1")

    def delete_all_tickets(self):
        if tkinter.messagebox.askyesno("Удалить все записи", "Вы уверены, что хотите удалить все записи?"):
            self.db.delete_all_tickets()
            self.update_ticket_info()

    def search_tickets(self):
        search_query = self.search_entry.get()
        if search_query:
            tickets = self.db.search_tickets(search_query)
            self.display_search_results(tickets)
            self.search_history.append(search_query)
        else:
            self.update_ticket_info()

    def show_search_history(self):
        history_window = tk.Toplevel(self.master)
        history_window.title("История поиска")

        history_frame = tk.Frame(history_window, bg="#82A6CB")
        history_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(
            history_frame, orient=tk.VERTICAL, bg="#82A6CB", highlightthickness=0)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas = tk.Canvas(history_frame, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        content_frame = tk.Frame(canvas, bg="#82A6CB")
        canvas.create_window(
            (120, 100), window=content_frame, anchor=tk.CENTER)

        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=canvas.yview)

        canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        content_frame.bind("<Configure>", lambda event,
                           canvas=canvas: self.on_frame_configure(canvas))

        for i, query in enumerate(self.search_history):
            label = tk.Label(
                content_frame, font="Verdana 9 normal roman", text=f"{i+1}. {query}", bg="#82A6CB", anchor=tk.CENTER, justify=LEFT)
            label.pack(pady=1)

        history1_frame = tk.Frame(history_window, bg="#82A6CB")
        history1_frame.pack(fill=tk.BOTH, expand=True)

        clear_button = tk.Button(history1_frame, font="Verdana 10 bold roman", text="Очистить",
                                 command=self.clear_search_history, bg="#3667A6", fg="white")
        clear_button.pack(side=tk.RIGHT, padx=5)

        history_window.geometry("400x300")
        history_window.resizable(0, 0)
        photo = tk.PhotoImage(file='ikon.png')
        self.master.wm_iconphoto(False, photo)

    def clear_search_history(self):
        self.search_history = []
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.display_search_results([])

    def filter_by_date(self):
        date_from = self.date_from_entry.get()
        # фильтр по Дате создания записи
        date_to = self.date_to_entry.get()
        try:
            datetime.datetime.strptime(date_from, '%d.%m.%Y')
            datetime.datetime.strptime(date_to, '%d.%m.%Y')
        except ValueError:
            tk.messagebox.showerror(
                "Ошибка", "Дата должна быть в формате ЧЧ-ММ-ГГГГ")
            return

        if date_from and date_to:
            tickets = self.db.get_tickets_by_date_range(date_from, date_to)
        else:
            tickets = self.db.get_all_tickets()
        self.display_tickets(tickets)

    def apply_filters(self):
        tickets = self.db.get_all_tickets()
        genders = []
        if self.gender_filter_male.get():                  # фильтр по Полу
            genders.append('Мужской')
        if self.gender_filter_female.get():
            genders.append('Женский')
        if genders:
            tickets = [t for t in tickets if t[3] in genders]

        services = []
        if self.service_filter_piling.get():
            services.append('Пилинг')                      # фильтр по Улугам
        if self.service_filter_mezoterapia.get():
            services.append('Мезотерапия')
        if self.service_filter_plazmolifting.get():
            services.append('Плазмолифтинг')
        if self.service_filter_botox.get():
            services.append('Ботулинотерапия')
        if self.service_filter_biorevitalization.get():
            services.append('Биоревитализация')
        if self.service_filter_cleaning.get():
            services.append('Чистка лица')
        if services:
            tickets = [t for t in tickets if t[5] in services]

        date_from = self.date_from_entry.get()
        date_to = self.date_to_entry.get()
        if date_from and date_to:                             # фильтр по дате создания записи
            try:
                date_from = datetime.datetime.strptime(date_from, '%d.%m.%Y')
                date_to = datetime.datetime.strptime(date_to, '%d.%m.%Y')
                tickets = [t for t in tickets if date_from <= datetime.datetime.strptime(
                    t[7], '%d.%m.%Y %H:%M:%S') <= date_to]
            except ValueError:
                tk.messagebox.showerror(
                    "Ошибка", "Дата должна быть в формате ЧЧ.ММ.ГГГГ")

        self.display_tickets(tickets)

    def display_search_results(self, tickets):
        for label in self.ticket_labels:
            label.destroy()

        for button in self.edit_buttons:
            button.destroy()

        for button in self.delete_buttons:
            button.destroy()

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        for ticket in tickets:
            frame = tk.Frame(self.content_frame, bg="#82A6CB", padx=50)
            frame.pack(pady=1)
            ticket_info = f"Запись №: {ticket[1]}\nФИО клиента: {ticket[2]}\nПол: {ticket[3]}\nНомер телефона: {ticket[4]}\nУслуга: {ticket[5]}\nСтатус: {ticket[6]}\nДата/время создания записи: {ticket[7]}\n"
            if ticket[8]:
                ticket_info += f"Дата/время оказания услуги: {ticket[8]}"

            label = tk.Label(frame, font="Verdana 9 normal roman", text=ticket_info,
                             bg="#82A6CB", anchor=tk.W, justify=LEFT)
            label.grid(row=0, column=0, sticky=tk.W, padx=150, pady=10) 

            edit_button = tk.Button(frame, font="Verdana 9 normal roman", text="Редактировать", bg="#3667A6",
                                    fg="white", command=lambda t=ticket[0]: self.edit_ticket(t))
            edit_button.grid(row=0, column=1, padx=2, pady=10)
            self.edit_buttons.append(edit_button)

            delete_button = tk.Button(frame, font="Verdana 9 normal roman", text="Удалить", bg="#3667A6",
                                      fg="white", command=lambda t=ticket[0]: self.delete_ticket(t))
            delete_button.grid(row=0, column=2, padx=10, pady=10)
            self.delete_buttons.append(delete_button)

            client_button = tk.Button(frame, font="Verdana 9 normal roman", text="Все записи клиента", bg="#214177",
                                      fg="white", command=lambda t=ticket[2]: self.open_client_window(t))
            client_button.grid(row=0, column=3, padx=25, pady=10)

        if tickets:
            self.label_ticket_info.config(
             font="Verdana 10 bold  roman", text="Результаты поиска", bg="#BDD8F1")
        else:
            self.label_ticket_info.config(
             font="Verdana 10 bold  roman", text="Нет результатов поиска", bg="#BDD8F1")

    def update_datetime(self):
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config (text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def logout(self):
        self.master.destroy()
        self.root.deiconify()
