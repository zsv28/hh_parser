import time
from datetime import datetime, timedelta

import pandas as pd
import requests
from dateutil.parser import parse
from pywebio import input, output, start_server

AREA_ID = 113  # Идентификатор области поиска, 113 - Россия
RESULTS_PER_PAGE = 100  # Количество результатов на странице


def format_date(date_str):
    """Форматирование даты"""
    try:
        date_obj = parse(date_str)
        formatted_date = date_obj.strftime("%H:%M %d-%m-%Y")
        return formatted_date
    except ValueError:
        return "Неверная дата"


def show_loading_message():
    """Отображение сообщения загрузки"""
    loading_message = """
    <div style="text-align: center;">
        <p>Загрузка, пожалуйста подождите...</p>
        <img src="https://s6.gifyu.com/images/S605j.gif" width="50">
    </div>
    """
    output.put_html(loading_message)


def get_vacancies(keyword, start_date):
    """Возвращает полученные вакансии"""
    url = "https://api.hh.ru/vacancies"
    all_vacancies = []
    page = 0
    total_vacancies = None
    show_loading_message()
    while total_vacancies is None or len(all_vacancies) < total_vacancies:
        params = {
            "text": keyword,
            "area": AREA_ID,
            "per_page": RESULTS_PER_PAGE,
            "page": page,
            "date_from": start_date.strftime("%Y-%m-%d"),
        }

        headers = {
            "User-Agent": "Your User Agent",
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            vacancies = data.get("items", [])

            if total_vacancies is None:
                total_vacancies = data.get("found", 0)

            if not vacancies:
                break

            all_vacancies.extend(vacancies)
            page += 1
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            return f"Запрос не прошел с ошибкой: {e}"

    return all_vacancies


def display_vacancies(all_vacancies, keyword, period):
    """Вывод полученных вакансий в таблицу"""
    today = datetime.now().strftime("%Y-%m-%d")
    recent_vacancies = [vacancy for vacancy in all_vacancies if
                        vacancy.get("published_at").startswith(today)]
    recent_vacancies.sort(
        key=lambda x: parse(x.get("published_at")), reverse=True)

    table_data = []

    for vacancy in recent_vacancies:
        vacancy_data = {
            "Дата публикации": format_date(vacancy.get("published_at")),
            "Город": vacancy.get("area", {}).get("name"),
            "Вакансия": vacancy.get("name"),
            "Компания": vacancy.get("employer", {}).get("name"),
            "Ссылка": vacancy.get("alternate_url"),
            "Опыт": vacancy.get("experience", {}).get("name"),
        }

        salary_data = vacancy.get("salary")
        if salary_data:
            salary_from = salary_data.get("from")
            salary_to = salary_data.get("to")
            salary_currency = salary_data.get("currency", "Не указано")

            if salary_from is not None and salary_to is not None:
                vacancy_data[
                    "Зарплата"] = (f"от {salary_from} до {salary_to} "
                                   f"{salary_currency}")
            elif salary_from is not None:
                vacancy_data[
                    "Зарплата"] = f"от {salary_from} {salary_currency}"
            elif salary_to is not None:
                vacancy_data["Зарплата"] = f"до {salary_to} {salary_currency}"
            else:
                vacancy_data["Зарплата"] = "Не указано"
        else:
            vacancy_data["Зарплата"] = "Не указано"
        table_data.append(vacancy_data)
    table_data.sort(key=lambda x: parse(x["Дата публикации"]), reverse=True)
    df = pd.DataFrame(table_data)
    output.clear()
    output.put_text(
        f"Список вакансий по запросу {keyword}, за период "
        f"{period} дней.").style(
        'font-weight: bold; font-size: 20px; text-align: center;')
    output.put_datatable(table_data, height=800)

    def save_data_to_excel():
        """Сохранение вакансий в формат Excel"""
        df.to_excel('vacancies.xlsx', index=False)
        output.put_text("Сохранено в файл 'vacancies.xlsx'").style(
            'font-size: 16px; text-align: center;')

    output.put_button("Сохранить в Excel", save_data_to_excel)

    output.put_text(
        f"Всего получено вакансий: {len(recent_vacancies)}.").style(
        'font-size: 16px; text-align: center;')


def search_vacancies():
    """Поиск вакансий по ключевому запросу"""
    output.put_text("Парсинг вакансий на hh.ru с помощью API").style(
        'font-weight: bold; font-size: 24px; text-align: center;')
    keyword = input.input(
        "Введите ключевое слово для поиска вакансий:", type=input.TEXT,
        placeholder="например, python", required=True)
    period = input.input(
        "Введите количество дней(последних) для поиска:",
        type=input.NUMBER, placeholder="например, 3", required=True)
    output.clear()

    start_time = time.time()
    start_date = datetime.now() - timedelta(days=period)
    all_vacancies = get_vacancies(keyword, start_date)
    end_time = time.time()
    loading_time = round(end_time - start_time, 2)

    if isinstance(all_vacancies, str):
        output.put_text(all_vacancies)
    else:
        display_vacancies(all_vacancies, keyword, period)
        output.put_text(f"Данные получены за {loading_time} секунд.").style(
            'font-size: 16px; text-align: center;')


if __name__ == '__main__':
    start_server(search_vacancies, port=8080)
