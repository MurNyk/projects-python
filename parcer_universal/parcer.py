import requests
from bs4 import BeautifulSoup

url = input("Введите URL сайта: ")
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Найти все заголовки h1
    titles = soup.find_all('h1')
    for i, title in enumerate(titles, 1):
        print(f"{i}. {title.text.strip()}")
else:
    print("Страница не загрузилась")