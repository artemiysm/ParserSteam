import requests
from bs4 import BeautifulSoup

url = 'https://store.steampowered.com/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

allgame = soup.find_all('a', class_='tab_item')

for data in allgame:
    name = data.find('div', class_='tab_item_name')
    final_price = data.find('div', class_='discount_final_price')
    discount_pct = data.find('div', class_='discount_pct')

    if name and final_price:
        game_name = name.text.strip()
        price = final_price.text.strip()
        discount = discount_pct.text.strip() if discount_pct else 'Нет скидки'

        print(f'Игра: {game_name} | Цена: {price} | Скидка: {discount}')
