import requests
from bs4 import BeautifulSoup

city = input("Введите город: ")

url = f"https://sinoptik.com.ru/погода-{city}"
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        temp = soup.find('p', class_='today-temp')
        
        if temp:
            print(f"Температура в {city}: {temp.text}")
        else:
            print("Не удалось найти температуру")
    else:
        print("Город не найден")
        
except Exception as e:
    print(f"Ошибка: {e}")