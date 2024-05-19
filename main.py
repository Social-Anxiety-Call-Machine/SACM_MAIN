import sys
import os
from ai_assistant import AI_Assistant

def main_loop(ai_assistant):
    greeting = "Hallo! Ich würde gerne eine Pizza bestellen."
    ai_assistant.full_transcript.append({"role": "assistant", "content": greeting})
    ai_assistant.elevenlabs_utils.generate_audio(greeting)
    ai_assistant.transcription.start_transcription()

if __name__ == "__main__":
    ai_assistant = AI_Assistant()
    main_loop(ai_assistant)