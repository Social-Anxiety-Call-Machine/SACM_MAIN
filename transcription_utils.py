import json
from vosk import Model, KaldiRecognizer
from audio_utils import start_audio_stream, read_audio_data

class Transcription:
    def __init__(self, assistant):
        self.assistant = assistant
        model_path = "vosk-model-de-0.21"
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.transcribing = False

    def start_transcription(self):
        self.transcribing = True
        print("Starting transcription...")
        stream = start_audio_stream()

        speech_detected = False
        silence_threshold = 500
        silence_duration = 0

        while self.transcribing:
            data = read_audio_data(stream)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result["text"]
                if text:
                    print("Transcript:", text)
                    self.assistant.full_transcript.append({"role": "user", "content": text})
                    speech_detected = True
                    silence_duration = 0
            else:
                if speech_detected:
                    silence_duration += 4000 / 16000 * 1000
                    if silence_duration >= silence_threshold:
                        print("Silence detected")
                        self.assistant.generate_ai_response(text)
                        break
                    else:
                        print("Waiting for speech...")

    def stop_transcription(self):
        self.transcribing = False
