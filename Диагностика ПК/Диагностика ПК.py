import os
import subprocess
import wmi
import psutil
import platform
import tkinter as tk
import winreg
from tkinter import ttk
from tkinter import filedialog
import sqlite3
from tkinter import messagebox
import win32evtlog

def scan_system_log(text_box):
    handle = win32evtlog.OpenEventLog(None, "System")
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events = win32evtlog.ReadEventLog(handle, flags, 0)
    log_data = ""
    for event in events:
        log_data += str(event.StringInserts) + "\n"
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, log_data)
    return log_data

def view_installed_programs(text_box):
    programs = []
    for root, dirs, files in os.walk('C:\\Program Files'):
        for file in files:
            if file.endswith('.exe'):
                programs.append(os.path.join(root, file))
    for root, dirs, files in os.walk('C:\\Program Files (x86)'):
        for file in files:
            if file.endswith('.exe'):
                programs.append(os.path.join(root, file))

    text_box.delete(1.0, tk.END)
    for program in programs:
        text_box.insert(tk.END, program + "\n")

    return programs


def display_results(results, text_box):
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, "IP Address\t\tMAC Address\n")
    text_box.insert(tk.END, "-----------------------------------------\n")
    for result in results:
        text_box.insert(tk.END, result["ip"] + "\t\t" + result["mac"] + "\n")

def diagnose_system(text_box):
    c = wmi.WMI()
    my_system = c.Win32_ComputerSystem()[0]

    system_info = f"Manufacturer: {my_system.Manufacturer}\n"
    system_info += f"Model: {my_system.Model}\n"
    system_info += f"Name: {my_system.Name}\n"
    system_info += f"NumberOfProcessors: {my_system.NumberOfProcessors}\n"
    system_info += f"SystemType: {my_system.SystemType}\n"
    system_info += f"SystemFamily: {my_system.SystemFamily}\n"

    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, system_info)

def diagnose_memory(text_box):
    memory_info = str(psutil.virtual_memory()) + "\n\n"
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, memory_info)

def diagnose_platform(text_box):
    platform_info = f"System: {platform.system()}\n"
    platform_info += f"Node Name: {platform.node()}\n"
    platform_info += f"Release: {platform.release()}\n"
    platform_info += f"Version: {platform.version()}\n"
    platform_info += f"Machine: {platform.machine()}\n"
    platform_info += f"Processor: {platform.processor()}\n"

    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, platform_info)

def diagnose_system_info(text_box):
    system_info_output = subprocess.check_output(["chcp", "65001"], shell=True).decode("utf-8")
    system_info_output += subprocess.check_output(["systeminfo"], shell=True).decode("utf-8")

    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, system_info_output)


def scan_registry(text_box):
    reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE")
    subkeys = []
    for i in range(winreg.QueryInfoKey(reg_key)[0]):
        subkey_name = winreg.EnumKey(reg_key, i)
        subkeys.append(subkey_name)
    text_box.delete(1.0, tk.END)
    for subkey in subkeys:
        text_box.insert(tk.END, f"Subkey: {subkey}\n")
        subkey_key = winreg.OpenKey(reg_key, subkey)
        values = []
        for i in range(winreg.QueryInfoKey(subkey_key)[1]):
            value_name, value_data, _ = winreg.EnumValue(subkey_key, i)
            values.append(f"{value_name}: {value_data}")
        text_box.insert(tk.END, "\n".join(values) + "\n\n")

    return subkeys

def save_system():
    file = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if file is None:
        return
    file.write(system_text_box.get(1.0, tk.END))
    file.close()

def save_system_info():
    file = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if file is None:
        return
    file.write(system_info_text_box.get(1.0, tk.END))
    file.close()

def save_memory_info():
    file = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if file is None:
        return
    file.write(memory_text_box.get(1.0, tk.END))
    file.close()

def save_platform_info():
    file = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if file is None:
        return
    file.write(platform_text_box.get(1.0, tk.END))
    file.close()
    

def save_registry_info():
    file = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if file is None:
        return
    file.write(platform_text_box.get(1.0, tk.END))
    file.close()

def save_system_log_info():
    file = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if file is None:
        return
    file.write(system_log_text_box.get(1.0, tk.END))
    file.close()


# def save_all_info():
#     file = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
#     if file is None:
#         return
#     file.write(system_text_box.get(1.0, tk.END) + "\n\n")
#     file.writet(tk.END, "\n\n")
#     file.write(memory_text_box.get(1.0, tk.END) + "\n\n")
#     file.writet(tk.END, "\n\n")
#     file.write(platform_text_box.get(1.0, tk.END) + "\n\n")
#     file.writet(tk.END, "\n\n")
#     file.write(system_info_text_box.get(1.0, tk.END) + "\n\n")
#     file.writet(tk.END, "\n\n")
#     file.write(system_log_text_box.get(1.0, tk.END) + "\n\n")
#     file.writet(tk.END, "\n\n")
#     file.write(install_text_box.get(1.0, tk.END) + "\n\n")
#     file.writet(tk.END, "\n\n")
#     file.write(registry_text_box.get(1.0, tk.END) + "\n\n")
#     file.close()


def scan_all():
    diagnose_system(system_text_box)
    system_text_box_data = system_text_box.get(1.0, tk.END)
    diagnose_memory(memory_text_box)
    memory_text_box_data = memory_text_box.get(1.0, tk.END)
    diagnose_platform(platform_text_box)
    platform_text_box_data = platform_text_box.get(1.0, tk.END)
    diagnose_system_info(system_info_text_box)
    system_info_text_box_data = system_info_text_box.get(1.0, tk.END)
    log_data=scan_system_log(system_log_text_box)
    system_log_text_box_data=system_log_text_box.get(1.0, tk.END)
    installed_programs = view_installed_programs(install_text_box)
    install_text_box_data = install_text_box.get(1.0, tk.END)
    subkey = scan_registry(registry_text_box)
    registry_text_box_data = registry_text_box.get(1.0, tk.END)
   


def save_to_database(system_text_box_data, memory_text_box_data, platform_text_box_data, system_info_text_box_data, system_log_text_box_data, install_text_box_data, registry_text_box_data):
    print("system_text_box_data:", system_text_box_data)
    print("memory_text_box_data:", memory_text_box_data)
    print("platform_text_box_data:", platform_text_box_data)
    print("system_info_text_box_data:", system_info_text_box_data)
    print("system_log_text_box_data:", system_log_text_box_data)
    print("install_text_box_data:", install_text_box_data)
    print("registry_text_box_data:", registry_text_box_data)

    try:
        conn = sqlite3.connect('diagnostic_history.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS diagnostic_history
              (system_info text, memory_info text, platform_info text, system_info_all text, system_log_info text,  install_info text, registry_info text)''')
        c.execute("INSERT INTO diagnostic_history VALUES (?,?,?,?,?,?,?)",
                  (system_text_box_data, memory_text_box_data,
                   platform_text_box_data, system_info_text_box_data, system_log_text_box_data, install_text_box_data, registry_text_box_data))
        conn.commit()  # Add this line to commit the changes
        conn.close()
        messagebox.showinfo("Success", "Ваши данные успешно сохранены!")  # Display a messagebox with a success message


    except sqlite3.Error as e:
        print(f"Error: {e}")


def view_history():
    conn = sqlite3.connect('diagnostic_history.db')
    c = conn.cursor()
    c.execute("SELECT * FROM diagnostic_history")
    rows = c.fetchall()
    conn.close()
    history_window = tk.Toplevel(root)
    history_window.geometry("900x500")
    history_window.title("Diagnostic History")
    history_window.configure(bg='#d2a7f5')  # set background color to purple
    canvas = tk.Canvas(history_window, bg='#d2a7f5')  # set canvas background color to purple
    frame = tk.Frame(canvas, bg='#d2a7f5')  # set frame background color to purple
    canvas.create_window((0, 0), window=frame, anchor='nw')
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(history_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.configure(xscrollcommand=scrollbar.set)
    for i, row in enumerate(rows):
        label = tk.Label(frame, text=f"Record {i+1}:", bg='#d2a7f5', fg='white', font="Verdana 10 bold italic" )  # set label background color to purple and text color to white
        label.grid(row=i, column=0, padx=10, pady=10)
        text_box = tk.Text(frame, width=95, height=20, bg='white')  # set text box background color to purple and text color to white
        text_box.grid(row=i, column=1, padx=10, pady=10)
        text_box.insert(tk.END, f"System Info:\n{row[0]}\n\n")
        text_box.insert(tk.END, "\n\n")  # add an empty line between records
        text_box.insert(tk.END, f"Memory Info:\n{row[1]}\n\n")
        text_box.insert(tk.END, "\n\n")  # add an empty line between records
        text_box.insert(tk.END, f"Platform Info:\n{row[2]}\n\n")
        text_box.insert(tk.END, "\n\n")  # add an empty line between records
        text_box.insert(tk.END, f"System Info All:\n{row[3]}\n\n")
        text_box.insert(tk.END, "\n\n")  # add an empty line between records
        text_box.insert(tk.END, f"System log:\n{row[4]}\n\n")
        text_box.insert(tk.END, "\n\n")  # add an empty line between records
        text_box.insert(tk.END, f"Install app:\n{row[5]}\n\n")
        text_box.insert(tk.END, "\n\n")  # add an empty line between records
        text_box.insert(tk.END, f"Registry:\n{row[6]}\n\n")
        text_box.insert(tk.END, "\n\n")  # add an empty line between records
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


def save_system_info_all():
    file = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if file is None:
        return
    file.write(system_text_box.get(1.0, tk.END) + "\n\n")
    file.write(memory_text_box.get(1.0, tk.END) + "\n\n")
    file.write(platform_text_box.get(1.0, tk.END) + "\n\n")
    file.write(system_info_text_box.get(1.0, tk.END))
    file.close()


def save_installed_programs():
    file = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if file is None:
        return
    programs = []
    for root, dirs, files in os.walk('C:\\Program Files'):
        for file in files:
            if file.endswith('.exe'):
                programs.append(os.path.join(root, file))
    for root, dirs, files in os.walk('C:\\Program Files (x86)'):
        for file in files:
            if file.endswith('.exe'):
                programs.append(os.path.join(root, file))
    file.write('\n'.join(programs))
    file.close()


def clear_database():
    result = messagebox.askyesno("Подтверждение", "Вы действительно хотите очистить историю?")
    if result:
        conn = sqlite3.connect('diagnostic_history.db')
        c = conn.cursor()
        c.execute("DELETE FROM diagnostic_history")
        conn.commit()
        conn.close()
        messagebox.showinfo("Успешно", "История успешно очищена!")


lang = "ru"  # Initialize the language to Russian
def change_language():
    global lang
    if lang == "ru":
        lang = "en"
        button_change_language.config(text="Russian")
        button_scan_all.config(text="Scan All")
        button_save_to_database.config(text="Save to Database")
        notebook.tab(system_tab, text="System")
        notebook.tab(memory_tab, text="Memory")
        notebook.tab(platform_tab, text="Platform")
        notebook.tab(system_info_tab, text="System Info")
        notebook.tab(system_log_tab, text="System log")
        notebook.tab(install_app, text="Install app")
        notebook.tab(registry_tab, text="Registry")
        button_diagnose_system.config(text="Diagnose System")
        button_scan_system_log.config(text="Scan System Log")
        button_view_installed_programs.config(text="View Installed Programs")
        button_diagnose_memory.config(text="Diagnose Memory")
        button_diagnose_platform.config(text="Diagnose Platform")
        button_diagnose_system_info.config(text="Diagnose System Info")
        button_scan_registry.config(text="Diagnose Registry")
        button_save_system.config(text="Save System")
        button_save_installed_programs.config(text="Save Installed Programs")
        button_save_system_info.config(text="Save System Info")
        button_save_memory.config(text="Save Memory")
        button_save_platform.config(text="Save Platform")
        button_save_registry.config(text="Save Registry")
        button_clear_database.config(text="Clear Database")
        button_view_history.config(text="View History")
        button_save_system_log.config(text="Save system log")
    else:
        lang = "ru"
        button_change_language.config(text="English")
        button_scan_all.config(text="Сканировать все")
        button_save_to_database.config(text="Сохранить в бд")
        notebook.tab(system_tab, text="Система")
        notebook.tab(memory_tab, text="Память")
        notebook.tab(platform_tab, text="Платформа")
        notebook.tab(system_info_tab, text="Инфо о системе")
        notebook.tab(system_log_tab, text="Системный журнал")
        notebook.tab(install_app, text="Установленные приложения")
        notebook.tab(registry_tab, text="Реестр")
        button_diagnose_system.config(text="Диагностика системы")
        button_scan_system_log.config(text="Сканирование системного журнала")
        button_view_installed_programs.config(text="Просмотр установленных программ")
        button_diagnose_memory.config(text="Диагностика памяти")
        button_diagnose_platform.config(text="Диагностика платформы")
        button_diagnose_system_info.config(text="Диагностика системной информации")
        button_scan_registry.config(text="Диагностика реестра")
        button_save_system.config(text="Сохранить систему")
        button_save_installed_programs.config(text="Сохранить установленные программы")
        button_save_system_info.config(text="Сохранить системную информацию")
        button_save_memory.config(text="Сохранить память")
        button_save_platform.config(text="Сохранить платформу")
        button_save_registry.config(text="Сохранить реестр")
        button_clear_database.config(text="Очистить бд")
        button_view_history.config(text="Просмотр истории")
        button_save_system_log.config(text="Сохранить системный журнал")


# Создание GUI
root = tk.Tk()
root.title("PC Scanner and Diagnostic")
root.configure(background='#f0e2fc')


notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)


# Создание кнопок
button_scan_all = tk.Button(root, bg="#aa59ec",fg="white", font="Verdana 10 bold italic", text="Scan All", command=lambda: scan_all())

# button_save_all_info = tk.Button(root, bg="#aa59ec",fg="white", font="Verdana 10 bold italic", text="Save All info", command=lambda: save_all_info())
button_save_to_database = tk.Button(root, bg="#aa59ec", font="Verdana 10 bold italic",fg="white", text="Save to Database", command=lambda: save_to_database(system_text_box.get(1.0, tk.END), memory_text_box.get(1.0, tk.END), platform_text_box.get(1.0, tk.END), system_info_text_box.get(1.0, tk.END), system_log_text_box.get(1.0, tk.END),install_text_box.get(1.0, tk.END), registry_text_box.get(1.0, tk.END)))

button_view_history = tk.Button(root, bg="#aa59ec", font="Verdana 10 bold italic",fg="white",text="View History", command=view_history)

button_clear_database = tk.Button(root, bg="#aa59ec", font="Verdana 10 bold italic",fg="white",text="Clear Database", command=clear_database)


button_change_language = tk.Button(root, text="Russian", command=change_language)
button_change_language.pack(anchor="center")


button_frame = tk.Frame(root, bg='#f0e2fc')
button_frame.pack(pady=10, fill=tk.X)
button_scan_all.pack(side=tk.LEFT, padx=7, pady=(0,10))
button_save_to_database.pack(side=tk.LEFT, padx=7, pady=(0,10))
button_view_history.pack(side=tk.LEFT, padx=7, pady=(0,10))
button_clear_database.pack(side=tk.LEFT, padx=7, pady=(0,10))
# Создание горизонтального фрейма
button_frame = tk.Frame(root, bg='#f0e2fc')  #нижняя часть, где отображалась белая полоса

# Размещение кнопок в горизонтальном фрейме
button_frame.pack(pady=10, fill=tk.X)
button_scan_all.pack(side=tk.LEFT)
button_save_to_database.pack(side=tk.RIGHT)


style = ttk.Style()
style.theme_create( "meow", parent="alt", settings={
        "TNotebook": {"configure": {"background": "#f0e2fc","tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": "#d2a7f5" },
            "map":       {"background": [("selected", "#aa59ec")],
                          "foreground": [("selected", "white")],
                          "expand": [("selected", [2, 2, 2, 2])] } } } )
style.theme_use("meow")
note = ttk.Notebook(root)
style = ttk.Style()
style.configure('Yellow.TFrame', background='#d2a7f5')
system_tab = ttk.Frame(notebook, style='Yellow.TFrame')
memory_tab = ttk.Frame(notebook, style='Yellow.TFrame')
platform_tab = ttk.Frame(notebook, style='Yellow.TFrame')
system_info_tab = ttk.Frame(notebook, style='Yellow.TFrame')
system_log_tab = ttk.Frame(notebook, style='Yellow.TFrame')
install_app = ttk.Frame(notebook, style='Yellow.TFrame')
registry_tab = ttk.Frame(notebook, style='Yellow.TFrame')


notebook.add(system_tab, text="System")
notebook.add(memory_tab, text="Memory")
notebook.add(platform_tab, text="Platform")
notebook.add(system_info_tab, text="System Info")
notebook.add(system_log_tab, text="System log")
notebook.add(install_app, text="Install app")
notebook.add(registry_tab, text="Registry")


system_text_box = tk.Text(system_tab, bg="white" ,width=95, height=30)
system_text_box.pack()

install_text_box = tk.Text(install_app, bg="white", width=95, height=30)
install_text_box.pack()

registry_text_box = tk.Text(registry_tab, bg="white", width=95, height=30)
registry_text_box.pack()

memory_text_box = tk.Text(memory_tab, bg="white", width=95, height=30)
memory_text_box.pack()

platform_text_box = tk.Text(platform_tab, bg="white", width=95, height=30)
platform_text_box.pack()

system_info_text_box = tk.Text(system_info_tab, bg="white", width=95, height=30)
system_info_text_box.pack()

system_log_text_box = tk.Text(system_log_tab, bg="white", width=95, height=30)
system_log_text_box.pack()

button_diagnose_system = tk.Button(system_tab, bg="#aa59ec", font="Verdana 10 bold italic", fg="white", text="Diagnose System", command=lambda: diagnose_system(system_text_box))
button_diagnose_system.pack()

button_scan_system_log = tk.Button(system_log_tab,bg="#aa59ec", font="Verdana 10 bold italic",fg="white", text="Scan System Log", command=lambda: scan_system_log(system_log_text_box))
button_scan_system_log.pack()

button_view_installed_programs = tk.Button(install_app, bg="#aa59ec", font="Verdana 10 bold italic",fg="white",text="View Installed Programs", command=lambda: view_installed_programs(install_text_box))
button_view_installed_programs.pack()

button_diagnose_memory = tk.Button(memory_tab,bg="#aa59ec",fg="white", font="Verdana 10 bold italic", text="Diagnose Memory", command=lambda: diagnose_memory(memory_text_box))
button_diagnose_memory.pack()

button_diagnose_platform = tk.Button(platform_tab, bg="#aa59ec",fg="white", font="Verdana 10 bold italic",text="Diagnose platform", command=lambda: diagnose_platform(platform_text_box))
button_diagnose_platform.pack()

button_diagnose_system_info = tk.Button(system_info_tab, bg="#aa59ec",fg="white", font="Verdana 10 bold italic",text="Diagnose System Info", command=lambda: diagnose_system_info(system_info_text_box))
button_diagnose_system_info.pack()

button_scan_registry = tk.Button(registry_tab, bg="#aa59ec",fg="white", font="Verdana 10 bold italic",text="Diagnose Registry", command=lambda: scan_registry(registry_text_box))
button_scan_registry.pack()



button_save_system = tk.Button(system_tab, bg="#aa59ec",fg="white", font="Verdana 10 bold italic",text="Save system", command= save_system)
button_save_system.pack()

button_save_installed_programs = tk.Button(install_app, bg="#aa59ec",fg="white", font="Verdana 10 bold italic",text="Save Installed Programs", command=save_installed_programs)
button_save_installed_programs.pack()

button_save_system_info = tk.Button(system_info_tab,bg="#aa59ec",fg="white", font="Verdana 10 bold italic", text="Save system info", command= save_system_info)
button_save_system_info.pack()

button_save_memory = tk.Button(memory_tab, bg="#aa59ec",fg="white", font="Verdana 10 bold italic",text="Save Memory", command=save_memory_info)
button_save_memory.pack()

button_save_platform = tk.Button(platform_tab,bg="#aa59ec",fg="white", font="Verdana 10 bold italic", text="Save platform", command= save_platform_info)
button_save_platform.pack()

button_save_registry = tk.Button(registry_tab, bg="#aa59ec",fg="white", font="Verdana 10 bold italic",text="Save registry", command= save_registry_info)
button_save_registry.pack()

button_save_system_log = tk.Button(system_log_tab, bg="#aa59ec",fg="white", font="Verdana 10 bold italic",text="Save system log", command= save_system_log_info)
button_save_system_log.pack()

root.mainloop()