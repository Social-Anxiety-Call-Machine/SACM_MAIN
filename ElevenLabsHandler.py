import os
from elevenlabs import stream, play
from elevenlabs.client import ElevenLabs
from interfaces import TextToSpeech

class ElevenLabsHandler(TextToSpeech):
    def __init__(self, model_id, voice_id):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.client = ElevenLabs(api_key=self.api_key)
        self.model_id = model_id
        self.voice_id = voice_id

    def generateSpeech(self, text):
        print("Assistant:", text)
            
        #können hier halt bei elevenLabs nicht in den stream reinschauen; man könnte einfach selber http req machen, vllt weise

        audio_stream = self.client.text_to_speech.convert_as_stream(
            optimize_streaming_latency=2,
            text = text,
            voice_id = self.voice_id,
            model_id = self.model_id
        )
        
        stream(audio_stream)

    def playAudio(self, audio_path):
        with open(audio_path, "rb") as audio:
            audio_content = audio.read()
            play(audio_content)