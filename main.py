from make_out_dir import make_out_dir
from browser import browser_init
from routes_in_nvp import nvp_routes
from move_districts_in_gu import move_destricts_in_gu


def main(login, password, start_date, end_date, operation_type, reg, server):

    out_dir = make_out_dir(reg)

    driver = browser_init(out_dir)

    nvp_routes(driver, login, password, server, operation_type, start_date, end_date, out_dir)

    move_destricts_in_gu(out_dir, reg)

