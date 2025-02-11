from elevenlabs.client import ElevenLabs
import config
from pydub import AudioSegment
from pydub.utils import which
from io import BytesIO
import sounddevice as sd
import numpy as np

# Указываем путь к ffmpeg и ffprobe вручную
ffmpeg_path = "C:\\ffmpeg\\bin\\ffmpeg.exe"
ffprobe_path = "C:\\ffmpeg\\bin\\ffprobe.exe"

# Устанавливаем пути для pydub
AudioSegment.converter = which(ffmpeg_path)
AudioSegment.ffprobe = which(ffprobe_path)

# Инициализация клиента ElevenLabs
client = ElevenLabs(
    api_key=config.elevenlabs_api_key,
)

# Генерация аудио
audio = client.generate(
    text="Привет! Меня зовут Дейв.",
    voice="Dave",
    model="eleven_multilingual_v2"
)

# Собираем данные из генератора в один байтовый объект
audio_bytes = b"".join(audio)  # Преобразуем генератор в байты

# Преобразуем аудио в формат, понятный pydub
audio_segment = AudioSegment.from_file(BytesIO(audio_bytes))

# Преобразуем аудио в массив numpy для sounddevice
samples = np.array(audio_segment.get_array_of_samples())

# Воспроизводим аудио через sounddevice
sd.play(samples, audio_segment.frame_rate)
sd.wait()  # Ждем окончания воспроизведения