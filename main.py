import requests
from googletrans import Translator, constants
import telebot

from config import TELEGRAM_TOKEN, CITY_COORDINATES_KEY, CITY_COORDINATES_BASE_URL


bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    text = (
        f'Привет! Этот бот позволяет узнать координаты '
        f'нужного вам города.'
    )
    bot.reply_to(message, text)
    chat_id = message.chat.id
    messg = bot.send_message(chat_id, 'Введите название города: ')
    bot.register_next_step_handler(messg, get_city_name)


def get_city_name(message):
    city_name = message.text
    translator = Translator()
    city_name = str(translator.translate(city_name).text)
    bot.send_message(message.chat.id, 'Получено. Ищу координаты.')
    print(city_name)
    query_params = {
        'apikey': CITY_COORDINATES_KEY
    }
    response = requests.get(CITY_COORDINATES_BASE_URL +
                            city_name, params=query_params)

    if response.status_code == 200:
        data = response.json()
        print(data)
        latitude = data[0].get('latitude')
        longitude = data[0].get('longitude')
        msg_text = (
            f'Город {city_name} расположен по следующим координатам:\n'
            f'Широта: {latitude}\nДолгота: {longitude}.'
        )
        bot.reply_to(message, msg_text)


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
