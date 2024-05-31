from ElevenLabsHandlerWOLib import ElevenLabsHandlerWOLib
from VoskHandler import VoskHandler
from groqHandler import GroqModel

from FileHandler import FileHandler
from ai_assistant import AI_Assistant
from EmbeddingHandler import EmbeddingHandler

if __name__ == "__main__":
    prompt = FileHandler.readText("prompts/pizzaPrompt.txt")

    stt = VoskHandler("models/vosk-model-small-de-0.15")
    llm = GroqModel("llama3-8b-8192", stream=True)
    tts = ElevenLabsHandlerWOLib(voice_id= "VC9NHIQryLjTvEtbF4kj", model_id="eleven_multilingual_v2")
    emd = EmbeddingHandler(embedding_threshold=0.3) #the smaller the better the match

    ai_assistant = AI_Assistant(stt, llm, tts, emd, prompt)

    fullTranscript = ai_assistant.start_conversation()
    #FileHandler.writeFullTranscript("transcripts/full_transcript.txt", fullTranscript)git checkout your-branch