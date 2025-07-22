import requests
from bs4 import BeautifulSoup

url = 'https://store.steampowered.com/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

allgame = soup.find_all('a', class_='tab_item')
games = []
for data in allgame:
    name = data.find('div', class_='tab_item_name')
    final_price = data.find('div', class_='discount_final_price')
    discount_pct = data.find('div', class_='discount_pct')

    if name and final_price and discount_pct:
        game_name = name.text.strip()
        price = final_price.text.strip()
        discount = discount_pct.text.strip()
        game = {
            'name': name.text.strip(),
            'price': final_price.text.strip(),
            'discount': discount_pct.text.strip()
        }
        games.append(game)
        print(f'Игра: {game_name} | Цена: {price} | Скидка: {discount}')
query = input("Введите название игры для поиска: ").lower()
results = [g for g in games if query in g['name'].lower()]
if results:
    for game in results:
        print(f"Игра: {game['name']} | Цена: {game['price']} | Скидка: {game['discount']}")
else:
    print("Игры с таким названием не найдено.")
input("Нажмите любую кнопку для завершения: ")