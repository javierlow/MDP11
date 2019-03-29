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
  delay(5000);
  Serial.begin( 9600 ); //Enable the serial comunication
}

void loop()
{
    //double vol = analogRead(A0); //Calculate the distance in centimeters and store the value in a variable
    //Serial.println(vol); //Print the value to the serial monitor
    //double disFL = sensorFrontLeft.getDistance();
    //Serial.println(disFL);
    //double disFM = sensorFrontMiddle.getDistance();
    //Serial.println(disFM);
    //double disFR = sensorFrontRight.getDistance();
    //Serial.println(disFR);
    double disLB = sensorLeftBack.getDistance();
    Serial.println(disLB);
    double disLF = sensorLeftFront.getDistance();
    Serial.println(disLF);
    delay(1000);
}
