import os
import districts


def move_destricts_in_gu(out_dir, reg):
    # Переносим наши папки районов в ГУ
    for district_dir in os.listdir(out_dir):
        gu_path = districts.get_district(district_dir, out_dir, reg)

        district_dir_path = os.path.join(out_dir, district_dir)

        os.rename(district_dir_path, os.path.join(gu_path, district_dir))
