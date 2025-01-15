import requests
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from config import PIXABAY_API_KEY

# Настройки

search_query = 'The process of home or apartment renovation: laying tiles or porcelain stoneware, installing plumbing fixtures.'  # Ваш поисковый запрос
per_page = 3  # Количество видео для загрузки

logo_path = '/content/logotype.svg'  # Путь к вашему логотипу

# Функции
def download_pixabay_videos(query, per_page=3):
    url = 'https://pixabay.com/api/videos/'

    params = {
        'key': PIXABAY_API_KEY,
        'q': query,
        'per_page': per_page,
        'safesearch': 'true'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        videos = response.json()['hits']
        video_paths = []
        for idx, video in enumerate(videos):
            # Выбираем видео с наилучшим качеством
            video_files = video['videos']
            if 'large' in video_files:
                video_url = video_files['large']['url']
            elif 'medium' in video_files:
                video_url = video_files['medium']['url']
            else:
                video_url = video_files['small']['url']

            video_response = requests.get(video_url)
            video_filename = f'video_{idx}.mp4'
            with open(video_filename, 'wb') as f:
                f.write(video_response.content)
            video_paths.append(video_filename)
        return video_paths
    else:
        print('Ошибка при запросе к Pixabay API:', response.status_code)
        return []

def overlay_logo_on_video(video_path, logo_path, output_path):
    # Загрузка видео
    video_clip = VideoFileClip(video_path)

    # Проверка наличия аудио (для избежания предупреждений)
    if video_clip.audio is None:
        video_clip = video_clip.set_audio(None)

    # Загрузка логотипа
    logo = (ImageClip(logo_path)
            .set_duration(video_clip.duration)
            .resize(height=100)  # Измените размер логотипа при необходимости
            .margin(right=8, top=8, opacity=0)  # Отступы
            .set_pos(("right", "top")))  # Позиция логотипа

    # Наложение логотипа на видео
    final_video = CompositeVideoClip([video_clip, logo])

    # Сохранение итогового видео
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # Освобождение ресурсов
    video_clip.close()
    final_video.close()

# Основной процесс

video_paths = download_pixabay_videos(search_query, per_page)

if video_paths:
    for video_path in video_paths:
        output_path = f'logo_{video_path}'
        overlay_logo_on_video(video_path, logo_path, output_path)
        print(f'Видео с наложенным логотипом сохранено: {output_path}')
else:
    print('Не удалось скачать видео.')
