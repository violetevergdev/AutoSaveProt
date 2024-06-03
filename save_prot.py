from selenium.webdriver.common.by import By
import os

# Функция для создания папки района
def is_district_dir_exists(out_dir, dir_name):
    district_path = os.path.join(out_dir, dir_name)

    if os.path.exists(district_path):
        new_path = os.path.join(district_path, "(дубль)")
        os.makedirs(new_path)
        return new_path
    else:
        os.makedirs(district_path, exist_ok=True)
        return district_path


def save_prot(out_dir, driver, i, district):
    el_values_ids = [":text35", ":text34", ":text33", ":text32"]
    el_links_ids = [":link8", ":link7", ":link6", ":link5"]

    district_dir = is_district_dir_exists(out_dir, district)

    for el_val_id, el_link_id in zip(el_values_ids, el_links_ids):
        try:
            el_var = driver.find_element(By.ID, 'form1:table1:' + str(i) + el_val_id).text
            if int(el_var) > 0:
                el_link = driver.find_element(By.ID, 'form1:table1:' + str(i) + el_link_id)
                el_link.click()

                for el in os.listdir(out_dir):
                    if el.endswith(".csv"):
                        file_path = os.path.join(out_dir, el)
                        os.rename(file_path, os.path.join(district_dir, el))
        except Exception:
            pass