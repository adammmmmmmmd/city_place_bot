import requests
from googletrans import Translator
import telebot

from config import TELEGRAM_TOKEN, CITY_COORDINATES_KEY, CITY_COORDINATES_BASE_URL, MAPS_BASE_URL

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    text = (
        f'Привет! Этот бот позволяет узнать координаты '
        f'нужного вам города.'
    )
    bot.reply_to(message, text)
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Введите название города: ')


@bot.message_handler(func=lambda m: True)
def handle_city(message):
    bot.send_message(message.chat.id, 'Получено. Ищу координаты.')
    get_city_name(message)



def get_city_name(message):
    print('Вызывана функция')
    city_name = message.text
    translator = Translator()
    city_name = str(translator.translate(city_name).text)

    query_params = {
        'apikey': CITY_COORDINATES_KEY
    }
    url = (f'{CITY_COORDINATES_BASE_URL}{city_name}')
    response = requests.get(url, params=query_params)

    if response.status_code == 200:
        data = response.json()

        latitude = data[0].get('latitude')
        longitude = data[0].get('longitude')
        map_url = (f'{MAPS_BASE_URL}{city_name}/@'
                    f'{latitude}{longitude}')
        map_link = (map_url)
        msg_text = (
            f'Город {city_name} расположен по следующим координатам:\n'
            f'Широта: {latitude}\nДолгота: {longitude}.Ссылка: {map_link}'
        )
        bot.reply_to(message, msg_text)
    else:
        bot.reply_to(message, f'Город {city_name} не найден\n')


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
