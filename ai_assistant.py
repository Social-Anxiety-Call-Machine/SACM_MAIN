from openai_utils import OpenAIUtils
from elevenlabs_utils import ElevenLabsUtils
from transcription_utils import Transcription

class AI_Assistant:
    def __init__(self):
        self.transcription = Transcription(self)
        self.openai_utils = OpenAIUtils()
        self.elevenlabs_utils = ElevenLabsUtils()
        self.transcribing = False
        self.full_transcript = [
            {"role": "system", "content": "Du rufst eine Pizzeria an und möchtest eine Pizza bestellen. Du hättest gerne eine Pizza Margherita und eine Pizza Salami."},
        ]

    def generate_ai_response(self, transcript):
        print("Generating AI response...")
        self.transcription.stop_transcription()

        self.full_transcript.append({"role": "user", "content": transcript})
        print(f"\nUser: {transcript}", end="\r\n")

        ai_response = self.openai_utils.generate_response(self.full_transcript)

        self.full_transcript.append({"role": "assistant", "content": ai_response})

        self.elevenlabs_utils.generate_audio(ai_response)
        self.transcription.start_transcription()

    def main_loop(self):
        greeting = "Hallo! Ich würde gerne eine Pizza bestellen."
        self.elevenlabs_utils.generate_audio(greeting)
        self.transcription.start_transcription()

if __name__ == "__main__":
    ai_assistant = AI_Assistant()
    ai_assistant.main_loop()
