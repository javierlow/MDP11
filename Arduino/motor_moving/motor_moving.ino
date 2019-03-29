#include "DualVNH5019MotorShield.h"
DualVNH5019MotorShield md;
void stopIfFault() {
  if (md.getM1Fault()) {
    Serial.println("M1 fault");
    while(1);
  }
  if (md.getM2Fault()) {
    Serial.println("M2 fault");
    while(1);
  }
}
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Dual VNH5019 Motor Shield");
  md.init();
}

void loop() {
  // put your main code here, to run repeatedly:
  //md.setM1Speed(400);
  //md.setM2Speed(400);
  /*delay(1000);
  md.setM1Speed(0);
  md.setM2Speed(0);
  delay(1000);*/
  /*md.setM1Speed(-400);
  md.setM2Speed(400);
  delay(1000);
  md.setM1Speed(0);
  md.setM2Speed(0);
  delay(1000);*/
  Serial.println("Forward Accelerate");
  for (int i = 0; i <= 400; i++) {
    md.setM1Speed(i);
    md.setM2Speed(i);
    stopIfFault();
    if (i%200 == 100) {
      Serial.print("M1 current: ");
      Serial.println(md.getM1CurrentMilliamps());
      Serial.print("M2 current: ");
      Serial.println(md.getM2CurrentMilliamps());
    }
    delay(2);
  }
  Serial.println("Forward Decelerate");
  for (int i = 400; i >= 0; i--) {
    md.setM1Speed(i);
    md.setM2Speed(i);
    stopIfFault();
    if (i%200 == 100) {
      Serial.print("M1 current: ");
      Serial.println(md.getM1CurrentMilliamps());
      Serial.print("M2 current: ");
      Serial.println(md.getM2CurrentMilliamps());
    }
    delay(2);
  }
  Serial.println("Backward Accelerate");
  for (int i = 0; i >= -400; i--) {
    md.setM1Speed(i);
    md.setM2Speed(i);
    stopIfFault();
    if (i%200 == -100) {
      Serial.print("M1 current: ");
      Serial.println(md.getM1CurrentMilliamps());
      Serial.print("M2 current: ");
      Serial.println(md.getM2CurrentMilliamps());
    }
    delay(2);
  }
  Serial.println("Backward Decelerate");
  for (int i = -400; i <= 0; i++) {
    md.setM1Speed(i);
    md.setM2Speed(i);
    stopIfFault();
    if (i%200 == -100) {
      Serial.print("M1 current: ");
      Serial.println(md.getM1CurrentMilliamps());
      Serial.print("M2 current: ");
      Serial.println(md.getM2CurrentMilliamps());
    }
    delay(2);
  }
}
