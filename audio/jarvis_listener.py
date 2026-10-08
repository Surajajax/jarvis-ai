import queue
import time
import wave

import numpy as np
import sounddevice as sd
import webrtcvad
import torch
import soundfile as sf

from openwakeword.model import Model
from transformers import pipeline

from brain.llm import ask_jarvis
from tts.speech import speak


# ==============================
# SETTINGS
# ==============================

SAMPLE_RATE = 16000
CHANNELS = 1
DEVICE = 1

WAKE_CHUNK_SIZE = 1280

VAD_FRAME_MS = 30
VAD_FRAME_SIZE = int(
    SAMPLE_RATE * VAD_FRAME_MS / 1000
)

WAKE_THRESHOLD = 0.5

SILENCE_DURATION = 0.8
SILENCE_FRAMES = int(
    SILENCE_DURATION / (VAD_FRAME_MS / 1000)
)

COMMAND_FILE = "data/command.wav"


# ==============================
# INITIALIZATION
# ==============================

print("================================")
print("🤖 JARVIS INITIALIZING")
print("================================")


# ==============================
# LOAD WAKE WORD MODEL
# ==============================

print("\nLoading wake-word model...")

wake_model = Model(
    inference_framework="onnx"
)

print("✅ Wake-word model loaded.")


# ==============================
# LOAD WHISPER
# ==============================

print("\nLoading Whisper...")

device = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

print(f"Device: {device}")

if device == "cuda":
    print(
        f"GPU: {torch.cuda.get_device_name(0)}"
    )

whisper = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base",
    device=0 if device == "cuda" else -1,
)

print("✅ Whisper loaded.")


# ==============================
# LOAD VAD
# ==============================

vad = webrtcvad.Vad(2)

print("✅ Voice activity detection loaded.")


# ==============================
# READY
# ==============================

print("\n================================")
print("🟢 JARVIS READY")
print("================================")
print('Say "Hey Jarvis"...\n')


# ==============================
# RECORD COMMAND
# ==============================

def record_command():

    print("🎙️ Listening for command...")

    audio_frames = []

    silence_count = 0
    speech_started = False

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=VAD_FRAME_SIZE,
        device=DEVICE,
        channels=CHANNELS,
        dtype="int16",
    ) as stream:

        while True:

            frame, _ = stream.read(
                VAD_FRAME_SIZE
            )

            frame_bytes = bytes(frame)

            is_speech = vad.is_speech(
                frame_bytes,
                SAMPLE_RATE
            )

            if is_speech:

                speech_started = True
                silence_count = 0

                audio_frames.append(
                    frame_bytes
                )

            elif speech_started:

                audio_frames.append(
                    frame_bytes
                )

                silence_count += 1

                if silence_count >= SILENCE_FRAMES:
                    break

    # Save command audio
    with wave.open(
        COMMAND_FILE,
        "wb"
    ) as wf:

        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)

        wf.writeframes(
            b"".join(audio_frames)
        )

    print("🛑 Command finished.")

    return COMMAND_FILE


# ==============================
# WHISPER TRANSCRIPTION
# ==============================

def transcribe(audio_file):

    audio, sample_rate = sf.read(
        audio_file
    )

    result = whisper(
        {
            "raw": audio,
            "sampling_rate": sample_rate,
        },
        generate_kwargs={
            "language": "english",
            "task": "transcribe",
        },
    )

    return result["text"].strip()


# ==============================
# WAKE WORD AUDIO QUEUE
# ==============================

audio_queue = queue.Queue()


def audio_callback(
    indata,
    frames,
    time_info,
    status
):

    if status:

        print(
            f"Audio status: {status}"
        )

    audio_queue.put(
        indata.copy()
    )


# ==============================
# MAIN JARVIS LOOP
# ==============================

try:

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        blocksize=WAKE_CHUNK_SIZE,
        device=DEVICE,
        callback=audio_callback,
    ):

        while True:

            # Get microphone audio
            audio = audio_queue.get()

            audio = np.squeeze(audio)

            # Check wake word
            prediction = wake_model.predict(
                audio
            )

            score = prediction.get(
                "hey_jarvis",
                0.0
            )

            # ==============================
            # WAKE WORD DETECTED
            # ==============================

            if score >= WAKE_THRESHOLD:

                print(
                    f"\n🔥 HEY JARVIS DETECTED!"
                    f" Score: {score:.2f}"
                )

                # Reset wake-word model
                # to prevent repeated detection.
                wake_model.reset()

                # Give the wake-word audio
                # time to finish.
                time.sleep(0.8)

                # ==============================
                # RECORD USER COMMAND
                # ==============================

                command_file = record_command()

                # ==============================
                # TRANSCRIBE
                # ==============================

                print("\n🧠 Transcribing...")

                text = transcribe(
                    command_file
                )

                # Ignore empty transcription
                if not text:

                    print(
                        "⚠️ No speech detected."
                    )

                    print(
                        '\n🟢 Listening for "Hey Jarvis"...\n'
                    )

                    continue

                # ==============================
                # SHOW USER COMMAND
                # ==============================

                print(
                    "\n=============================="
                )

                print(
                    "📝 YOU SAID"
                )

                print(
                    "=============================="
                )

                print(text)

                print(
                    "=============================="
                )

                # ==============================
                # ASK JARVIS
                # ==============================

                print(
                    "\n🧠 JARVIS THINKING..."
                )

                response = ask_jarvis(
                    text
                )

                # ==============================
                # SHOW JARVIS RESPONSE
                # ==============================

                print(
                    "\n=============================="
                )

                print(
                    "🤖 JARVIS"
                )

                print(
                    "=============================="
                )

                print(response)

                print(
                    "==============================\n"
                )

                # ==============================
                # SPEAK RESPONSE
                # ==============================

                speak(response)

                # ==============================
                # LISTEN AGAIN
                # ==============================

                print(
                    '\n🟢 Listening for "Hey Jarvis"...\n'
                )


# ==============================
# STOP JARVIS
# ==============================

except KeyboardInterrupt:

    print(
        "\n\n🛑 JARVIS stopped."
    )
