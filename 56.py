import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def collect_user_rates(user_login):
    page_num = 1
    data = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    while True:
        url = f'https://www.kinopoisk.ru/user/{user_login}/votes/list/vs/vote/page/{page_num}/#list'
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Проверка на ошибки HTTP
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе страницы: {e}")
            break

        html_content = response.text
        print(url)

        soup = BeautifulSoup(html_content, 'lxml')
        entries = soup.find_all('div', class_='item')

        if len(entries) == 0:  # Признак остановки
            print("Фильмов больше нет, либо их не удалось получить")
            break

        for entry in entries:
            div_film_details = entry.find('div', class_="nameRus")
            if div_film_details:
                film_name = div_film_details.find('a').text
            else:
                film_name = "Неизвестно"

            watching_date = entry.find('div', class_='date').text if entry.find('div', class_='date') else "Неизвестно"
            rating = entry.find('div', class_="vote").text if entry.find('div', class_="vote") else "Неизвестно"

            data.append({'Фильм': film_name, 'Дата просмотра': watching_date, 'Оценка': rating})

        page_num += 1  # Переход на следующую страницу
        time.sleep(5)  # Задержка времени для обхода защиты

    return data

user_rates = collect_user_rates(user_login='550660')
df = pd.DataFrame(user_rates)

df.to_excel(r'C:\Users\dublk\PycharmProjects\PythonProject\.venv\user_rates.xlsx', index=False)