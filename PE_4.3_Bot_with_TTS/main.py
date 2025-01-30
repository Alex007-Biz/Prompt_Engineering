import telebot
import config

API_TOKEN = config.bot_token

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для создания озвучки. Выбери голос, который будет использоваться для озвучки:")

if __name__ == '__main__':
    bot.polling(none_stop=True)