import time

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
            answer = self.execute_llm()
            self.execute_tts(answer)
        
        return self.end_conversation()

    def execute_stt(self):
        start_time = time.time()
        transcript = self.stt.generateText()
        end_time = time.time()
        print(f"STT execution time: {end_time - start_time} seconds")
        
        self.full_transcript.append({"role": "user", "content": transcript})
        print(f"User: {transcript}")

        return transcript

    def execute_llm(self):
        start_time = time.time()
        answer = self.llm.generateAnswer(self.full_transcript)
        end_time = time.time()
        print(f"LLM execution time: {end_time - start_time} seconds")
        
        self.full_transcript.append({"role": "assistant", "content": answer})

        return answer

    def execute_tts(self, answer):
        start_time = time.time()
        self.tts.generateSpeech(answer)
        end_time = time.time()
        print(f"TTS execution time: {end_time - start_time} seconds")


    def end_conversation(self):
        #Calender, Mail ...

        return self.full_transcript