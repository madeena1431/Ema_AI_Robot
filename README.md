# Emma AI Robot

Emma AI Robot is an AI-powered talking robot that combines speech recognition, artificial intelligence, text-to-speech, and hardware movement into a single interactive system. The project was developed to explore how software and hardware components can work together to create a conversational robot capable of listening, understanding, responding, and performing physical gestures.

The project is divided into separate folders for software testing, hardware testing, resources, and Arduino control. Each module can be executed independently for learning and testing purposes, while the complete robot system is executed through the main.py file.

## Required Python Libraries:

Before running the project, install the required libraries:

groq
pyaudio
pygame
cvzone
pyserial

## Main Program:

1. main.py

---

Purpose:

This is the complete Emma AI Robot system. It combines all major functionalities into a single application.

The program performs the following tasks:

• Establishes communication with the Arduino board.

• Controls the robot's servo motors.

• Calibrates the microphone based on environmental noise.

• Detects speech using Voice Activity Detection (VAD).

• Records audio from the microphone.

• Converts speech into text using Groq Whisper.

• Sends the recognized text to the Groq Llama AI model.

• Receives an AI-generated response.

• Converts the response into spoken audio using Text-to-Speech.

• Detects greeting words such as:

* Hello
* Hi
* Hey
* Greetings
* Howdy
* Emma

• Executes a Hello Gesture whenever a greeting is detected.

• Provides audio feedback using notification sounds while listening and processing speech.

## Workflow:

User Speaks
↓
Microphone Records Audio
↓
Groq Whisper Converts Speech to Text
↓
Groq Llama Generates Response
↓
Text-to-Speech Speaks Response
↓
Robot Performs Gesture (if applicable)

## Running the Complete Robot:

Execute the following command:

python main.py

When the program starts, the robot initializes the servos, calibrates the microphone, and waits for voice input.

## Project Structure:

Emma-AI-Robot/

├── main.py

├── Arduino/
│   ├── talking_ai_robot.ino
│   └── readme.md

├── hardware/
│   ├── servo_control.py
│   └── readme.md

├── software/
│   ├── speech_to_text.py
│   ├── text_to_speech.py
│   ├── ai_model.py
│   └── readme.md

├── Resources/
│   ├── listen.mp3
│   ├── convert.mp3
│   └── readme.md

├── requirements.txt

└── README.md

## Summary of Learning:

• Learned microphone audio processing and Voice Activity Detection.

• Learned speech recognition using Groq Whisper.

• Learned AI response generation using Groq Llama models.

• Learned text-to-speech synthesis.

• Learned serial communication between Python and Arduino.

• Learned servo motor control and gesture design.

• Learned how to integrate multiple software and hardware components into a complete robotic system.

Emma AI Robot represents the final integration of all individual experiments and modules into a fully functional conversational robot capable of listening, thinking, speaking, and performing physical actions.

# ----------------------------------------------------------------------------------

Platform Notes
--------------

This project was developed and tested on macOS.

The Text-to-Speech module uses the built-in macOS `say` command:

subprocess.run(["say", "--voice=Samantha", "--rate=180", text])

Linux and Windows users may need to replace this implementation with an alternative Text-to-Speech library such as:

• pyttsx3
• gTTS
• edge-tts

All other modules are platform-independent provided the required dependencies are installed correctly.