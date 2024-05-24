from groq import Groq
import os


#groq models: https://console.groq.com/docs/models
class GroqModel:
    def __init__(self, groqmodel, stream):
        self.groqModel = groqmodel
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.stream = stream

    # Streaming
    def generateAnswer(self, transcript):
        stream = self.client.chat.completions.create(
            messages = transcript,
            model = self.groqModel,
            stop = None,
            stream = self.stream
        )

        if self.stream:
            for chunk in stream:
                print(chunk.choies[0].delta.content, end="")
        print(stream)        
        return stream.choices[0].message.content
            
"""
    def batch(self, transcript):
        chat = ChatGroq(temperature=0, model_name=self.groqModel, groq_api_key=self.GroqApiKey)

        system = "You are a helpful assistant."
        human = "{text}"
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

        chain = prompt | chat
        print(chain.invoke({"text": "Explain the importance of low latency LLMs."}))
"""