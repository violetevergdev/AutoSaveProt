from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

def browser_init(out_dir):
    options = Options()
    options.headless = False
    # options.binary_location = 'C:\\soft_for_py_exe\\Mozilla Firefox\\firefox.exe'

    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.improvements_to_download_panel", False)
    options.set_preference("browser.download.dir", out_dir)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

    #Ставим драйвер
    driver_local_path = Service('C:\\soft_for_py_exe\\geckodriver.exe')
    driver = webdriver.Firefox(options=options, service=driver_local_path)

    return driver
