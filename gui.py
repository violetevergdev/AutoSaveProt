import tkinter as tk
from tkinter import ttk
import datetime
from main import main
from tkcalendar import DateEntry

operation_aliases = {
    "Индексация": "инд",
    "80 лет": " 80 лет",
    "Перерасчет Ижд. (ФБР)": " ФБР)",
    "Анализ работодателей": "Анализ данных ",
    "Перерасчет ПРБЗ": "(ПРБЗ)",
    "Лётчики": "Лёт",
    "Шахтёры": "Шах",
    "индексация ЕДВ": "индексация ЕДВ"
}

operations = [
    "Индексация",
    "80 лет",
    "Перерасчет Ижд. (ФБР)",
    "Анализ работодателей",
    "Перерасчет ПРБЗ",
    "Лётчики",
    "Шахтёры",
    "индексация ЕДВ"
]

def change_server(reg):
    def close():
        server_window.result = server_combobox.get()
        server_window.destroy()
        return server_window

    server_window = tk.Toplevel(root)
    x = (server_window.winfo_screenwidth() - server_window.winfo_reqwidth()) / 2
    y = (server_window.winfo_screenheight() - server_window.winfo_reqheight()) / 2
    server_window.wm_geometry("+%d+%d" % (x, y))

    server_label = tk.Label(server_window, text="Сервер:")
    server_label.pack()

    if reg == "Москва":
        servers = ["179", "183", "184"]
    elif reg == "Область":
        servers = ["209", "206", "210"]

    server_combobox = ttk.Combobox(server_window, values=servers)
    server_combobox.pack()

    server_window.result = None

    ok_btn = tk.Button(server_window, text="Ok", command=close)
    ok_btn.pack(side=tk.RIGHT)

    return server_window

def run_program():
    login = login_entry.get()
    password = password_entry.get()

    date_str = start_date_calendar.get()
    month, day, year_part = date_str.split('/')
    year = int(year_part) + 2000
    start_date = datetime.datetime.strptime(str(day) + "." + str(month) + "." + str(year), '%d.%m.%Y').date()
    end_date = start_date + datetime.timedelta(days=1)

    operation_type_selected = operation_type_combobox.get()
    operation_type = operation_aliases[operation_type_selected]

    reg = selected_reg.get()

    server_window = change_server(reg)
    root.wait_window(server_window)
    server = server_window.result

    main(login, password, start_date, end_date, operation_type, reg, server)


root = tk.Tk()
root.geometry('400x370')
root.resizable(False, False)
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.wm_geometry("+%d+%d" % (x, y))
root.title("Auto Save Prot")

# Создание фреймов для разделения интерфейса
title_frame = tk.Frame(root)
title_frame.pack(pady=5)

login_frame = tk.Frame(root)
login_frame.pack(pady=15)

settings_frame = tk.Frame(root)
settings_frame.pack(pady=15)

buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=5)

# Заголовок
title = tk.Label(title_frame, text="Автоматическая выгрузка протоколов", font=40)
title.pack()

login_label = tk.Label(login_frame, text="Логин от НВП:")
login_label.pack()
login_entry = tk.Entry(login_frame)
login_entry.pack()

password_label = tk.Label(login_frame, text="Пароль:")
password_label.pack()
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack()

start_date_label = tk.Label(settings_frame, text="Дата начала операции:")
start_date_label.pack(pady=2)
start_date_calendar = DateEntry(settings_frame)
start_date_calendar.pack(pady=5)

operation_type_frame = tk.Label(settings_frame, text="Тип операции:")
operation_type_frame.pack(pady=2)
operation_type_combobox = ttk.Combobox(settings_frame, values=operations)
operation_type_combobox.pack(pady=5)

selected_reg = tk.StringVar()
moscow_radio = tk.Radiobutton(settings_frame, text="Москва", variable=selected_reg, value="Москва")
moscow_radio.pack(side=tk.LEFT, padx=5)
region_radio = tk.Radiobutton(settings_frame, text="Область", variable=selected_reg, value="Область")
region_radio.pack(side=tk.LEFT, padx=5)

run_button = tk.Button(buttons_frame, text="Начать выгрузку", command=run_program)
run_button.pack()

root.mainloop()
