import time
import threading
import os
import random
import asyncio
class AI_Assistant:
    def __init__(self, stt, llm, tts, prompt):
        self.stt = stt
        self.llm = llm
        self.tts = tts
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

            embAnswer = self.checkEmbedding() # not used yet - returns False
            if embAnswer:
                self.execute_tts(embAnswer)
            else:
                asyncio.run(self.execute_llm_tts())
        
        return self.end_conversation()

    def execute_stt(self):
        transcript = self.stt.generateText()
    
        print(f"STT execution time: {self.stt.time} seconds")
        
        self.full_transcript.append({"role": "user", "content": transcript})

    async def execute_llm_tts(self):
        answer = await self.llm.generateAnswer(self.full_transcript)
        print(f"LLM execution time: {self.llm.time} seconds")

        await self.tts.text_to_speech_input_streaming(answer)
        print(f"TTS execution time: {self.tts.time} seconds")

        # add answer to transcript

    def checkEmbedding(self):
        return False
    
    def playFiller(self):
        filler_folder = os.path.join(os.path.dirname(__file__), "filler")
        filler_files = [f for f in os.listdir(filler_folder) if os.path.isfile(os.path.join(filler_folder, f))]
        filler_file_path = os.path.join(filler_folder, random.choice(filler_files))

        self.tts.playAudio(filler_file_path)

    def end_conversation(self):
        #Calender, Mail ...

        return self.full_transcript