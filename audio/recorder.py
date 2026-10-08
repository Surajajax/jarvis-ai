import collections
import wave

import webrtcvad
import sounddevice as sd


SAMPLE_RATE = 16000
CHANNELS = 1

FRAME_DURATION_MS = 30
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)

DEVICE = 1

SILENCE_DURATION = 0.8
SILENCE_FRAMES = int(SILENCE_DURATION / (FRAME_DURATION_MS / 1000))


def record_command(output_file="data/command.wav"):
    vad = webrtcvad.Vad(2)

    print("\n🎙️ Listening for your command...")
    print("Speak now...")

    audio_frames = []

    silence_count = 0
    speech_started = False

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=FRAME_SIZE,
        device=DEVICE,
        channels=CHANNELS,
        dtype="int16",
    ) as stream:

        while True:
            frame, _ = stream.read(FRAME_SIZE)

            frame_bytes = bytes(frame)

            is_speech = vad.is_speech(
                frame_bytes,
                SAMPLE_RATE
            )

            if is_speech:
                speech_started = True
                silence_count = 0
                audio_frames.append(frame_bytes)

            elif speech_started:
                audio_frames.append(frame_bytes)

                silence_count += 1

                if silence_count >= SILENCE_FRAMES:
                    break

    print("🛑 Command finished.")

    with wave.open(output_file, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(audio_frames))

    print(f"💾 Command saved: {output_file}")


if __name__ == "__main__":
    record_command()