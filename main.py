import telebot

from config import TELEGRAM_TOKEN


bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    print(message)
    text = (
        f'Привет! Этот бот позволяет узнать координаты'
        f' нужного вам города.'
    )
    bot.reply_to(message, text)


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
