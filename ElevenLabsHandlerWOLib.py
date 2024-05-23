import os, requests, time
from elevenlabs import play
#from elevenlabs.client import ElevenLabs
from interfaces import TextToSpeech
import subprocess, shutil
from typing import Iterator

class ElevenLabsUtilsWOLib(TextToSpeech):
    def __init__(self, model_id, voice_id):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        #self.client = ElevenLabs(api_key=self.api_key)
        self.model_id = model_id
        self.voice_id = voice_id
        self.time = -1

    def generateSpeech(self, text):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"

        headers = {
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

        data = {
            "text": text,
            "model_id": self.model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        self.time = time.time()

        response = requests.post(
            url,
            json=data,
            headers=headers,
            stream=True
        )

        if response.status_code != 200:
            print(f"Error encountered, status: {response.status_code}, "
                    f"content: {response.text}")
            quit()


        self.streamAudio(response.iter_content())


    def streamAudio(self, audio_stream: Iterator[bytes]) -> bytes:
        if not self.is_installed("mpv"):
            message = (
                "mpv not found, necessary to stream audio. "
                "On mac you can install it with 'brew install mpv'. "
                "On linux and windows you can install it from https://mpv.io/"
            )
            raise ValueError(message)

        mpv_command = ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"]
        mpv_process = subprocess.Popen(
            mpv_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        audio = b""
        firstBit = False

        for chunk in audio_stream:
            if chunk is not None:
                if not firstBit:
                    self.time = time.time() - self.time
                    firstBit = True
                mpv_process.stdin.write(chunk)  # type: ignore
                mpv_process.stdin.flush()  # type: ignore
                audio += chunk
        if mpv_process.stdin:
            mpv_process.stdin.close()
        mpv_process.wait()

        return audio

    def is_installed(self, lib_name: str) -> bool:
        lib = shutil.which(lib_name)
        if lib is None:
            return False
        return True
    
    def playAudio(self, audio_path):
        with open(audio_path, "rb") as audio:
            audio_content = audio.read()
            play(audio_content)