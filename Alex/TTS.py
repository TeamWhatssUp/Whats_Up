from pathlib import Path
import openai

speech_file_path = Path(__file__).parent / "speech.mp3"
response = openai.audio.speech.create(
    model="tts-1-hd",

    # voice list(alloy, ash, coral, echo, fable, onyx, nova, sage, shimmer)
    voice="alloy",

    # max input = 4096
    input=""
)
response.stream_to_file(speech_file_path)
