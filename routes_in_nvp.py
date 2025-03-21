import datetime
import time
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from save_prot import save_prot


def nvp_routes(driver, login, password, server, operation_type, start_date, end_date, out_dir, statistic_state):
    data = dict()

    login_url = 'http://10.87.0.' + server + ':9080/ViplataWEB'

    if operation_type in ("ДМО-Лёт", "ДМО-Шах", "ДМО"):
        table_url = 'http://10.87.0.' + server + ':9080/DMOcReport.jsp'
    elif operation_type == "индексация ЕДВ":
        table_url = 'http://10.87.0.' + server + ':9080/RecalcReport.jsp'
    else:
        table_url = 'http://10.87.0.' + server + ':9080/CommonlcReport.jsp'


    # Запуск НВП в Firefox
    driver.get(login_url)

    # Логинимся
    user_field = driver.find_element(By.NAME, 'j_username')
    user_field.send_keys(login)

    pass_field = driver.find_element(By.NAME, 'j_password')
    pass_field.send_keys(password)

    action_button = driver.find_element(By.NAME, 'action')
    action_button.click()

    # Переход на журнал перерасчетов
    driver.get(table_url)

    # Ждем загрузки журнала
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 'form1:table1')))

    if operation_type in ("ДМО-Лёт", "ДМО-Шах", "ДМО"):
        select = Select(driver.find_element(By.ID, "form1:menuTFile"))
        select.select_by_value("0")
    else:
        select = Select(driver.find_element(By.ID, "form1:menu3"))
        select.select_by_value("2")


    ind = 0
    page = 1
    last_row_in_page = 29
    start_iteration = True

    while start_iteration:
        # Получаем массив строк журнала
        rows = driver.find_elements(By.CLASS_NAME, 'table-row')

        for _ in rows:
            # Сверяем даты
            dateInCell = driver.find_element(By.ID, 'form1:table1:' + str(ind) + ':text12')
            dateEndInCell = driver.find_element(By.ID, 'form1:table1:' + str(ind) + ':text13')

            # Для указания новой последней строки ли мы перешли на сл. страницу
            if ind == last_row_in_page + 1:
                last_row_in_page += 30

            # Извлекаем дату без времени
            date_in_cell = datetime.datetime.strptime(dateInCell.text, "%d.%m.%Y %H:%M:%S").date()

            our_row = date_in_cell == end_date or date_in_cell == start_date

            # Если наши даты, то ...
            if our_row:
                if operation_type in ("ДМО-Лёт", "ДМО-Шах", "ДМО"):
                    type_id = ":textKat"
                elif operation_type == "индексация ЕДВ":
                    type_id = ":textVid14"
                else:
                    type_id = ':text11'

                type_of_op_in_cell = driver.find_element(By.ID, 'form1:table1:' + str(ind) + type_id)

                if operation_type == "ДМО":
                    inner_op_type = ("ДМО-ООН", "ДМО-Пре", "ДМО-995", "ДМО-Выд", "ДМО-Атм", "ДМО-ВОВ", "ДМО-Гос")
                else:
                    inner_op_type = (operation_type,)

                if type_of_op_in_cell.text in inner_op_type:
                    if operation_type in ("ДМО-Лёт", "ДМО-Шах", "ДМО"):
                        mode_id = ":textSDPMode"
                    elif operation_type == "индексация ЕДВ":
                        mode_id = ":text132"
                    else:
                        mode_id = ':textMode'

                    mode_in_cell = driver.find_element(By.ID, 'form1:table1:' + str(ind) + mode_id)

                    if mode_in_cell.text == 'с сохранением':
                        num_of_district = driver.find_element(By.ID, 'form1:table1:' + str(ind) + ':text22').text

                        if statistic_state in ("Со статой", "Только стата"):
                            if operation_type == "ДМО":
                                if num_of_district in data:
                                    if data[num_of_district].get(type_of_op_in_cell.text):
                                        data[num_of_district].update({
                                        type_of_op_in_cell.text: (data[num_of_district].get(type_of_op_in_cell.text) + 1)
                                    })
                                    else:
                                        data[num_of_district].update({
                                            type_of_op_in_cell.text: 1
                                        })
                                else:
                                    data[num_of_district] = {
                                        type_of_op_in_cell.text: 1
                                    }
                            elif operation_type not in ("ДМО-Лёт", "ДМО-Шах", "индексация ЕДВ"):
                                if num_of_district in data:
                                   num_of_district_dub = num_of_district + 'dub'
                                   data[num_of_district_dub] = {
                                        "Начало": dateInCell.text,
                                        "Конец": dateEndInCell.text
                                    }
                                else:
                                    data[num_of_district] = {
                                        "Начало": dateInCell.text,
                                        "Конец": dateEndInCell.text
                                    }
                        if statistic_state in ("Со статой", "Без статы"):
                            # Проверка наличия протоколов в этом районе и их сохранение
                            save_prot(operation_type, out_dir, driver, ind, num_of_district)

            # Выход из цикла по причине полной итерации по нашим датам
            elif date_in_cell < start_date:
                print("ВЫХОЖУ - КОНЕЦ ПЕРИОДА")
                start_iteration = False
                if statistic_state in ("Со статой", "Только стата"):
                    if operation_type not in ("ДМО-Лёт", "ДМО-Шах", "индексация ЕДВ"):
                        with open(f'statistic-{operation_type}.json', mode='w', encoding='UTF-8') as file:
                            json.dump(data, file, ensure_ascii=False, indent=4)
                break

            # Переключение на др. страницу если строка последняя
            if ind == last_row_in_page:
                next_button = driver.find_element(By.ID, 'form1:table1:' + (
                    'deluxe1__pagerNext'
                    if operation_type not in ("ДМО-Лёт", "ДМО-Шах", "индексация ЕДВ", "ДМО")
                    else "web1__pagerWeb__" + str(page) + '_next'))
                next_button.click()

                if operation_type in ("ДМО-Лёт", "ДМО-Шах", "индексация ЕДВ", "ДМО"):
                    page += 1

            ind += 1

    time.sleep(1)

    driver.close()
