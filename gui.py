import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel, showerror
import datetime
from main import main
from tkcalendar import DateEntry
import json
import os

operation_aliases = {
    "Индексация": "инд",
    "80 лет": " 80 лет",
    "Перерасчет Ижд. (ФБР)": " ФБР)",
    "Анализ работодателей": "Анализ данных ",
    "Перерасчет ПРБЗ": "(ПРБЗ)",
    "Лётчики": "Лёт",
    "Шахтёры": "Шах",
    "индексация ЕДВ": "индексация ЕДВ",
    "ДМО": "ДМО"
}

operations = [
    "Индексация",
    "80 лет",
    "Перерасчет Ижд. (ФБР)",
    "Анализ работодателей",
    "Перерасчет ПРБЗ",
    "Лётчики",
    "Шахтёры",
    "индексация ЕДВ",
    "ДМО"
]

def check_account_data():
        if os.path.isfile('C:\\soft_for_py_exe\\asp.json'):
            with open('C:\\soft_for_py_exe\\asp.json', 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                if json_data["ACCOUNT"]:
                    login_j = json_data["ACCOUNT"]["login"]
                    password_j = json_data["ACCOUNT"]["password"]

                    return login_j, password_j
        else:
            return False

def run_program():
    login = login_entry.get()
    password = password_entry.get()

    if check_account_data() is False:
        acc = dict()
        if login and password:
            if askokcancel('Запись данных', f"Внимание, сейчас ваши данные для входа будут записаны, подтвердите правильность ввода {login, password}"):
                with open('C:\\soft_for_py_exe\\asp.json', 'a', encoding='utf-8') as f:
                    acc['ACCOUNT'] = {
                        'login': login_entry.get(),
                        'password': password_entry.get()
                    }
                    json.dump(acc, f, ensure_ascii=False, indent=4)
        else:
            showerror("Ошибка", "Введите логин и пароль")
            raise Exception

    date_str = start_date_calendar.get()
    month, day, year_part = date_str.split('/')
    year = int(year_part) + 2000
    start_date = datetime.datetime.strptime(str(day) +"." + str(month) + "." + str(year), '%d.%m.%Y').date()
    end_date = start_date + datetime.timedelta(days=1)

    operation_type_selected = operation_type_combobox.get()
    operation_type = operation_aliases[operation_type_selected]
    server = server_combobox.get()
    reg = ("Москва" if server in ('179', '183', '184') else "Область")
    statistic_state = selected_statistic.get()

    main(login, password, start_date, end_date, operation_type, reg, server, statistic_state)


root = tk.Tk()
root.geometry('400x250')
root.resizable(False, False)
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.wm_geometry("+%d+%d" % (x, y))
root.title("Auto Save Prot")

# Создание фреймов для разделения интерфейса
title_frame = tk.Frame(root)
title_frame.place(y=1, relwidth=1, relheight=0.1)

login_frame = tk.Frame(root)
login_frame.place(relwidth=1, relheight=0.26, y=25)

settings_frame = tk.LabelFrame(root)
settings_frame.place(relwidth=1.5, relheight=0.4, y=100)

buttons_frame = tk.Frame(root)
buttons_frame.place(relwidth=1.5, relheight=0.2, y=200)

# Заголовок
title = tk.Label(title_frame, text="Автоматическая выгрузка протоколов", font=40)
title.place(relx=0.15)

login_label = tk.Label(login_frame, text="Логин от НВП:")
login_label.place(x=10, y=10)
login_entry = tk.Entry(login_frame)
login_entry.place(x=100, y=10)

password_label = tk.Label(login_frame, text="Пароль:")
password_label.place(x=10, y=40)
password_entry = tk.Entry(login_frame, show="*")
password_entry.place(x=100, y=40)

account_data = check_account_data()
if account_data:
    login_a, password_a = account_data
    login_entry.insert(0, login_a)
    password_entry.insert(0, password_a)

start_date_label = tk.Label(login_frame, text="Сервер:")
start_date_label.place(x=280, y=10)

servers = ["179", "183", "184", "209", "206", "210"]
server_combobox = ttk.Combobox(login_frame, values=servers)
server_combobox.place(x=272, y=40, width=70, height=20)

start_date_label = tk.Label(settings_frame, text="Дата начала операции:")
start_date_label.place(x=30, y=5)
start_date_calendar = DateEntry(settings_frame)
start_date_calendar.place(x=45, y=35)

operation_type_frame = tk.Label(settings_frame, text="Тип операции:")
operation_type_frame.place(x=240, y=5)
operation_type_combobox = ttk.Combobox(settings_frame, values=operations)
operation_type_combobox.place(x=213, y=35)

selected_statistic = tk.StringVar(value="Со статой")
with_statistic = tk.Radiobutton(settings_frame, text="Со статистикой", variable=selected_statistic, value="Со статой")
with_statistic.place(x=5, y=65)

without_statistic = tk.Radiobutton(settings_frame, text="Без статистики", variable=selected_statistic, value="Без статы")
without_statistic.place(x=135, y=65)

only_statistic = tk.Radiobutton(settings_frame, text="Только статистика", variable=selected_statistic, value="Только стата")
only_statistic.place(x=265, y=65)

run_button = tk.Button(buttons_frame, text="Начать выгрузку", command=run_program)
run_button.place(x=10, y=7, relwidth=0.634)

root.mainloop()
