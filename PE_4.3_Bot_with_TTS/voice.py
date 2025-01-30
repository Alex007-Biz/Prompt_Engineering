# from elevenlabs import play
# from elevenlabs.client import ElevenLabs
from config import elevenlabs_api_key

print(f"config.elevenlabs_api_key: {elevenlabs_api_key}")

# client = ElevenLabs(
#  api_key=config.elevenlabs_api_key,
# )
# print(f"config.elevenlabs_api_key: {config.elevenlabs_api_key}")
# audio = client.generate(
#   text="Привет! Меня зовут Дейв.",
#   voice="Dave",
#   model="eleven_multilingual_v2"
# )
# with open("output.mp3", "wb") as f:
#     f.write(audio)  # audio — это bytes-объект
#
# play(audio)