import os
from openai import OpenAI
from interfaces import LLM

class OpenAIHandler(LLM):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def generateAnswer(self, transcript):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=transcript
        )

        return response.choices[0].message.content
