from openai import OpenAI
from dotenv import load_dotenv
import pyaudio
import wave
import os




class AudioRecorder:
    def __init__(self, chunk=1024, format=pyaudio.paInt16, channels=1, rate=44100, duration=15, output_filename="output.wav"):
        self.CHUNK = chunk
        self.FORMAT = format
        self.CHANNELS = channels
        self.RATE = rate
        self.DURATION = duration
        self.output_filename = output_filename
        self.frames = []
        self.p = pyaudio.PyAudio()

    def record(self):
        stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
            )

        for _ in range(0, int(self.RATE / self.CHUNK * self.DURATION)):
            data = stream.read(self.CHUNK)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()

    def save(self):
        wf = wave.open(self.output_filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def terminate(self):
        self.p.terminate()



class AudioTranscriber:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

    def transcribe(self, model="whisper-1", language=["en", "kr"]):
        with open("recording.wav", "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                language=language,
            )
        return transcription



recorder = AudioRecorder(
        chunk=1024,              # Number of audio samples per chunk
        format=pyaudio.paInt16,  # Format of audio (16-bit PCM)
        channels=1,              # Number of audio channels (mono)
        rate=44100,              # Sampling rate in Hz
        duration=10,             # Duration of the recording in seconds
        output_filename="recording.wav"  # File to save the recording
    )



# 사용방법
recorder.record()
print("Start recording")
recorder.save()
recorder.terminate()
print("Recording has been saved to 'recording.wav'.")

transcriber = AudioTranscriber()
print("Starting transcription...")
result = transcriber.transcribe(model="whisper-1", language=["en", "kr"])
print(result.text)




