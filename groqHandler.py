from groq import AsyncGroq
import os, time

#groq models: https://console.groq.com/docs/models
class GroqModel:
    def __init__(self, groqmodel, stream):
        self.groqModel = groqmodel
        self.client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        self.stream = stream
        self.first = False
        self.time = -1

    async def generateAnswer(self, transcript):
        startTime = time.time()
        response = await self.client.chat.completions.create(
            messages = transcript,
            model = "llama3-70b-8192",
            stream = True
        )
        
        async def text_iterator():
            async for chunk in response:
                delta = chunk.choices[0].delta
                if delta.content is not None:
                    if not self.first:
                        self.time = time.time() - startTime
                        self.first = True
                    yield delta.content

        return text_iterator()