from elevenlabs import play
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import config

client = ElevenLabs(
 api_key=config.elevenlabs_api_key,
)

def get_all_voices():
    voices = client.voices.get_all()
    return [{'name': voice.name, 'id': voice.voice_id} for voice in voices.voices]


def generate_audio(text: str, voice: str):
    audio = client.generate(
      text=text,
      voice=voice,
      model="eleven_multilingual_v2"
    )
    name = "audio.mp3"
    save(audio, name)
    return name

# print(get_all_voices())

# a = generate_audio('привет Машенька!', 'Charlie')
# play(a)

