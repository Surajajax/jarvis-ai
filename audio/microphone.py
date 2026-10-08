import sounddevice as sd
import soundfile as sf

DEVICE = 1
SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 5

print("🎤 Recording for 5 seconds...")
print("Speak normally...")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="float32",
    device=DEVICE
)

sd.wait()

sf.write(
    "data/test_recording.wav",
    audio,
    SAMPLE_RATE
)

print("✅ Recording saved:")
print("data/test_recording.wav")