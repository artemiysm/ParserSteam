import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('bot'))


bot.set_my_commands([
    telebot.types.BotCommand("start", "Запустить бота"),
    telebot.types.BotCommand("help", "Помощь"),
])

url = 'https://store.steampowered.com/'

@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button1 = types.KeyboardButton("Раздача Steam")
    button2 = types.KeyboardButton("Раздача Epic Games")
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, "Выберите платформу:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Раздача Steam")
def handle_steam(message):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    allgame = soup.find_all('a', class_='tab_item')
    games = []
    for data in allgame:
        name = data.find('div', class_='tab_item_name')
        final_price = data.find('div', class_='discount_final_price')
        discount_pct = data.find('div', class_='discount_pct')

        if name and final_price and discount_pct:
            game = {
                'name': name.text.strip(),
                'price': final_price.text.strip(),
                'discount': discount_pct.text.strip()
            }
            games.append(game)
            bot.send_message(
                message.chat.id,
                f' Игра: {game["name"]}\n Цена: {game["price"]}\n Скидка: {game["discount"]}'
            )

    msg = bot.send_message(message.chat.id, " Введите название игры для поиска:")
    bot.register_next_step_handler(msg, process_search, games)  

def process_search(message, games):
    query = message.text.lower() 
    results = [g for g in games if query in g['name'].lower()]
    
    if results:
        for game in results:
            bot.send_message(
                message.chat.id,
                f" Найдено:\n\nИгра: {game['name']}\nЦена: {game['price']}\nСкидка: {game['discount']}"
            )
    else:
        bot.send_message(message.chat.id, "Игра не найдена. Попробуйте другое название.")
@bot.message_handler(func=lambda message: message.text == "Раздача Epic Games")
def handle_hi(message):
    bot.send_message(message.chat.id, "Здесь скоро будет раздача")
bot.polling()