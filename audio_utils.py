import pyaudio

def start_audio_stream():
    p = pyaudio.PyAudio()
    return p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

def read_audio_data(stream, chunk_size=4000):
    return stream.read(chunk_size)
