import os
from openai import OpenAI
import time

class OpenAIUtils:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def generate_response(self, transcript):
        start_time = time.time()  # Start measuring time
        print(transcript)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=transcript
        )
        end_time = time.time()
        execution_time = end_time - start_time
        #print(f"OpenAI response generation time: {execution_time} seconds")
        return response.choices[0].message.content
