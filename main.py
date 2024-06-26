from googletrans import Translator
import requests
import telebot
import telebot.apihelper

from config import TELEGRAM_TOKEN, CITY_COORDINATES_KEY, CITY_COORDINATES_BASE_URL, MAPS_BASE_URL


try:
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    bot_info = bot.get_me()
except telebot.apihelper.ApiTelegramException:
    print("Ошибка токена, проверьте его на правильность")
    bot.stop_bot()
else:
    print("Бот авторизован")


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    """Отправляет пользователю два сообщения: приветствие, 
    а также просьбу отправить название города.
    """
    text = (
        f'Привет! Этот бот позволяет узнать координаты '
        f'нужного вам города.'
    )
    bot.reply_to(message, text)
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Введите название города: ')


@bot.message_handler(func=lambda m: True)
def handle_city(message):
    """Ожидает сообщение пользователя. При получении сообщения отправляет
    пользователю сообщение с информацией о начале поиска.
    """
    bot.send_message(message.chat.id, 'Получено. Ищу координаты.')
    get_city_name(message)


def get_coordinates_url(city_name):
    """Переводит название города на английский. Составляет url для 
    последующего осуществления запроса.
    """
    translator = Translator()
    city_name = str(translator.translate(city_name).text)
    url = f'{CITY_COORDINATES_BASE_URL}{city_name}'
    return url


def get_city_info(city_name):
    """Запрашивает данные через api с помощью url."""
    url = get_coordinates_url(city_name)
    query_params = {
        'apikey': CITY_COORDINATES_KEY
    }
    response = requests.get(url, params=query_params)
    return response


def get_map_url(city_name, latitude, longitude):
    """Возвращает url адрес googlemaps для 
    запрашиваемого города и его координат.
    """
    return f'{MAPS_BASE_URL}{city_name}/@{latitude},{longitude}'


def send_search_failed(message):
    """Отправляет пользователю сообщение об неудачном получении данных.
    """
    text = 'Не удалось получить данные'
    bot.reply_to(message, text)
    exit()


def get_city_name(message):
    """Формирует и отправляет пользователю ответ о поиске запрошенного 
    города в зависимости от успешности поиска.
    """
    city_name = message.text
    response = get_city_info(city_name)
    if response.status_code == 200:
        data = response.json()
        try:
            latitude = data[0].get('latitude')
            longitude = data[0].get('longitude')
        except IndexError:
            print('Элемент не найден')
            send_search_failed(message)
        map_url = get_map_url(city_name, latitude, longitude)
        msg_text = (
            f'Город {city_name} расположен по следующим координатам:\n'
            f'Широта: {latitude}\nДолгота: {longitude}.\nСсылка: {map_url}'
        )
        bot.reply_to(message, msg_text)
    else:
        bot.reply_to(message, f'Город {city_name} не найден\n')


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
