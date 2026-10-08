import torch
import soundfile as sf
from transformers import pipeline


# -----------------------------
# Device
# -----------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Device: {device}")

if device == "cuda":
    print(f"GPU: {torch.cuda.get_device_name(0)}")


# -----------------------------
# Load Whisper
# -----------------------------
print("\nLoading Whisper...")

pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base",
    device=0 if device == "cuda" else -1,
)


# -----------------------------
# Load WAV
# -----------------------------
audio_file = "data/command.wav"

audio, sample_rate = sf.read(audio_file)

print(f"\n🎧 Sample rate: {sample_rate} Hz")
print(f"🎧 Audio length: {len(audio) / sample_rate:.2f} seconds")


# -----------------------------
# Transcribe
# -----------------------------
print("\n🎤 Transcribing...")

result = pipe(
    {
        "raw": audio,
        "sampling_rate": sample_rate,
    },
    generate_kwargs={
        "language": "english",
        "task": "transcribe",
    },
)


# -----------------------------
# Output
# -----------------------------
print("\n==============================")
print("📝 TRANSCRIPTION")
print("==============================")
print(result["text"])
print("==============================")