import subprocess
import tempfile
import os
import sys


VOICE = "en_US-lessac-medium"


def speak(text):

    print(f"\n🔊 JARVIS: {text}")

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as temp:

        output_file = temp.name

    try:

        process = subprocess.run(
            [
                sys.executable,
                "-m",
                "piper",
                "-m",
                VOICE,
                "-f",
                output_file,
            ],
            input=text,
            text=True,
            capture_output=True,
        )

        if process.returncode != 0:

            print("❌ Piper error:")
            print(process.stderr)

            return

        # Play the generated WAV.
        subprocess.run(
            [
                "powershell",
                "-Command",
                f'(New-Object Media.SoundPlayer "{output_file}").PlaySync()'
            ],
            capture_output=True,
        )

    finally:

        if os.path.exists(output_file):
            os.remove(output_file)


if __name__ == "__main__":

    print("🤖 Testing JARVIS voice...")

    speak(
        "Hello. I am Jarvis. "
        "Your local AI assistant is now online."
    )