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
            {"role": "system", "content": """
            Du rufst in einer Pizzeria an und möchtest eine Pizza Schinken bestellen. Deine Adresse lautet: Bahnhofstraße 1, Musterstadt.
            Du bist sehr freundlich und antwortest auf die Fragen des Mitarbeiters. Du möchtest die Pizza geliefert haben. 
            Außerdem antwortest du kurz und präzise auf die Fragen des Mitarbeiters.
            Dein Name ist Max Mustermann.
            """
            },
        ]

    def generate_ai_response(self, transcript):
        #print("Generating AI response...")
        self.transcription.stop_transcription()

        self.full_transcript.append({"role": "user", "content": transcript})
        print(f"User: {transcript}")

        ai_response = self.openai_utils.generate_response(self.full_transcript)

        self.full_transcript.append({"role": "assistant", "content": ai_response})

        self.elevenlabs_utils.generate_audio(ai_response)
        self.transcription.start_transcription()