from config import IAM_TOKEN
import urllib.request
import json

FOLDER_ID = "b1g56h2p36fq4g7gub7l"  # Идентификатор каталога

# Чтение аудиофайла в бинарном формате
with open("speechkit_2.ogg", "rb") as f:
    audio_data = f.read()

# Формирование параметров URL
params = "&".join([
    "topic=general",
    f"folderId={FOLDER_ID}",
    "lang=ru-RU"
])

# Формирование полного URL
url = f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}"

# Формирование запроса
request = urllib.request.Request(url, data=audio_data, method="POST")
request.add_header("Authorization", f"Bearer {IAM_TOKEN}")
request.add_header("Content-Type", "application/ogg")

try:
    # Отправка запроса
    with urllib.request.urlopen(request) as response:
        response_data = response.read().decode('UTF-8')

    # Декодирование ответа
    decoded_data = json.loads(response_data)

    if "result" in decoded_data:
        print("Распознанный текст:")
        print(decoded_data["result"])
    else:
        print("Ошибка в ответе API:")
        print(decoded_data)

except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code} {e.reason}")
    print(e.read().decode('UTF-8'))

except Exception as e:
    print(f"Произошла ошибка: {e}")

