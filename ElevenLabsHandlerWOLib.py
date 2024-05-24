import os, requests, time, json, base64
from elevenlabs import play
from interfaces import TextToSpeech
import subprocess, shutil
from typing import Iterator

import asyncio 
import websockets

class ElevenLabsHandlerWOLib(TextToSpeech):
    def __init__(self, model_id, voice_id):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
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
    
    async def streamAudioAsync(self, audio_stream: Iterator[bytes]) -> bytes:
        firstBit = False
        """Stream audio data using mpv player."""
        if shutil.which("mpv") is None:
            raise ValueError(
                "mpv not found, necessary to stream audio. "
                "Install instructions: https://mpv.io/installation/"
            )

        mpv_process = subprocess.Popen(
            ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"],
            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

        print("Started streaming audio")
        async for chunk in audio_stream:
            if chunk:
                if not firstBit:
                    self.time = time.time() - self.time
                    firstBit = True
                mpv_process.stdin.write(chunk)
                mpv_process.stdin.flush()

        if mpv_process.stdin:
            mpv_process.stdin.close()
        mpv_process.wait()

    def is_installed(self, lib_name: str) -> bool:
        lib = shutil.which(lib_name)
        if lib is None:
            return False
        return True
    
    async def text_to_speech_input_streaming(self, text_iterator):
        """Send text to ElevenLabs API and stream the returned audio."""
        uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream-input?model_id=eleven_multilingual_v2"

        self.time = time.time()

        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps({
                "text": " ",
                "model": "eleven_multilingual_v2",
                #"voice_settings": {"stability": 0.5, "similarity_boost": 0.8},
                "xi_api_key": self.api_key,
            }))

            async def listen():
                """Listen to the websocket for audio data and stream it."""
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        if data.get("audio"):
                            yield base64.b64decode(data["audio"])
                        elif data.get('isFinal'):
                            break
                    except websockets.exceptions.ConnectionClosed:
                        print("Connection closed")
                        break

            listen_task = asyncio.create_task(self.streamAudioAsync(listen()))

            async for text in self.text_chunker(text_iterator):
                await websocket.send(json.dumps({"text": text, "try_trigger_generation": True}))

            await websocket.send(json.dumps({"text": ""}))

            await listen_task

    async def text_chunker(self, chunks):
        """Split text into chunks, ensuring to not break sentences."""
        splitters = (".", ",", "?", "!", ";", ":", "—", "-", "(", ")", "[", "]", "}", " ")
        buffer = ""

        async for text in chunks:
            if buffer.endswith(splitters):
                yield buffer + " "
                buffer = text
            elif text.startswith(splitters):
                yield buffer + text[0] + " "
                buffer = text[1:]
            else:
                buffer += text

        if buffer:
            yield buffer + " "

    def playAudio(self, audio_path):
        with open(audio_path, "rb") as audio:
            audio_content = audio.read()
            play(audio_content)