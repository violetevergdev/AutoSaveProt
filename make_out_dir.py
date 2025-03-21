import os, datetime
from tkinter.messagebox import showerror

def make_out_dir(reg):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    if reg == "Москва":
        dir_name = 'ПРОТОКОЛЫ МСК'
    else:
        dir_name = 'ПРОТОКОЛЫ ОБЛАСТЬ'

    dir_path = os.path.join(desktop_path, dir_name)

    today = datetime.datetime.today().date().strftime("%d.%m.%Y")
    alt_dir_name = dir_name + str(today)

    if os.path.exists(dir_path):
       new_path = os.path.join(desktop_path, alt_dir_name)
       try:
           os.makedirs(new_path)
           return new_path
       except Exception:
           showerror('Ошибка', "Ошибка создания новой директории")
    else:
        os.makedirs(dir_path, exist_ok=True)
        return dir_path



