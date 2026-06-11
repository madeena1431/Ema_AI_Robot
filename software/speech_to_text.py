import pyaudio
import audioop
import wave
import io
import os

from groq import Groq

SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
CHANNELS = 1
FORMAT = pyaudio.paInt16

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

MAX_SILENT_CHUNKS = 30
MIN_SPEECH_CHUNKS = 5


def calibrate_mic():

    print("Calibrating microphone...")

    mic = pyaudio.PyAudio()

    stream = mic.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE
    )

    rms_values = []

    num_chunks = int(
        SAMPLE_RATE / CHUNK_SIZE * 2
    )

    for _ in range(num_chunks):

        data = stream.read(
            CHUNK_SIZE,
            exception_on_overflow=False
        )

        rms_values.append(
            audioop.rms(data, 2)
        )

    stream.stop_stream()
    stream.close()
    mic.terminate()

    noise_floor = (
        sum(rms_values) / len(rms_values)
    )

    threshold = int(noise_floor * 2)

    threshold = max(threshold, 100)

    print(f"Threshold = {threshold}")

    return threshold


SILENCE_THRESHOLD = calibrate_mic()


def record_until_silence():

    mic = pyaudio.PyAudio()

    stream = mic.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE
    )

    frames = []

    speech_detected = False
    silent_chunks = 0
    speech_chunks = 0

    print("Listening...")

    try:

        while True:

            data = stream.read(
                CHUNK_SIZE,
                exception_on_overflow=False
            )

            rms = audioop.rms(data, 2)

            if rms >= SILENCE_THRESHOLD:

                speech_detected = True
                silent_chunks = 0
                speech_chunks += 1

                frames.append(data)

            else:

                if speech_detected:

                    frames.append(data)

                    silent_chunks += 1

                    if silent_chunks >= MAX_SILENT_CHUNKS:
                        break

    finally:

        stream.stop_stream()
        stream.close()
        mic.terminate()

    if speech_chunks < MIN_SPEECH_CHUNKS:
        return None

    return frames


def frames_to_wav_bytes(frames):

    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wf:

        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)

        wf.writeframes(
            b"".join(frames)
        )

    buffer.seek(0)

    return buffer.read()


def transcribe_with_whisper(wav_bytes):

    try:

        audio_file = io.BytesIO(wav_bytes)

        audio_file.name = "audio.wav"

        transcription = (
            client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file,
                language="en",
                response_format="text"
            )
        )

        if isinstance(transcription, str):
            return transcription.strip()

        return transcription.text.strip()

    except Exception as e:

        print(f"Whisper Error: {e}")

        return ""


def listen_with_whisper():

    frames = record_until_silence()

    if not frames:
        return ""

    wav_bytes = frames_to_wav_bytes(frames)

    return transcribe_with_whisper(
        wav_bytes
    )


if __name__ == "__main__":

    print("Speech Recognition Demo")

    text = listen_with_whisper()

    print("\nDetected Text:\n")

    print(text)