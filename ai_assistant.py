import time
import threading
import os
import random

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

            embAnswer = self.checkEmbedding() # not used yet - returns true
            if embAnswer:
                self.execute_tts(embAnswer)
            else:
                threading.Thread(target=self.execute_llm).start()
                while threading.active_count() > 1:
                    time.sleep(1)
                    self.playFiller()
                    self.playFiller()

                self.execute_llm()
                self.execute_tts()    
        
        return self.end_conversation()

    def execute_stt(self):
        transcript = self.stt.generateText()
    
        print(f"STT execution time: {self.stt.time} seconds")
        
        self.full_transcript.append({"role": "user", "content": transcript})

    def execute_llm(self):
        start_time = time.time()
        answer = self.llm.generateAnswer(self.full_transcript)
        end_time = time.time()
        print(f"LLM execution time: {end_time - start_time} seconds")
        
        self.full_transcript.append({"role": "assistant", "content": answer})

    def execute_tts(self):
        self.tts.generateSpeech(self.full_transcript[-1]["content"])

        #print(f"TTS execution time: {self.tts.time} seconds")

    def checkEmbedding(self):
        return False
    
    def playFiller(self):
        filler_folder = os.path.join(os.path.dirname(__file__), "filler")
        filler_files = os.listdir(filler_folder)
        filler_file_path = os.path.join(filler_folder, random.choice(filler_files))

        self.tts.playAudio(filler_file_path)

    def end_conversation(self):
        #Calender, Mail ...

        return self.full_transcript