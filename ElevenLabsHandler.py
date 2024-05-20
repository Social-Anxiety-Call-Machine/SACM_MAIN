import os
from elevenlabs import Voice, VoiceSettings, play, stream
from elevenlabs.client import ElevenLabs
from interfaces import TextToSpeech

class ElevenLabsUtils(TextToSpeech):
    def __init__(self, model_id, voice_id):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.client = ElevenLabs(api_key=self.api_key)
        self.model_id = model_id
        self.voice_id = voice_id

    def generateSpeech(self, text):
        print("Assistant:", text)
            
        audio_stream = self.client.text_to_speech.convert_as_stream(
            text = text,
            voice_id = self.voice_id,
            model_id = self.model_id
        )
        
        stream(audio_stream)