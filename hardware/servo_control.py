from cvzone.SerialModule import SerialObject
from time import sleep

arduino = SerialObject(
    digits=3,
    portNo="/dev/cu.usbmodem1101",
    baudRate=9600
)

last_positions = [0, 0, 90]


def move_servo(target_positions, delay=0.0001):

    global last_positions

    differences = [
        abs(target_positions[i] - last_positions[i])
        for i in range(3)
    ]

    max_step = max(differences)

    if max_step == 0:
        max_step = 1

    for step in range(max_step):

        current = [0, 0, 0]

        for i in range(3):

            diff = target_positions[i] - last_positions[i]

            current[i] = (
                last_positions[i]
                + round((step + 1) * diff / max_step)
            )

        arduino.sendData(current)

        sleep(delay)

    last_positions = target_positions[:]


def hello_gesture():

    base = last_positions[:]

    move_servo([base[0], 180, base[2]])

    for _ in range(3):

        move_servo([base[0], 180, base[2]])
        sleep(0.15)

        move_servo([base[0], 150, base[2]])
        sleep(0.15)

    move_servo([base[0], 0, base[2]])


if __name__ == "__main__":

    print("Running Hardware Demo...")

    move_servo([180, 0, 90])
    sleep(1)

    move_servo([0, 180, 90])
    sleep(1)

    move_servo([90, 90, 90])
    sleep(1)

    print("Executing Hello Gesture...")
    hello_gesture()

    print("Hardware Demo Completed.")