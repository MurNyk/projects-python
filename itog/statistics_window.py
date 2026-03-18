import tkinter as tk
from tkinter import ttk
import datetime
from collections import Counter


def create_statistics_window(db):
    statistics_window = tk.Toplevel()
    statistics_window.title("Статистика")

    # Метка для отображения даты и времени
    label_datetime = tk.Label(
        statistics_window, text="", font="Verdana 10 normal roman", bg="#D5F1E1")
    label_datetime.pack()

    # Функция для обновления даты и времени в реальном времени
    def update_datetime():
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        label_datetime.config(text=current_datetime,
                              font="Verdana 11 normal roman")
        # Обновляем каждую секунду
        statistics_window.after(1000, update_datetime)
    update_datetime()

    # Таблица для отображения заявок
    tree_tickets = ttk.Treeview(statistics_window)
    tree_tickets["columns"] = ("ID", "Оборудование", "Тип неисправности", "Описание",
                               "Клиент", "Статус", "Создание", "Выполнение", "Время выполнения")
    tree_tickets.heading("#0", text="№")
    tree_tickets.column("#0", anchor="w", width=50)
    for col in tree_tickets["columns"]:
        tree_tickets.heading(col, text=col)
        tree_tickets.column(col, anchor="w")
    tree_tickets.pack(expand=True, fill="both")

    # Получение всех заявок из базы данных
    tickets = db.get_all_tickets()

    if tickets:
        for ticket in tickets:
            # Рассчитываем время выполнения заявки, если оно указано
            if ticket[6] == "Выполнено" and ticket[7] and ticket[8]:
                creation_time = datetime.datetime.strptime(
                    ticket[7], "%Y-%m-%d %H:%M:%S")
                completion_time = datetime.datetime.strptime(
                    ticket[8], "%Y-%m-%d %H:%M:%S")
                execution_time = completion_time - creation_time
                execution_time_str = str(execution_time)
            else:
                execution_time_str = "Не указано"

            tree_tickets.insert("", "end", text=ticket[1], values=tuple(
                ticket[1:]) + (execution_time_str,))
    else:
        tree_tickets.insert("", "end", text="Нет данных", values=[""]*9)

    # Таблица для отображения типов неисправностей и количества выполненных заявок для каждого типа
    tree_fault_types = ttk.Treeview(statistics_window)
    tree_fault_types["columns"] = (
        "Тип неисправности", "Количество выполненных заявок")
    tree_fault_types.heading("#0", text="№")
    tree_fault_types.column("#0", anchor="w", width=50)
    for col in tree_fault_types["columns"]:
        tree_fault_types.heading(col, text=col)
        tree_fault_types.column(col, anchor="w")
    tree_fault_types.pack(expand=True, fill="both")

    # Получение всех заявок из базы данных
    tickets = db.get_all_tickets()

    if tickets:
        # Счетчик для подсчета количества выполненных заявок для каждого типа неисправности
        fault_type_counter = Counter()

        for ticket in tickets:
            if ticket[6] == "Выполнено":
                fault_type_counter[ticket[3]] += 1

        # Заполнение таблицы с типами неисправностей и количеством выполненных заявок
        row_num = 1
        for fault_type, count in fault_type_counter.items():
            tree_fault_types.insert(
                "", "end", text=row_num, values=(fault_type, count))
            row_num += 1
    else:
        tree_fault_types.insert("", "end", text="Нет данных", values=[""]*2)
