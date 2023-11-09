[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=6BF709&random=false&width=435&lines=%D0%9F%D0%B0%D1%80%D1%81%D0%B5%D1%80+hh.ru)](https://git.io/typing-svg)

Парсер популярного сайта вакансий hh.ru посредством использования API https://dev.hh.ru/

### Технолонии
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)


- Python 3.9
- Pandas 2.1.2
- Pywebio


### Доступный функционал

- Получение вакансий по запросу
- Выбор за какой период
- Сохранения результата в Excel файл


#### Локальный запуск проекта

- Склонировать репозиторий:

```bash
   git clone git@github.com:zsv28/hh_parser.git
```


В папке с проектом создать и активировать виртуальное окружение:

Команда для установки виртуального окружения на Mac или Linux:

```bash
   python3 -m venv env
   source env/bin/activate
```

Команда для Windows:

```bash
   python -m venv venv
   source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```bash
   pip install -r requirements.txt
```

- Запустить локальный сервер:

```bash
   python main.py runserver
```