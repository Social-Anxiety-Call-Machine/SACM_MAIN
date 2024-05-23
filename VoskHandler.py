import json, time
from vosk import Model, KaldiRecognizer
from audio_utils import start_audio_stream, read_audio_data
from interfaces import SpeechToText

class VoskHandler(SpeechToText):
    def __init__(self, modelPath):
        self.model = Model(modelPath)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.transcribing = False
        self.time = -1

    def generateText(self):
        startTime = time.time()
        firstBit = False

        self.transcribing = True
        print("Starting transcription...")
        stream = start_audio_stream()

        speech_detected = False
        silence_threshold = 1000
        silence_duration = 0

        while self.transcribing:
            data = read_audio_data(stream)
            if len(data) == 0:
                break
            if not firstBit:
                self.time = time.time() - startTime
                firstBit = True
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result["text"]
                if text:
                    print("Transcript:", text)
                    speech_detected = True
                    silence_duration = 0
            else:
                if speech_detected:
                    silence_duration += 4000 / 16000 * 1000
                    if silence_duration >= silence_threshold:
                        print("Silence detected")
                        self.stop_transcription()
                        break
                    else:
                        #print("Waiting for speech...")
                        pass
        return text    
    

    def stop_transcription(self):
        self.transcribing = False
