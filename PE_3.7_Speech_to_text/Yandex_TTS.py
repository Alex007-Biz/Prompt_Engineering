from config import IAM_TOKEN
import requests

# Конфигурация
# IAM_TOKEN = "ваш_IAM_токен"  # Замените на ваш IAM-токен
FOLDER_ID = "b1g56h2p36fq4g7gub7l"  # Идентификатор каталога
TEXT = "Привет! Это пример синтеза речи с помощью Yandex SpeechKit."  # Текст для синтеза речи
OUTPUT_FILE = "output.ogg"  # Имя выходного аудиофайла

# URL API Yandex SpeechKit для синтеза речи
URL = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"

# Параметры запроса
params = {
    "text": TEXT,
    "lang": "ru-RU",  # Язык синтеза речи
    "folderId": FOLDER_ID,
    "speed": "1.0",  # Скорость речи (от 0.1 до 3.0)
    "voice": "alyss",  # Выберите голос (alyss, omazh, jane, etc.)
    "emotion": "neutral",  # Эмоция речи (neutral, good, evil)
    "format": "oggopus",  # Формат аудио (oggopus, lpcm)
}

# Заголовки запроса
headers = {
    "Authorization": f"Bearer {IAM_TOKEN}",
}

# Выполнение запроса
try:
    response = requests.post(URL, headers=headers, data=params)
    response.raise_for_status()  # Проверка на ошибки

    # Сохранение ответа (аудиофайла) в файл
    with open(OUTPUT_FILE, "wb") as f:
        f.write(response.content)

    print(f"Синтез речи завершён. Файл сохранён как {OUTPUT_FILE}")

except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")
