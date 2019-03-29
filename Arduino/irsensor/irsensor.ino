//import the library in the sketch
#include <SharpIR.h>

//Create a new instance of the library
//Call the sensor "sensor"
//The model of the sensor is "GP2YA41SK0F"
//The sensor output pin is attached to the pin A0
SharpIR sensorFrontRight( SharpIR:: GP2Y0A21YK0F, A0);
SharpIR sensorFrontLeft( SharpIR:: GP2Y0A21YK0F, A1);
SharpIR sensorLongRight( SharpIR:: GP2Y0A02YK0F, A2);
SharpIR sensorFrontMiddle( SharpIR:: GP2Y0A21YK0F, A3);
SharpIR sensorLeftBack( SharpIR:: GP2Y0A21YK0F, A4);
SharpIR sensorLeftFront( SharpIR:: GP2Y0A21YK0F, A5);

void setup()
{
  Serial.begin( 9600 ); //Enable the serial comunication
}

void loop()
{
  //double volFR = analogRead(A0); //Calculate the distance in centimeters and store the value in a variable
  //Serial.print("Voltage Front Right ");
  //Serial.println(volFR); //Print the value to the serial monitor
  /*int disFR = sensorFrontRight.getDistance();
  Serial.print("Distance Front Right ");
  Serial.println(disFR);
  int disFL = sensorFrontLeft.getDistance(); //Calculate the distance in centimeters and store the value in a variable
  Serial.print("Distance Front Left ");
  Serial.println(disFL); //Print the value to the serial monitor*/
  int disLR = sensorLongRight.getDistance(); //Calculate the distance in centimeters and store the value in a variable
  Serial.print("Distance Long Right ");
  Serial.println(disLR); //Print the value to the serial monitor
  double volLR = analogRead(A2);
  Serial.println(volLR);
  /*int disFM = sensorFrontMiddle.getDistance(); //Calculate the distance in centimeters and store the value in a variable
  Serial.print("Distance Front Middle ");
  Serial.println(disFM); //Print the value to the serial monitor
  int disLB = sensorLeftBack.getDistance(); //Calculate the distance in centimeters and store the value in a variable
  Serial.print("Distance Left Back ");
  Serial.println(disLB); //Print the value to the serial monitor
  int disLF = sensorLeftFront.getDistance(); //Calculate the distance in centimeters and store the value in a variable
  Serial.print("Distance Left Front ");
  Serial.println(disLF); //Print the value to the serial monitor*/
  delay(1000);
}
