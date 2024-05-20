import pyaudio

def start_audio_stream():
    p = pyaudio.PyAudio()
    return p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

def read_audio_data(stream, chunk_size=4000):
    while True:
        try:
            data = stream.read(chunk_size)
            return data if data is not None else ""  # Return an empty string if data is None
        except OSError as e:
            if e.errno == -9981:  # Input overflowed
                continue  # Try reading from the buffer again
            else:
                raise  # Re-raise the exception if it's not an input overflow
