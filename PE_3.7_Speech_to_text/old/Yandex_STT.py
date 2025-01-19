from pydub import AudioSegment
import requests
import json
from config import IAM_TOKEN

AUDIO_FILE_PATH = '../speech.wav'  # Исходный WAV файл
CONVERTED_AUDIO_PATH = '../speech.ogg'  # Конвертированный OGG файл

# Конвертация аудиофайла в формат OGG с использованием pydub
audio = AudioSegment.from_wav(AUDIO_FILE_PATH)
audio.export(CONVERTED_AUDIO_PATH, format="ogg", codec="libopus")

URL = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'

params = {
    'folderId': 'b1g56h2p36fq4g7gub7l',
    'topic': 'general',
}

headers = {
    'Authorization': f'Bearer {IAM_TOKEN}',
}

# Чтение конвертированного аудиофайла
with open(CONVERTED_AUDIO_PATH, 'rb') as audio_file:
    audio_data = audio_file.read()

# Выполнение POST-запроса
response = requests.post(URL, headers=headers, params=params, data=audio_data)

# Обработка ответа
if response.status_code == 200:
    result = response.json()
    if 'result' in result:
        print('Транскрибированный текст:')
        print(result['result'])
    else:
        print('Распознавание завершилось успешно, но текст не был получен')
else:
    print('Ошибка при распознавании речи:')
    print(f"Статус-код: {response.status_code}")
    print(f"Сообщение: {response.text}")
