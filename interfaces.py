from abc import ABC, abstractmethod

class SpeechToText(ABC):
    @abstractmethod
    def generateText(self):
        pass

class LLM(ABC):
    def generateAnswer(self, transcript):
        pass

class TextToSpeech(ABC):
    @abstractmethod
    def generateSpeech(self, text):
        pass
