# AutoSaveProt
 
Автоматизация процесса выгрузки протоколов во внутренней программе.

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
    * [Персональная настройка](#персональная-настройка)
    * [Использование заданных настроек](#использование-заданных-настроек)
- [Разработка](#разработка)
    * [Требования](#требования)
    * [Установка зависимостей](#установка-зависимостей)
    * [Компиляция](#компиляция)

## Технологии
- [Python 3.8.7](https://www.python.org/downloads/release/python-387/)
- [selenium](https://pypi.org/project/selenium/)
- [tkcalendar](https://pypi.org/project/tkcalendar/)



## Использование

#### Настройка перед использованием в НВП
Для работы необходимо разархивировать в корень диска C:\ архив ``soft_for_py_exe`` (находится в [Releases](https://github.com/violetevergdev/Sverka/releases/tag/v.3.1.0))

Для настройки рекомендуется установить на ПК файлы располагающиеся в ветке main.

Изменения необходимо внести в файл `gui.py`, а конкретно изменить `operation_aliases` и `operations`

Также требуется внести корректировки в url адреса в файле `routes_in_nvp.py`

## Разработка

### Требования
Для установки и запуска проекта, необходим [Python 3.8.7](https://www.python.org/downloads/release/python-387/)

### Установка зависимостей
Используемые библиотеки
```sh
pip install selenium tkcalendar pyinstaller
```

### Компиляция
```sh
pyinstaller --onefile --hidden-import "babel.numbers" --windowed --name AutoSaveProt gui.py
```


