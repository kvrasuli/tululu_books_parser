# Парсер книг с сайта tululu.org

Консольное приложение для парсинга и скачивания книг и их обложек раздела Научная фантастика с сайта [tululu.org](https://dvmn.org/).
Сопутствующая информация сохраняется в формате json.

### Как использовать

- Установить зависимости:

```
pip3 install -r requirements.txt
```

- Запустить скрипт с аргументами, о них ниже:

```
python3 main.py --start_page [start_page] --end_page [end_page]
```

### Аргументы

Скрипт принимает 2 необязательных аргумента - начальная страница сайта для скачивания и конечная,
например:

```
python3 main.py --start_page 700 --end_page 705
```

По умолчанию скачивает первые 5 страниц.
Другие необязательные аргументы:
```
--dest_folder [path_to_folder] - путь для скачивания
--skip_img - не скачивать обложки
--skip_txt - не скачивать книги
--json_path [path_to_json] - путь для json-файла
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
