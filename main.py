from ElevenLabsHandler import ElevenLabsUtils
from OpenaiHandler import OpenAIModel
from VoskHandler import VoskModel

from FileHandler import FileHandler
from ai_assistant import AI_Assistant

if __name__ == "__main__":
    fileHandler = FileHandler()
    prompt = fileHandler.readText("prompts/pizzaPrompt.txt")
    ai_assistant = AI_Assistant(VoskModel("vosk-model-small-de-0.15"), OpenAIModel(), ElevenLabsUtils(voice_id= "VC9NHIQryLjTvEtbF4kj", model_id="eleven_multilingual_v2"), prompt)

    fullTranscript = ai_assistant.start_conversation()
    fileHandler.writeText("transcripts/full_transcript.txt", fullTranscript)