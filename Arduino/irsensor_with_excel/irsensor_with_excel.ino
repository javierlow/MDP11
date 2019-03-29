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
  Serial.begin(9600); //Enable the serial comunication
  Serial.println("CLEARDATA"); //clears up any data left from previous projects
  Serial.println("LABEL,Time,Timer,Position of Sensor,Blocks Away,Sample Number,Voltage,Distance"); //always write LABEL, so excel knows the next things will be the names of the columns (instead of Acolumn you could write Time for instance)
  Serial.println("RESETTIMER"); //resets timer to 0
}

void loop()
{
  for (int i = 1; i <= 1250; i++)
  {
   if (i <= 50) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Front Right");
    Serial.print(",");
    Serial.print(1);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Front Right ");
    double volFR = analogRead(A0); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volFR); //Print the value to the serial monitor
    Serial.print(",");
    double disFR = sensorFrontRight.getDistance();
    //Serial.print("Distance Front Right ");
    Serial.println(disFR);
   }
   if (i == 50) {
    delay(5000);
   }
    if ( i > 50 && i <= 100) {
      Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Front Right");
    Serial.print(",");
    Serial.print(2);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Front Right ");
    double volFR = analogRead(A0); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volFR); //Print the value to the serial monitor
    Serial.print(",");
    double disFR = sensorFrontRight.getDistance();
    //Serial.print("Distance Front Right ");
    Serial.println(disFR);
    }
    if (i == 100) {
      delay(5000);
    }
    if ( i > 100 && i <= 150) {
      Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Front Right");
    Serial.print(",");
    Serial.print(3);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Front Right ");
    double volFR = analogRead(A0); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volFR); //Print the value to the serial monitor
    Serial.print(",");
    double disFR = sensorFrontRight.getDistance();
    //Serial.print("Distance Front Right ");
    Serial.println(disFR);
    }
    if (i == 150) {
      delay(5000);
    }
    if ( i > 150 && i <= 200) {
      Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Front Right");
    Serial.print(",");
    Serial.print(4);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Front Right ");
    double volFR = analogRead(A0); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volFR); //Print the value to the serial monitor
    Serial.print(",");
    double disFR = sensorFrontRight.getDistance();
    //Serial.print("Distance Front Right ");
    Serial.println(disFR);
    }
    if (i==200) {
      delay(10000);
    }
    if (i > 200 && i <= 250) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Front Left");
    Serial.print(",");
    Serial.print(1);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Front Left ");
    double volFL = analogRead(A1); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volFL); //Print the value to the serial monitor
    Serial.print(",");
    double disFL = sensorFrontLeft.getDistance();
    //Serial.print("Distance Front Left ");
    Serial.println(disFL);
   }
   if (i == 250) {
    delay(5000);
   }
   if (i > 250 && i <= 300) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Front Left");
    Serial.print(",");
    Serial.print(2);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Front Left ");
    double volFL = analogRead(A1); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volFL); //Print the value to the serial monitor
    Serial.print(",");
    double disFL = sensorFrontLeft.getDistance();
    //Serial.print("Distance Front Left ");
    Serial.println(disFL);
   }
   if (i == 300) {
    delay(5000);
   }
    if ( i > 300 && i <= 350) {
      Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Front Left");
    Serial.print(",");
    Serial.print(3);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Front Left ");
    double volFL = analogRead(A1); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volFL); //Print the value to the serial monitor
    Serial.print(",");
    double disFL = sensorFrontLeft.getDistance();
    //Serial.print("Distance Front Left ");
    Serial.println(disFL);
    }
    if (i == 350) {
      delay(5000);
    }
    if ( i > 350 && i <= 400) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Front Left");
    Serial.print(",");
    Serial.print(4);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Front Left ");
    double volFL = analogRead(A1); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volFL); //Print the value to the serial monitor
    Serial.print(",");
    double disFL = sensorFrontLeft.getDistance();
    //Serial.print("Distance Front Left ");
    Serial.println(disFL);
    }
    if (i==400) {
      delay(10000);
    }
    if (i > 400 && i <= 450) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Long Right");
    Serial.print(",");
    Serial.print(1);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Long Right ");
    double volLR = analogRead(A2); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volLR); //Print the value to the serial monitor
    Serial.print(",");
    double disLR = sensorLongRight.getDistance();
    //Serial.print("Distance Long Right ");
    Serial.println(disLR);
   }
   if (i == 450) {
    delay(5000);
   }
    if (i > 450 && i <= 500) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Long Right");
    Serial.print(",");
    Serial.print(2);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Long Right ");
    double volLR = analogRead(A2); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volLR); //Print the value to the serial monitor
    Serial.print(",");
    double disLR = sensorLongRight.getDistance();
    //Serial.print("Distance Long Right ");
    Serial.println(disLR);
   }
   if (i == 500) {
    delay(5000);
  }
  if (i > 500 && i <= 550) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Long Right");
    Serial.print(",");
    Serial.print(3);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Long Right ");
    double volLR = analogRead(A2); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volLR); //Print the value to the serial monitor
    Serial.print(",");
    double disLR = sensorLongRight.getDistance();
    //Serial.print("Distance Long Right ");
    Serial.println(disLR);
   }
   if (i == 550) {
    delay(5000);
   }
   if (i > 550 && i <= 600) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Long Right");
    Serial.print(",");
    Serial.print(4);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Long Right ");
    double volLR = analogRead(A2); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volLR); //Print the value to the serial monitor
    Serial.print(",");
    double disLR = sensorLongRight.getDistance();
    //Serial.print("Distance Long Right ");
    Serial.println(disLR);
   }
   if (i == 600) {
    delay(5000);
   }
   if (i > 600 && i <= 650) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Long Right");
    Serial.print(",");
    Serial.print(5);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Long Right ");
    double volLR = analogRead(A2); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volLR); //Print the value to the serial monitor
    Serial.print(",");
    double disLR = sensorLongRight.getDistance();
    //Serial.print("Distance Long Right ");
    Serial.println(disLR);
   }
   if (i == 650) {
    delay(10000);
  }
   if (i > 650 && i <= 700) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Front Middle");
    Serial.print(",");
    Serial.print(1);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Front Middle ");
    double volFM = analogRead(A3); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volFM); //Print the value to the serial monitor
    Serial.print(",");
    double disFM = sensorFrontMiddle.getDistance();
    //Serial.print("Distance Front Middle ");
    Serial.println(disFM);
   }
   if (i == 700) {
    delay(5000);
   }
   if (i > 700 && i <= 750) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Front Middle");
    Serial.print(",");
    Serial.print(2);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Front Middle ");
    double volFM = analogRead(A3); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volFM); //Print the value to the serial monitor
    Serial.print(",");
    double disFM = sensorFrontMiddle.getDistance();
    //Serial.print("Distance Front Middle ");
    Serial.println(disFM);
   }
   if (i == 750) {
    delay(5000);
   }
   if (i > 750 && i <= 800) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Front Middle");
    Serial.print(",");
    Serial.print(3);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Front Middle ");
    double volFM = analogRead(A3); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volFM); //Print the value to the serial monitor
    Serial.print(",");
    double disFM = sensorFrontMiddle.getDistance();
    //Serial.print("Distance Front Middle ");
    Serial.println(disFM);
   }
   if (i == 800) {
    delay(5000);
   }
   if (i > 800 && i <= 850) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Front Middle");
    Serial.print(",");
    Serial.print(4);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Front Middle ");
    double volFM = analogRead(A3); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volFM); //Print the value to the serial monitor
    Serial.print(",");
    double disFM = sensorFrontMiddle.getDistance();
    //Serial.print("Distance Front Middle ");
    Serial.println(disFM);
   }
   if (i == 850) {
    delay(10000);
   }
   if (i > 850 && i <= 900) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Left Back");
    Serial.print(",");
    Serial.print(1);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Left Back ");
    double volLB = analogRead(A4); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volLB); //Print the value to the serial monitor
    Serial.print(",");
    double disLB = sensorLeftBack.getDistance();
    //Serial.print("Distance Left Back ");
    Serial.println(disLB);
   }
   if (i == 900) {
    delay(5000);
   }
   if (i > 900 && i <= 950) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Left Back");
    Serial.print(",");
    Serial.print(2);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Left Back ");
    double volLB = analogRead(A4); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volLB); //Print the value to the serial monitor
    Serial.print(",");
    double disLB = sensorLeftBack.getDistance();
    //Serial.print("Distance Left Back ");
    Serial.println(disLB);
   }
   if (i == 950) {
    delay(5000);
   }
   if (i > 950 && i <= 1000) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Left Back");
    Serial.print(",");
    Serial.print(3);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Left Back ");
    double volLB = analogRead(A4); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volLB); //Print the value to the serial monitor
    Serial.print(",");
    double disLB = sensorLeftBack.getDistance();
    //Serial.print("Distance Left Back ");
    Serial.println(disLB);
   }
   if (i == 1000) {
    delay(5000);
   }
   if (i > 1000 && i <= 1050) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Left Back");
    Serial.print(",");
    Serial.print(4);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Left Back ");
    double volLB = analogRead(A4); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volLB); //Print the value to the serial monitor
    Serial.print(",");
    double disLB = sensorLeftBack.getDistance();
    //Serial.print("Distance Left Back ");
    Serial.println(disLB);
   }
   if (i == 1050) {
    delay(10000);
   }
   if (i > 1050 && i <= 1100) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Left Front");
    Serial.print(",");
    Serial.print(1);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Left Front ");
    double volLF = analogRead(A5); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volLF); //Print the value to the serial monitor
    Serial.print(",");
    double disLF = sensorLeftFront.getDistance();
    //Serial.print("Distance Left Front ");
    Serial.println(disLF);
   }
   if (i == 1100) {
    delay(5000);
   }
   if (i > 1100 && i <= 1150) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Left Front");
    Serial.print(",");
    Serial.print(2);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Left Front ");
    double volLF = analogRead(A5); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volLF); //Print the value to the serial monitor
    Serial.print(",");
    double disLF = sensorLeftFront.getDistance();
    //Serial.print("Distance Left Front ");
    Serial.println(disLF);
   }
   if (i == 1150) {
    delay(5000);
   }
   if (i > 1150 && i <= 1200) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Left Front");
    Serial.print(",");
    Serial.print(3);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Left Front ");
    double volLF = analogRead(A5); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volLF); //Print the value to the serial monitor
    Serial.print(",");
    double disLF = sensorLeftFront.getDistance();
    //Serial.print("Distance Left Front ");
    Serial.println(disLF);
   }
   if (i == 1200) {
    delay(5000);
   }
   if (i > 1200 && i <= 1250) {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    Serial.print("Left Front");
    Serial.print(",");
    Serial.print(4);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Voltage Left Front ");
    double volLF = analogRead(A5); //Calculate the distance in centimeters and store the value in a variable
    Serial.print(volLF); //Print the value to the serial monitor
    Serial.print(",");
    double disLF = sensorLeftFront.getDistance();
    //Serial.print("Distance Left Front ");
    Serial.println(disLF);
   }
   if (i == 1250) {
    delay(10000);
   }
  }
  /*int disFL = sensorFrontLeft.getDistance(); //Calculate the distance in centimeters and store the value in a variable
  Serial.print("Distance Front Left ");
  Serial.println(disFL); //Print the value to the serial monitor
  int disSR = sensorShortRight.getDistance(); //Calculate the distance in centimeters and store the value in a variable
  Serial.print("Distance Right ");
  Serial.println(disSR); //Print the value to the serial monitor
  int disSL = sensorShortLeft.getDistance(); //Calculate the distance in centimeters and store the value in a variable
  Serial.print("Distance Left ");
  Serial.println(disSL); //Print the value to the serial monitor
  int disLoF = sensorLongFront.getDistance(); //Calculate the distance in centimeters and store the value in a variable
  Serial.print("Distance Long Front ");
  Serial.println(disLoF); //Print the value to the serial monitor
  /*int disLoL = sensorLongLeft.getDistance(); //Calculate the distance in centimeters and store the value in a variable
  Serial.print("Distance Long Left ");
  Serial.println(disLoL); //Print the value to the serial monitor*/
  delay(5000);
}
