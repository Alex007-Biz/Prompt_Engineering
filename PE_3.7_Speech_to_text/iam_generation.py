import json
import requests
import jwt  # PyJWT
import time

# Путь к вашему JSON-файлу ключа сервисного аккаунта
SERVICE_ACCOUNT_KEY_FILE = "C:/Users/asus/Documents/GitHub/Prompt_Engineering/PE_3.7_Speech_to_text/authorized_key.json"

# Загрузка JSON-файла
with open(SERVICE_ACCOUNT_KEY_FILE, 'r') as f:
    key_data = json.load(f)

# Извлечение данных из JSON
service_account_id = key_data.get('service_account_id')
private_key = key_data.get('private_key')
key_id = key_data.get('id')  # Используем 'id' как 'kid'

# Проверка наличия необходимых полей
if not all([service_account_id, private_key, key_id]):
    raise ValueError("JSON-файл ключа сервисного аккаунта не содержит необходимых полей.")

# Текущее время и время истечения токена
now = int(time.time())
expire = now + 3600  # Токен будет действителен 1 час

# Заголовок JWT
headers = {
    'alg': 'PS256',
    'typ': 'JWT',
    'kid': key_id  # Убедитесь, что 'kid' соответствует ожидаемому значению
}

# Полезная нагрузка JWT
payload = {
    'iss': service_account_id,
    'sub': service_account_id,
    'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
    'iat': now,
    'exp': expire
}

# Генерация JWT-токена
jwt_token = jwt.encode(payload, private_key, algorithm='PS256', headers=headers)

# Отправка запроса для получения IAM токена
url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
response = requests.post(url, json={'jwt': jwt_token})

# Обработка ответа
if response.status_code == 200:
    iam_token = response.json().get('iamToken')
    print("IAM токен получен:", iam_token)
else:
    print("Ошибка при получении IAM токена:", response.status_code, response.text)

