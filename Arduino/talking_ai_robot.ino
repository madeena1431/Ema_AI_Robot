
//emma code
#include <cvzone.h>
#include <Servo.h>

//declaration of servo objects
Servo LServo;
Servo RServo;
Servo HServo;

//define 
const int LS_Pin = 8;
const int RS_Pin = 9; 
const int HS_Pin = 10;

//Initialize serial data to recive 3 values and each value contain 3 digits
SerialData serialData(3 , 3); //python codes send angle
int valsRec[3]; //Array to store the 3 received values for each servo motor [(0 , 0 , 100)] -->degrees

void setup(){
  Serial.begin(9600); //start serial communication at baurd rate of 9600
  serialData.begin();  //Initialize the serial Data communication

  //Attach servo to their respective pins.
  LServo.attach(LS_Pin);
  RServo.attach(RS_Pin);
  HServo.attach(HS_Pin);
}

void loop(){
   //python sends in list of angles : [LServo,RServo,HServo]
   serialData.Get(valsRec);
   LServo.write(valsRec[0]);
   RServo.write(valsRec[1]);
   HServo.write(valsRec[2]);

}

