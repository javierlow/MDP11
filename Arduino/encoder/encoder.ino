#include "DualVNH5019MotorShield.h"
#include "EnableInterrupt.h"

#define M1E1Right 3
#define M2E2Left 13

DualVNH5019MotorShield md;

volatile unsigned int E1Pos = 0;
volatile unsigned int E2Pos = 0;

void setup() {
  pinMode(M1E1Right, INPUT);
  digitalWrite(M1E1Right, HIGH);       // turn on pull-up resistor
  pinMode(M2E2Left, INPUT);
  digitalWrite(M2E2Left, HIGH);       // turn on pull-up resistor
  delay(5000);
  enableInterrupt(M1E1Right, E1, RISING);
  enableInterrupt(M2E2Left, E2, RISING);
  Serial.begin(9600);
  Serial.println("Dual VNH5019 Motor Shield");
  md.init();
  Serial.println("start");                // a personal quirk
}
void loop() {
  // do some stuff here - the joy of interrupts is that they take care of themselves
  int counter = 1;
  while(1){
    //md.setSpeeds(400,400);
    //delay(3000);
    //md.setBrakes(400,400);
    //delay(100);
    //md.setBrakes(0,0);
    //delay(100);
    delay(5000);
    Serial.print("Reading value: ");
    Serial.println(counter);
    counter++;
    Serial.print(E1Pos);
    //Serial.print(" M1E1Right RPM = ");
    //Serial.println(E1Pos/562.25 * 60);
    Serial.print(E2Pos);
    //Serial.print(" M2E2Left RPM = ");
    //Serial.println(E2Pos/562.25 * 60);
    E1Pos = 0;
    E2Pos = 0;
    
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
