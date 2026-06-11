# Software Folder - Emma AI Robot

This Software folder contains the three Python programs that I created and tested individually while developing the software features of the Emma AI Robot project. These files were separated from the main project so that each feature could be verified independently before being used inside the complete robot system.

All files inside this folder can be executed separately using:

python filename.py

Before running these programs, the following Python libraries should be installed:

groq
pyaudio
pygame

This folder contains the following files:

1. ai_model.py

---

Purpose:

This program is used to communicate with the Groq AI model. It accepts a text query from the user and sends it to the Llama language model through the Groq API. The generated response is then displayed in the terminal. This file helped me test whether the AI response generation works correctly before integrating it into the robot.

Running command used:

python ai_model.py

2. speech_to_text.py

---

Purpose:

This program is used to convert spoken voice into text using Groq Whisper speech recognition. It listens through the microphone, records the user's speech, and sends the recorded audio to the Whisper model for transcription. The recognized text is displayed in the terminal. This helped me verify microphone input, audio processing, and speech recognition separately from the robot.

Running command used:

python speech_to_text.py

3. text_to_speech.py

---

Purpose:

This program is used to convert text into spoken audio. It uses the built-in speech engine available on the system to generate voice output. When executed, the program speaks a predefined message through the speakers. This helped me verify that speech output works correctly before integrating it into the full robot project.

Running command used:

python text_to_speech.py

## Summary of learning:

• ai_model.py helped me practice AI response generation using Groq Llama models

• speech_to_text.py helped me practice speech recognition using Groq Whisper

• text_to_speech.py helped me practice voice output generation

All these codes are independent software demonstrations. After verifying these features separately, they were combined inside the main.py file to create the complete Emma AI Robot system.
