#include "DualVNH5019MotorShield.h"
#include "EnableInterrupt.h"

#define M1E1Right 3
#define M2E2Left 13

DualVNH5019MotorShield md;

double E1ticks = 0;
double E2ticks = 0;
double M1speed = 0;
double M2speed = 0;
double invertedM1speed = 0;
double invertedM2speed = 0;
int sampletime = 50; //1000 is 1 second
double targetticks = 29;//30(left for 45 degree) 29(left for 90 degree),70,83
double E1ticks_error = 0;
double E2ticks_error = 0;
double E1ticks_prev_error = 0;
double E2ticks_prev_error = 0;
double E1ticks_sum_error = 0;
double E2ticks_sum_error = 0;
double KP = 1;//0.8,0.0084460,0.0107142861,0.0091
double KD = 0.1;//0.075,0.0889,0.0113
double KI = 0;//0.0001,0.001
double E1ticksmoved = 0;
double E2ticksmoved = 0;

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
  /*left(360);
  left(360);
  left(360);
  left(360);
  left(360);
  left(360);
  left(360);
  left(360);
  left(360);
  left(360);
  delay(5000);*/
}

void loop() {
  right(90);
  delay(1000);
  /*while (Serial.available()) {
    if (Serial.read() == 'W') {
      forward(1);
    }
    }
    while(1) {
    forward(1);
    delay(3000);
    }*/
}

void left(int degreetomove) {
  E1ticks = 0;
  E2ticks = 0;
  E1ticksmoved = 0;
  E2ticksmoved = 0;
  int tickstomove = 0;
  if (degreetomove == 45) {
    tickstomove = 105;
  }
  else if (degreetomove == 90) {
    tickstomove = 290;
  }
  else if (degreetomove == 180) {
    tickstomove = 716;
  }
  else if (degreetomove == 360) {
    tickstomove = 1512;
  }
  int correction = 0;
  while (1) {
    if (E1ticksmoved > tickstomove || E2ticksmoved > tickstomove) {
      Serial.print("E1 ticks moved: ");
      Serial.println(E1ticksmoved);
      Serial.print("E2 ticks moved: ");
      Serial.println(E2ticksmoved);
      md.setBrakes(M1speed, invertedM2speed);
      delay(100);
      md.setBrakes(400, -400);
      delay(100);
      md.setBrakes(0, 0);
      /*if (E1ticksmoved > E2ticksmoved) {
        correction = E1ticksmoved - E2ticksmoved;
        Serial.print("M2 Correction: ");
        Serial.println(correction);
        ticksE2Corrector(correction);
      }
      else if (E1ticksmoved < E2ticksmoved ) {
        correction = E2ticksmoved - E1ticksmoved;
        Serial.print("M1 Correction: ");
        Serial.println(correction);
        ticksE1Corrector(correction);
      }*/
      break;
    }
    PIDController(2);
  }
}

void right(int degreetomove) {
  E1ticks = 0;
  E2ticks = 0;
  E1ticksmoved = 0;
  E2ticksmoved = 0;
  int tickstomove = 0;
  if (degreetomove == 45) {
    tickstomove = 105;
  }
  else if (degreetomove == 90) {
    tickstomove = 291; //
  }
  else if (degreetomove == 180) {
    tickstomove = 716;
  }
  /*else if (degreetomove == 360) {
    tickstomove = 1512;
    }
    int correction = 0;*/
  while (1) {
    if (E1ticksmoved > tickstomove || E2ticksmoved > tickstomove) {
      Serial.print("E1 ticks moved: ");
      Serial.println(E1ticksmoved);
      Serial.print("E2 ticks moved: ");
      Serial.println(E2ticksmoved);
      md.setBrakes(invertedM1speed, M2speed);
      delay(100);
      md.setBrakes(-400, 400);
      delay(100);
      md.setBrakes(0, 0);
      /*if (E1ticksmoved > E2ticksmoved) {
        correction = E1ticksmoved - E2ticksmoved;
        Serial.print("M2 Correction: ");
        Serial.println(correction);
        ticksE2Corrector(correction);
        }
        else if (E1ticksmoved < E2ticksmoved ) {
        correction = E2ticksmoved - E1ticksmoved;
        Serial.print("M1 Correction: ");
        Serial.println(correction);
        ticksE1Corrector(correction);
        }*/
      break;
    }
    PIDController(3);
  }
}

void PIDController(int directionflag) {
  E1ticks_error = targetticks - E1ticks;
  E2ticks_error = targetticks - E2ticks;
  M1speed += (E1ticks_error * KP) + (E1ticks_prev_error * KD) + (E1ticks_sum_error * KI);
  M2speed += (E2ticks_error * KP) + (E2ticks_prev_error * KD) + (E2ticks_sum_error * KI);
  M1speed = max(min(400, M1speed), 0);
  M2speed = max(min(400, M2speed), 0);
  invertedM1speed = -M1speed;
  invertedM2speed = -M2speed;
  if (directionflag == 1) {
    md.setSpeeds(M1speed, M2speed);
  }
  else if (directionflag == 2) {
    md.setSpeeds(M1speed, invertedM2speed);
  }
  else if (directionflag == 3) {
    md.setSpeeds(invertedM1speed, M2speed);
  }
  Serial.print("E1 Ticks: ");
  Serial.print(E1ticks);
  Serial.print(" M1 Speed: ");
  Serial.println(M1speed);
  Serial.print("E2 Ticks: ");
  Serial.print(E2ticks);
  Serial.print(" M2 Speed: ");
  Serial.println(M2speed);
  E1ticksmoved += E1ticks;
  E2ticksmoved += E2ticks;
  E1ticks = 0;
  E2ticks = 0;
  delay(sampletime);
  E1ticks_prev_error = E1ticks_error;
  E2ticks_prev_error = E2ticks_error;
  E1ticks_sum_error += E1ticks_error;
  E2ticks_sum_error += E2ticks_error;
}

void ticksE1Corrector(int correctionticks) {
  int temp = E1ticks;
  E1ticks = 0;
  md.setM1Speed(100);
  while (correctionticks > E1ticks) {
    Serial.print("M1 Moved for Correction: ");
    Serial.println(E1ticks);
  }
  md.setM1Brake(100);
  E1ticks = temp;
}

void ticksE2Corrector(int correctionticks) {
  int temp = E2ticks;
  E2ticks = 0;
  md.setM2Speed(-100);
  while (correctionticks > E2ticks) {
    Serial.print("M2 Moved for Correction: ");
    Serial.println(E2ticks);
  }
  md.setM2Brake(-100);
  E2ticks = temp;
}

void E1Increment() {
  E1ticks++;
}

void E2Increment() {
  E2ticks++;
}
