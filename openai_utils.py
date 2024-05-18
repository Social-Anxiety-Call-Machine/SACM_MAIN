import os
from openai import OpenAI

class OpenAIUtils:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def generate_response(self, transcript):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=transcript
        )
        return response.choices[0].message.content
