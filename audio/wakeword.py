import queue

import numpy as np
import sounddevice as sd

from openwakeword.model import Model


SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1280

# Your laptop microphone
DEVICE = 1

# Wake-word sensitivity
THRESHOLD = 0.5


audio_queue = queue.Queue()


def audio_callback(indata, frames, time, status):
    if status:
        print(f"Audio status: {status}")

    audio_queue.put(indata.copy())


print("Loading openWakeWord...")

model = Model(
    inference_framework="onnx"
)

print("Wake-word model loaded.")
print('🎧 Listening for "Hey Jarvis"...')
print("Press Ctrl+C to stop.\n")


try:

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        blocksize=CHUNK_SIZE,
        device=DEVICE,
        callback=audio_callback,
    ):

        while True:

            audio = audio_queue.get()

            # Convert:
            # (1280, 1) → (1280,)
            audio = np.squeeze(audio)

            # Run prediction
            prediction = model.predict(audio)

            score = prediction.get("hey_jarvis", 0.0)

            if score >= THRESHOLD:

                print(
                    f"🔥 HEY JARVIS DETECTED! "
                    f"Score: {score:.2f}"
                )

                # Prevent immediate repeated detection
                model.reset()

except KeyboardInterrupt:

    print("\n🛑 Wake-word listener stopped.")