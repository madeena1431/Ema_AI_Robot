import pyaudio
import subprocess
import pygame
from groq import Groq
from cvzone.SerialModule import SerialObject
from time import sleep
import os
import audioop
import wave
import io

# ── Arduino ────────────────────────────────────────────────────────────────────
arduino        = SerialObject(digits=3, portNo='''PORT NO''', baudRate=9600)
last_positions = [0, 0, 90]

# ── Pygame ─────────────────────────────────────────────────────────────────────
pygame.mixer.init()

# ── Audio settings ─────────────────────────────────────────────────────────────
SAMPLE_RATE = 16000
CHUNK_SIZE  = 1024
CHANNELS    = 1
FORMAT      = pyaudio.paInt16

# ── Groq client (used for both LLM + Whisper STT) ─────────────────────────────
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

# ── Keywords that trigger the greeting gesture ─────────────────────────────────
HI_WORDS = {"hello", "hi", "hey", "greetings", "howdy", "emma"}

# ── Mic mute flag ──────────────────────────────────────────────────────────────
is_speaking = False

# ── Voice activity detection settings ─────────────────────────────────────────
SILENCE_THRESHOLD = 500   # RMS — will be auto-calibrated below
MAX_SILENT_CHUNKS = 30    # ~0.5 s of silence after speech = done
MIN_SPEECH_CHUNKS = 5     # minimum chunks to count as real speech (not a click)

# --- Resources ---------------


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LISTEN_SOUND = os.path.join(BASE_DIR, "Resources", "listen.mp3")
CONVERT_SOUND = os.path.join(BASE_DIR, "Resources", "convert.mp3")


# ───────────────────────────────────────────────────────────────────────────────
# Mic calibration
# ───────────────────────────────────────────────────────────────────────────────

def calibrate_mic():
    print("Calibrating mic... please stay quiet for 2 seconds.")
    mic    = pyaudio.PyAudio()
    stream = mic.open(format=FORMAT, channels=CHANNELS,
                      rate=SAMPLE_RATE, input=True,
                      frames_per_buffer=CHUNK_SIZE)
    stream.start_stream()

    rms_values = []
    num_chunks = int(SAMPLE_RATE / CHUNK_SIZE * 2)
    for _ in range(num_chunks):
        data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
        rms_values.append(audioop.rms(data, 2))

    stream.stop_stream()
    stream.close()
    mic.terminate()

    noise_floor = sum(rms_values) / len(rms_values)
    threshold   = int(noise_floor * 2.0)   # 2x headroom for noisy environments
    threshold   = max(threshold, 100)
    print(f"Noise floor RMS: {int(noise_floor)}  ->  Threshold set to: {threshold}")
    return threshold

SILENCE_THRESHOLD = calibrate_mic()


# ───────────────────────────────────────────────────────────────────────────────
# Sound effects
# ───────────────────────────────────────────────────────────────────────────────

def play_sound(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(5)
    except Exception as e:
        print(f"Sound error: {e}")


# ──────────────────────────────────────────────────────────────────────────────
# TTS
# ──────────────────────────────────────────────────────────────────────────────

def speak(text):
    global is_speaking
    is_speaking = True
    print(f"Speaking: {text}")
    try:
        subprocess.run(
            ["say", "--voice=Samantha", "--rate=180", text],
            check=True
        )
    except Exception as e:
        print(f"TTS error: {e}")
    finally:
        is_speaking = False


# ───────────────────────────────────────────────────────────────────────────────
# STT — Record audio locally, send to Groq Whisper online
# ───────────────────────────────────────────────────────────────────────────────

def record_until_silence():
    """
    Records audio from mic using energy-based VAD.
    Starts capturing when voice is detected above threshold.
    Stops after MAX_SILENT_CHUNKS of silence following speech.
    Returns raw PCM frames as a list.
    """
    global is_speaking

    mic    = pyaudio.PyAudio()
    stream = mic.open(format=FORMAT, channels=CHANNELS,
                      rate=SAMPLE_RATE, input=True,
                      frames_per_buffer=CHUNK_SIZE)
    stream.start_stream()

    # Drain stale OS buffer
    for _ in range(8):
        stream.read(CHUNK_SIZE, exception_on_overflow=False)

    print("\nListening...")
    play_sound(listen_sound)
    
    frames          = []
    speech_detected = False
    silent_chunks   = 0
    speech_chunks   = 0

    try:
        while True:
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)

            if is_speaking:
                continue

            rms = audioop.rms(data, 2)

            if rms >= SILENCE_THRESHOLD:
                # Voice detected
                speech_detected = True
                silent_chunks   = 0
                speech_chunks  += 1
                frames.append(data)
                print(f"Recording... (RMS: {rms})   ", end="\r")

            else:
                if speech_detected:
                    # Trailing silence — still append so Whisper hears natural ending
                    frames.append(data)
                    silent_chunks += 1
                    if silent_chunks >= MAX_SILENT_CHUNKS:
                        # Done speaking
                        break

    finally:
        stream.stop_stream()
        stream.close()
        mic.terminate()

    # Ignore accidental clicks / very short noise bursts
    if speech_chunks < MIN_SPEECH_CHUNKS:
        return None

    return frames


def frames_to_wav_bytes(frames):
    """Convert raw PCM frames into an in-memory WAV file (bytes)."""
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)          # paInt16 = 2 bytes
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(frames))
    buf.seek(0)
    return buf.read()


def transcribe_with_whisper(wav_bytes):
    """Send WAV bytes to Groq Whisper API and return transcribed text."""
    try:
        # Groq expects a file-like object with a name ending in .wav
        audio_file = io.BytesIO(wav_bytes)
        audio_file.name = "audio.wav"

        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file,
            language="en",
            response_format="text"
        )
        # When response_format="text", Groq returns a plain string directly
        return transcription.strip() if isinstance(transcription, str) else transcription.text.strip()

    except Exception as e:
        print(f"Whisper API error: {e}")
        return ""


def listen_with_whisper():
    """Full pipeline: record → encode → transcribe online via Groq Whisper."""
    frames = record_until_silence()

    if not frames:
        print("No speech detected, listening again...")
        return ""

    print("\nTranscribing...")
    wav_bytes = frames_to_wav_bytes(frames)
    result    = transcribe_with_whisper(wav_bytes)

    if result:
        print(f"You said: {result}")
        play_sound(convert_sound)
    else:
        print("Could not transcribe. Please try again.")

    return result


# ───────────────────────────────────────────────────────────────────────────────
# Groq LLM
# ───────────────────────────────────────────────────────────────────────────────

def groq_response(text):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": text}]
        )
        reply = response.choices[0].message.content
        print(f"AI: {reply}")
        return reply
    except Exception as e:
        print(f"Groq error: {e}")
        return "Sorry, I could not reach the AI right now."


# ───────────────────────────────────────────────────────────────────────────────
# Servo control — UNCHANGED
# ───────────────────────────────────────────────────────────────────────────────

def move_servo(target_positions, delay=0.0001):
    global last_positions
    differences = [abs(target_positions[i] - last_positions[i]) for i in range(3)]
    max_step    = max(differences) if max(differences) > 0 else 1
    for step in range(max_step):
        current = [0, 0, 0]
        for i in range(3):
            diff       = target_positions[i] - last_positions[i]
            current[i] = last_positions[i] + round((step + 1) * diff / max_step)
        arduino.sendData(current)
        sleep(delay)
    last_positions = target_positions[:]


def hello_gesture():
    base = last_positions[:]
    move_servo([base[0], 180, base[2]])
    for _ in range(3):
        move_servo([base[0], 180, base[2]])
        sleep(0.15)
        move_servo([base[0], 150, base[2]])
        sleep(0.15)
    move_servo([base[0], 0, base[2]])


# ───────────────────────────────────────────────────────────────────────────────
# Startup
# ───────────────────────────────────────────────────────────────────────────────
sleep(1)
move_servo([180, 0, 90], delay=0.0001)
print("Robot ready. Say something!")

# ───────────────────────────────────────────────────────────────────────────────
# Main loop
# ───────────────────────────────────────────────────────────────────────────────
while True:
    try:
        move_servo([180, 0, 90], delay=0.0001)
        text = listen_with_whisper()

        if not text.strip():
            continue

        # Strip punctuation from each word before matching
        # Whisper often returns "Hi!" or "Hello." which breaks exact matching
        import re
        words = set(re.sub(r'[^\w\s]', '', text.lower()).split())
        if any(word in words for word in HI_WORDS):
            print("Triggering Hello Gesture...")
            sleep(0.3)
            hello_gesture()
            speak("Hello! How can I assist you today?")
        else:
            print(f"Processing: {text}")
            ai_reply = groq_response(text)
            if ai_reply:
                speak(ai_reply)

    except KeyboardInterrupt:
        print("\nStopping robot. Bye!")
        break
    except Exception as e:
        print(f"Error: {e}")
        sleep(1)
