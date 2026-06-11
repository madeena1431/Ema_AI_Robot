# Arduino Folder - Emma AI Robot

This Arduino folder contains the Arduino program responsible for controlling the physical movements of the Emma AI Robot. The Arduino board receives servo angle values from the Python application through serial communication and moves the robot's servo motors accordingly.

The Arduino program works together with the Python files in the project. The Python application calculates the required servo positions and sends them to the Arduino, while the Arduino executes the actual motor movement.

Before uploading this program, the following Arduino libraries should be installed:

cvzone

Servo

This folder contains the following file:

1. talking_ai_robot.ino

---

Purpose:

This program is responsible for receiving servo angle values from the Python application and controlling the robot's three servo motors.

The program performs the following tasks:

• Establishes serial communication between Arduino and Python.

• Receives servo angle values sent from the computer.

• Stores the received values inside an array.

• Controls the Left Servo, Right Servo, and Head Servo.

• Updates servo positions continuously based on commands received from the Python application.

## Servo Connections:

Left Servo  (LServo)  → Pin 8

Right Servo (RServo)  → Pin 9

Head Servo  (HServo)  → Pin 10

## Communication Process:

Python Application
↓
Serial Communication (9600 baud)
↓
Arduino Receives Angle Values
↓
Servo Motors Move To Requested Position

## Data Format:

The Python application sends a list containing three servo angles:

[LServo, RServo, HServo]

Example:

[180, 0, 90]

Where:

• 180 = Left Servo Angle

• 0 = Right Servo Angle

• 90 = Head Servo Angle

The Arduino receives these values and immediately updates the servo positions.

## Uploading the Program:

1. Connect the Arduino board to the computer.

2. Open talking_ai_robot.ino in the Arduino IDE.

3. Install the required libraries if not already installed.

4. Select the correct board and COM/USB port.

5. Upload the sketch to the Arduino.

After uploading, the Arduino will continuously wait for servo commands from the Python application.

## Summary of Learning:

• Learned serial communication between Python and Arduino.

• Learned how to receive structured data using the cvzone SerialData library.

• Learned servo motor control using the Servo library.

• Learned how software and hardware interact in a robotics project.

• Learned how to control multiple servo motors simultaneously.

This Arduino program acts as the hardware controller of the Emma AI Robot. It receives movement instructions from the Python application and converts them into physical robot movements.
