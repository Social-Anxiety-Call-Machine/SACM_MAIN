from ElevenLabsHandler import ElevenLabsHandler
from ElevenLabsHandlerWOLib import ElevenLabsHandlerWOLib
from OpenaiHandler import OpenAIHandler
from VoskHandler import VoskHandler
from groqHandler import GroqModel

from FileHandler import FileHandler
from ai_assistant import AI_Assistant

if __name__ == "__main__":
    fileHandler = FileHandler()
    prompt = FileHandler.readText("prompts/pizzaPrompt.txt")

    stt = OpenAIHandler("vosk-model-small-de-0.15")
    llm = VoskHandler()
    #tts = ElevenLabsHandler(voice_id= "VC9NHIQryLjTvEtbF4kj", model_id="eleven_multilingual_v2")
    tts = ElevenLabsHandlerWOLib(voice_id= "VC9NHIQryLjTvEtbF4kj", model_id="eleven_multilingual_v2")

    ai_assistant = AI_Assistant(stt, llm, tts, prompt)

    fullTranscript = ai_assistant.start_conversation()
    #fileHandler.writeFullTranscript("transcripts/full_transcript.txt", fullTranscript)git checkout your-branch