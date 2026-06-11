# Hardware Folder - Emma AI Robot

This Hardware folder contains the Python program that I used to test and control the physical movements of the Emma AI Robot. The purpose of this file is to verify that communication between the computer and the Arduino works correctly and that the robot's servo motors move as expected.

The program inside this folder can be executed independently using:

python servo_control.py

Before running this program, the following Python libraries should be installed:

cvzone
pyserial

This folder contains the following file:

1. servo_control.py

---

Purpose:

This program is responsible for communicating with the Arduino and controlling the robot's servo motors. It contains the functions used to move servos smoothly between positions and also includes the Hello Gesture used by the robot when a greeting is detected.

The file can be executed independently to test hardware movement without running the complete AI system. This helped me verify servo control and gesture execution separately from speech recognition and AI processing.

Running command used:

python servo_control.py

## Summary of learning:

• Learned serial communication between Python and Arduino

• Learned smooth servo motor control

• Learned gesture creation using coordinated servo movement

• Verified hardware functionality independently before integrating with the complete robot

This code focuses only on robot movement and hardware communication. After successful testing, these functions were used inside the complete Emma AI Robot system.
