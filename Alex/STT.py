from openai import OpenAI
from dotenv import load_dotenv
import pyaudio
import wave
import os


# 마이크 녹음 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNERLS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNERLS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("start recording...")

frames = []
seconds = 15

for i in range(0, int(RATE / CHUNK * seconds)):
    data = stream.read(CHUNK)
    frames.append(data)

print("recording stopped")

stream.start_stream()
stream.close()
p.terminate()

wf = wave.open("output.wav", 'wb')
wf.setnchannels(CHANNERLS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


# text로 변환
load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

audio_file = open("output.wav", "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    language = ["en","kr"]
)

print(transcription.text)