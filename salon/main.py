import tkinter as tk
from auth_window import AuthWindow


def main():   
    root = tk.Tk()
    auth_window = AuthWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
