import telebot
import config
import voice

API_TOKEN = config.bot_token

bot = telebot.TeleBot(API_TOKEN)

voices = voice.get_all_voices()
voice_buttons = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
for v in voices:
    button = telebot.types.KeyboardButton(v['name'])
    voice_buttons.add(button)

selected_voice = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Я бот для создания озвучки! Выбери голос, который будет использоваться при создании озвучки:",
        reply_markup=voice_buttons
    )


@bot.message_handler(func=lambda message: message.text in [v['name'] for v in voices])
def voice_selected(message):
    user_id = message.from_user.id
    selected_voice[user_id] = message.text
    bot.reply_to(message, f"Вы выбрали голос: {message.text}. Теперь введите текст для озвучки:")


@bot.message_handler(func=lambda message: True)
def generate_voice(message):
    user_id = message.from_user.id
    if user_id in selected_voice:
        voice_name = selected_voice[user_id]
        try:
            voice_id = next(v['id'] for v in voices if v['name'] == voice_name)
            audio_file = voice.generate_audio(message.text, voice_id)

            with open(audio_file, 'rb') as audio:
                bot.send_voice(message.chat.id, audio)
        except StopIteration:
            bot.reply_to(message, "Ошибка: выбранный голос не найден.")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {str(e)}")
    else:
        bot.reply_to(message, "Сначала выберите голос командой /start")


if __name__ == '__main__':
    bot.polling(none_stop=True)