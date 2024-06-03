import datetime
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from save_prot import save_prot


def nvp_routes(driver, login, password, server, operation_type, start_date, end_date, out_dir):
    if server == "Москва":
        login_url = 'http://179'
        table_url = 'http://179/index.html'
    else:
        login_url = 'http://206'
        table_url = 'http://206/index.html'

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

    driver.switch_to.frame("navigation_tree")
    mass_op = driver.find_element(By.ID, 'form1:actionbarIndBez_link')
    mass_op.click()
    log = driver.find_element(By.ID, 'form1:text77')
    log.click()
    driver.switch_to.parent_frame()

    # Работа внутри журнала
    driver.switch_to.frame("detail")

    # Ждем загрузки журнала
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 'form1:table1')))

    ind = 0
    last_row_in_page = 29
    start_iteration = True

    while start_iteration:
        # Получаем массив строк журнала
        rows = driver.find_elements(By.CLASS_NAME, 'table-row')

        for _ in rows:
            # Сверяем даты
            dateInCell = driver.find_element(By.ID, 'form1:table1:' + str(ind) + ':text12')

            # Для указания новой последней строки ли мы перешли на сл. страницу
            if ind == last_row_in_page + 1:
                last_row_in_page += 30

            # Извлекаем дату без времени
            date_in_cell = datetime.datetime.strptime(dateInCell.text, "%d.%m.%Y %H:%M:%S").date()

            our_row = date_in_cell == end_date or date_in_cell == start_date

            # Если наши даты, то ...
            if our_row:
                type_of_op_in_cell = driver.find_element(By.ID, 'form1:table1:' + str(ind) + ':text11')

                if type_of_op_in_cell.text == operation_type:
                    num_of_district = driver.find_element(By.ID, 'form1:table1:' + str(ind) + ':text22').text

                    # Проверка наличия протоколов в этом районе и их сохранение
                    save_prot(out_dir, driver, ind, num_of_district)

            # Выход из цикла по причине полной итерации по нашим датам
            elif date_in_cell < start_date:
                print("ВЫХОЖУ - КОНЕЦ ПЕРИОДА")
                start_iteration = False
                break

            # Переключение на др. страницу если строка последняя
            if ind == last_row_in_page:
                next_button = driver.find_element(By.ID, 'form1:table1:deluxe1__pagerNext')
                next_button.click()

            ind += 1

    time.sleep(3)

    driver.close()
