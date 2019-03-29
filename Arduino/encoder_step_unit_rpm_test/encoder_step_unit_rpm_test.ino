#include "DualVNH5019MotorShield.h"
#include "EnableInterrupt.h"

#define M1E1Right 3
#define M2E2Left 11

DualVNH5019MotorShield md;

volatile unsigned int E1Pos = 0;
volatile unsigned int E2Pos = 0;

//always starts in line 0 and writes the thing written next to LABEL

void setup() {

pinMode(M1E1Right, INPUT);
digitalWrite(M1E1Right, HIGH);       // turn on pull-up resistor
pinMode(M2E2Left, INPUT);
digitalWrite(M2E2Left, HIGH);       // turn on pull-up resistor
delay(5000);
enableInterrupt(M1E1Right, E1, RISING);
enableInterrupt(M2E2Left, E2, RISING);
Serial.begin(9600); // the bigger number the better
md.init();
Serial.println("CLEARDATA"); //clears up any data left from previous projects
Serial.println("LABEL,Time,Timer,Sample Number,Step Unit,M1E1 Right RPM,M2E2 Left RPM,E1 Ticks, E2 Ticks"); //always write LABEL, so excel knows the next things will be the names of the columns (instead of Acolumn you could write Time for instance)
Serial.println("RESETTIMER"); //resets timer to 0
}

void loop() {
int unit = 300;
  while (unit > 0)
  {
    unit = unit - 50;
    md.setM1Speed(0);
    md.setM2Speed(0);
    delay(5000);
    E1Pos = 0;
    E2Pos = 0;
    
    for (int i = 1; i <= 7; i++)
   {
    Serial.print("DATA,TIME,TIMER,"); //writes the time in the first column A and the time since the measurements started in column B
    md.setM1Speed(unit);
    md.setM2Speed(unit);
    delay(1000);
    Serial.print(i);
    Serial.print(",");
    //Serial.print("Reading value for unit speed ");
    Serial.print(unit);
    Serial.print(",");
    //Serial.print("M1E1Right RPM = ");
    Serial.print(E1Pos/562.25 * 60);
    Serial.print(",");
    //Serial.print("M2E2Left RPM = ");
    Serial.print(E2Pos/562.25 * 60);
    Serial.print(E1Pos);
    Serial.println(E2Pos);
    delay(100); //add a delay
    E1Pos = 0;
    E2Pos = 0;
   }
  }
}
void E1() {
  /* If pinA and pinB are both high or both low, it is spinning
     forward. If they're different, it's going backward.

     For more information on speeding up this process, see
     [Reference/PortManipulation], specifically the PIND register.
  */
  E1Pos++;
}

void E2() {
  /* If pinA and pinB are both high or both low, it is spinning
     forward. If they're different, it's going backward.

     For more information on speeding up this process, see
     [Reference/PortManipulation], specifically the PIND register.
  */
  E2Pos++;
}
