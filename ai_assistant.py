import os
import random
import asyncio
class AI_Assistant:
    def __init__(self, stt, llm, tts, emd, prompt):
        self.stt = stt
        self.llm = llm
        self.tts = tts
        self.emd = emd
        self.prompt = prompt
        self.full_transcript = [
            {"role": "system", "content": prompt},
        ]

    def start_conversation(self):
        greeting = "Hallo! Ich würde gerne eine Pizza bestellen."
        self.full_transcript.append({"role": "assistant", "content": greeting})
        self.tts.generateSpeech(greeting)
        
        while True:
            self.execute_stt()

            #wahrscheinlich auch über embedding lösen
            if self.full_transcript[-1]["role"] == "user": 
                if "wiedersehen" in self.full_transcript[-1]["content"].lower():
                    break

            asyncio.run(self.EmbeddingOrLLm())
        
        return self.end_conversation()

    def execute_stt(self):
        transcript = self.stt.generateText()
    
        print(f"STT execution time: {self.stt.time} seconds")
        
        self.full_transcript.append({"role": "user", "content": transcript})

    async def execute_llm_tts(self):
        answer = await self.llm.generateAnswer(self.full_transcript)
            
        #llm_task = asyncio.create_task(self.playFiller()) #jo glaube klappt, aber eh falsche stimme und so

        await self.tts.text_to_speech_input_streaming(answer)

        print(f"LLM execution time: {self.llm.time} seconds")
        print(f"TTS execution time: {self.tts.time} seconds")

        #await llm_task

        transcript = "".join(self.llm.transcript)
        self.full_transcript.append({"role": "assistant", "content": transcript})
        print("Assistant: " + transcript)

    async def EmbeddingOrLLm(self):
        llm_task = asyncio.create_task(self.execute_llm_tts())

        embAnswer = self.checkEmbedding() 
        if embAnswer:
            llm_task.cancel()
            await self.playEmbeddingSound(embAnswer)
        else:
            await llm_task

    def checkEmbedding(self):
        best_response = self.emd.get_embedding(self.full_transcript[-1]["content"])

        return best_response
    
    async def playFiller(self):
        filler_folder = os.path.join(os.path.dirname(__file__), "filler")
        filler_files = [f for f in os.listdir(filler_folder) if os.path.isfile(os.path.join(filler_folder, f))]
        filler_file_path = os.path.join(filler_folder, random.choice(filler_files))

        self.tts.playAudio(filler_file_path)

    async def playEmbeddingSound(self, embAnswer):
        embAnswerwith_ = embAnswer.replace(" ", "_")
        
        self.tts.playAudio(f"embedding/embedding_audio/{embAnswerwith_}.mp3")

    def end_conversation(self):
        #Calender, Mail ...

        return self.full_transcript