import tkinter as tk
from tkinter import messagebox
from database import Database
from application_window import ApplicationWindow
from datetime import datetime

class AuthWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Авторизация")
        self.db = Database("users.db")  # Создаем экземпляр базы данных

        self.master.configure(bg="#82A6CB")
        master.geometry('440x350')
        master.resizable(0, 0)
        #master.eval('tk::PlaceWindow. center')

        photo = tk.PhotoImage(file='ikon.png')
        master.wm_iconphoto(False, photo)

        self.frame = tk.Frame(master, bg="#82A6CB")
        self.frame.pack(fill="both", expand=True)

        self.label_name = tk.Label(self.frame, font="Salwey 11 bold roman", text="Косметологический салон", bg="#82A6CB", fg="white")
        self.label_name.pack(pady=(7,0))

        self.label_datetime = tk.Label(self.frame, text="", bg="#82A6CB", font="Verdana 9 normal roman")
        self.label_datetime.pack(pady=10)

        self.label_username = tk.Label(self.frame, text="Имя пользователя:", bg="#82A6CB", font="Verdana 10 normal roman")
        self.label_username.pack(pady=(7,0))

        self.entry_username = tk.Entry(self.frame)
        self.entry_username.pack(pady=7)

        self.label_password = tk.Label(self.frame, text="Пароль:", bg="#82A6CB", font="Verdana 10 normal roman")
        self.label_password.pack()

        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.pack()

        self.show_password_var = tk.BooleanVar()

        self.checkbox_show_password = tk.Checkbutton(self.frame, text="Показать пароль", font="Verdana 8 normal roman", variable=self.show_password_var, command=self.toggle_password_visibility, bg="#82A6CB")
        self.checkbox_show_password.pack(pady=5)

        self.btn_login = tk.Button(self.frame, text="Войти", font="Verdana 10 normal roman", command=self.login, bg="#214177", fg="white")
        self.btn_login.pack()

        self.my_image = tk.PhotoImage(file='how1.png')
        self.canvas = tk.Canvas(self.master, width=220, height=130)
        self.canvas.pack()
        self.canvas_image = self.canvas.create_image(0, 0, anchor="nw", image=self.my_image)

        self.update_datetime()  # Начинаем обновление времени

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.db.check_credentials(username, password):
            self.master.withdraw()
            if username == "1":
                self.open_application_window(username)
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def open_application_window(self, username):
        application_window = tk.Toplevel(self.master)
        application_window.title("Главное окно приложения")

        ApplicationWindow(application_window, self.db, username, self.master)
        tickets = self.db.get_all_tickets()

    def update_datetime(self):
        current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def show(self):
        self.master.deiconify()

def main():
    root = tk.Tk()
    auth_window = AuthWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()