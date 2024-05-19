import os
import time
from elevenlabs import Voice, VoiceSettings, play, stream
from elevenlabs.client import ElevenLabs

class ElevenLabsUtils:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.client = ElevenLabs(api_key=self.api_key)

    def generate_audio(self, text):
        print("Assistant:", text)
        voice_response = self.client.voices.get_all()
        
        start_time = time.time()  # Start measuring time
        
        audio_stream = self.client.text_to_speech.convert_as_stream(
            text=text,
            voice_id="VC9NHIQryLjTvEtbF4kj",
            model_id="eleven_turbo_v2"
        )
        stream(audio_stream)
        
        end_time = time.time()  # Stop measuring time
        execution_time = end_time - start_time
        #print(f"Audio generation time: {execution_time} seconds")
