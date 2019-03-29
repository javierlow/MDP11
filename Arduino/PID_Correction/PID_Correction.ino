#include "DualVNH5019MotorShield.h"
#include "EnableInterrupt.h"

#define M1E1Right 3
#define M2E2Left 13

DualVNH5019MotorShield md;

double E1ticks = 0;
double E2ticks = 0;
double M1speed = 0;
double M2speed = 0;
int sampletime = 25; //1000 is 1 second
double targetticks = 30; //74,70,83
double E1ticks_error = 0;
double E2ticks_error = 0;
double E1ticks_prev_error = 0;
double E2ticks_prev_error = 0;
double E1ticks_sum_error = 0;
double E2ticks_sum_error = 0;
double KP = 1;//0.0089285714,0.0107142861,0.0091
double KD = 0.7;
double KI = 0;

void setup() {
  pinMode(M1E1Right, INPUT);
  digitalWrite(M1E1Right, HIGH);       // turn on pull-up resistor
  pinMode(M2E2Left, INPUT);
  digitalWrite(M2E2Left, HIGH);       // turn on pull-up resistor
  delay(5000);
  enableInterrupt(M1E1Right, E1Increment, RISING);
  enableInterrupt(M2E2Left, E2Increment, RISING);
  Serial.begin(9600);
  Serial.println("Dual VNH5019 Motor Shield");
  md.init();
  Serial.println("start");                // a personal quirk
  md.setM1Speed(M1speed);
  md.setM2Speed(M2speed);
}
void loop() {
  // do some stuff here - the joy of interrupts is that they take care of themselves
  int counter = 1;
  while(1){
    E1ticks_error = targetticks - E1ticks;
    E2ticks_error = targetticks - E2ticks;
    
    //M1speed += E1ticks_error * KP;
    //M2speed += E2ticks_error * KP;
    //M1speed += (E1ticks_error * KP) + (E1ticks_prev_error * KD);
    //M2speed += (E2ticks_error * KP) + (E2ticks_prev_error * KD);

    M1speed += (E1ticks_error * KP) + (E1ticks_prev_error * KD) + (E1ticks_sum_error * KI);
    M2speed += (E2ticks_error * KP) + (E2ticks_prev_error * KD) + (E2ticks_sum_error * KI);
    
    M1speed = max(min(400, M1speed), 0);
    M2speed = max(min(400, M2speed), 0);

    md.setM1Speed(M1speed);
    md.setM2Speed(M2speed);

    Serial.print("E1 Ticks: ");
    Serial.print(E1ticks);
    Serial.print(" M1 Speed: ");
    Serial.println(M1speed);
    Serial.print("E2 Ticks: ");
    Serial.print(E2ticks);
    Serial.print(" M2 Speed: ");
    Serial.println(M2speed);
    /*Serial.print("Reading value: ");
    Serial.println(counter);
    counter++;
    Serial.print("M1 Ticks: ");
    Serial.print(E1Pos);
    Serial.print(" M1E1Right RPM = ");
    Serial.println(E1Pos/562.25 * sampletime);
    Serial.print("M2 Ticks: ");
    Serial.print(E2Pos);
    Serial.print(" M2E2Left RPM = ");
    Serial.println(E2Pos/562.25 * sampletime);*/
    E1ticks = 0;
    E2ticks = 0;

    delay(sampletime);
    E1ticks_prev_error = E1ticks_error;
    E2ticks_prev_error = E2ticks_error;
    E1ticks_sum_error += E1ticks_error;
    E2ticks_sum_error += E2ticks_error;
  }
}

void E1Increment() {
  /* If pinA and pinB are both high or both low, it is spinning
     forward. If they're different, it's going backward.

     For more information on speeding up this process, see
     [Reference/PortManipulation], specifically the PIND register.
  */
  E1ticks++;
}

void E2Increment() {
  /* If pinA and pinB are both high or both low, it is spinning
     forward. If they're different, it's going backward.

     For more information on speeding up this process, see
     [Reference/PortManipulation], specifically the PIND register.
  */
  E2ticks++;
}
