import os
from elevenlabs import Voice, VoiceSettings, play, stream
from elevenlabs.client import ElevenLabs

class ElevenLabsUtils:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.client = ElevenLabs(api_key=self.api_key)

    def generate_audio(self, text):
        voice_response = self.client.voices.get_all()
        audio_stream = self.client.text_to_speech.convert_as_stream(
            text=text,
            voice_id="VC9NHIQryLjTvEtbF4kj"
        )
        stream(audio_stream)
