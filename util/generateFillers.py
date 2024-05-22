import os
from elevenlabs.client import ElevenLabs

class model():
    def __init__(self, model_id, voice_id):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.client = ElevenLabs(api_key=self.api_key)
        self.model_id = model_id
        self.voice_id = voice_id

    def generateSpeech(self, text):
        print("Assistant:", text)

        audio = self.client.text_to_speech.convert(
            text = text,
            voice_id = self.voice_id,
            model_id = self.model_id
        )
        
        audio_content = b"".join(audio)

        print(type(audio_content))
        with open(f"{text}.mp3", "wb") as f:
            f.write(audio_content)

eleven = model(voice_id= "VC9NHIQryLjTvEtbF4kj", model_id="eleven_multilingual_v2")

fillerWords = ["jaaa"]
for word in fillerWords:
    eleven.generateSpeech(word)