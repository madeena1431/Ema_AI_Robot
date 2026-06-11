import subprocess


def speak(text):

    print(f"Speaking: {text}")

    try:

        subprocess.run(
            ["say", "--voice=Samantha", "--rate=180", text],
            check=True
        )

    except Exception as e:

        print(f"TTS Error: {e}")


if __name__ == "__main__":

    speak("Hello, I am Emma AI Robot.")