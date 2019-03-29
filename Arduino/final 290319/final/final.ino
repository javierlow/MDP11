#include "DualVNH5019MotorShield.h"
#include "EnableInterrupt.h"
#include "SharpIR.h"

#define M1E1Right 3
#define M2E2Left 13

DualVNH5019MotorShield md;
SharpIR sensorFrontRight( SharpIR:: GP2Y0A21YK0F, A0);
SharpIR sensorFrontLeft( SharpIR:: GP2Y0A21YK0F, A1);
SharpIR sensorLongRight( SharpIR:: GP2Y0A02YK0F, A2);
SharpIR sensorFrontMiddle( SharpIR:: GP2Y0A21YK0F, A3);
SharpIR sensorLeftBack( SharpIR:: GP2Y0A21YK0F, A4);
SharpIR sensorLeftFront( SharpIR:: GP2Y0A21YK0F, A5);

double E1ticks = 0;
double E2ticks = 0;
double M1speed = 0;
double M2speed = 0;
double invertedM1speed = 0;
double invertedM2speed = 0;
int sampletime = 20; //1000 is 1 second
int targetticks = 30;//70,83
double E1ticks_error = 0;
double E2ticks_error = 0;
double E1ticks_prev_error = 0;
double E2ticks_prev_error = 0;
double E1ticks_sum_error = 0;
double E2ticks_sum_error = 0;
double KP = 1;//0.8,0.0084460,0.0107142861,0.0091
double KD = 0.8;//0.075,0.0889,0.0113
double KI = 0.1;//0.0001,0.001
double E1ticksmoved = 0;
double E2ticksmoved = 0;
char lastRPIcommand; // to check RPI last command received so that robot will move forward accordingly
int leftcaldirection = 0; // move forward three times and backward one time

/*-----Initialize-----*/
void setup() {
  pinMode(M1E1Right, INPUT);
  digitalWrite(M1E1Right, HIGH);       // turn on pull-up resistor
  pinMode(M2E2Left, INPUT);
  digitalWrite(M2E2Left, HIGH);       // turn on pull-up resistor
  //delay(5000);
  enableInterrupt(M1E1Right, E1Increment, RISING);
  enableInterrupt(M2E2Left, E2Increment, RISING);
  Serial.begin(115200);
  //Serial.println("Dual VNH5019 Motor Shield");
  md.init();
  //Serial.println("start");                // a personal quirk
}

/*-----Main-----*/
void loop() {
  //forward(1);
  //done();
  char RPIcommand;
  while (Serial.available()) {
    RPIcommand = Serial.read();
    if (RPIcommand == 'a') {
      left(90);
      lastRPIcommand = 'a';
      done();
    }
    else if (RPIcommand == 'b') {
      forward(2);
      lastRPIcommand = 'b';
      done();
    }
    else if (RPIcommand == 'c') {
      forward(3);
      lastRPIcommand = 'c';
      done();
    }
    else if (RPIcommand == 'd') {
      right(90);
      lastRPIcommand = 'd';
      done();
    }
    else if (RPIcommand == 'e') {
      forward(4);
      lastRPIcommand = 'e';
      done();
    }
    else if (RPIcommand == 'f') {
      forward(5);
      lastRPIcommand = 'f';
      done();
    }
    else if (RPIcommand == 'g') {
      forward(6);
      lastRPIcommand = 'g';
      done();
    }
    else if (RPIcommand == 'h') {
      forward(7);
      lastRPIcommand = 'h';
      done();
    }
    else if (RPIcommand == 'i') {
      forward(8);
      lastRPIcommand = 'i';
      done();
    }
    else if (RPIcommand == 'j') {
      forward(9);
      lastRPIcommand = 'j';
      done();
    }
    else if (RPIcommand == 'k') {
      forward(10);
      lastRPIcommand = 'k';
      done();
    }
    else if (RPIcommand == 'l') {
      forward(11);
      lastRPIcommand = 'l';
      done();
    }
    else if (RPIcommand == 'm') {
      forward(12);
      lastRPIcommand = 'm';
      done();
    }
    else if (RPIcommand == 'n') {
      forward(13);
      lastRPIcommand = 'n';
      done();
    }
    else if (RPIcommand == 'o') {
      forward(14);
      lastRPIcommand = 'o';
      done();
    }
    else if (RPIcommand == 'p') {
      forward(15);
      lastRPIcommand = 'p';
      done();
    }
    else if (RPIcommand == 'q') {
      initialCalibrate();
      lastRPIcommand = 'q';
      done();
    }
    else if (RPIcommand == 'r') {
      frontCalibrate();
      lastRPIcommand = 'r';
      done();
    }
    else if (RPIcommand == 's') {
      backward(1);
      lastRPIcommand = 's';
      done();
    }
    else if (RPIcommand == 't') {
      leftCalibrate();
      lastRPIcommand = 't';
      done();
    }
    else if (RPIcommand == 'u') {
      sensorReading();
      lastRPIcommand = 'u';
    }
    else if (RPIcommand == 'v') {
      left(180);
      lastRPIcommand = 'v';
      done();
    }
    else if (RPIcommand == 'w') {
      forward(1);
      lastRPIcommand = 'w';
      done();
    }
    else if (RPIcommand == 'x') {
      right(180);
      lastRPIcommand = 'x';
      done();
    }
    else if (RPIcommand == 'y') {
      left(45);
      lastRPIcommand = 'y';
      done();
    }
    else if (RPIcommand == 'z') {
      right(45);
      lastRPIcommand = 'z';
      done();
    }
  }
}

/*-----Motor-----*/
void forward(int blockstomove) {
  E1ticks = 0;
  E2ticks = 0;
  E1ticksmoved = 0;
  E2ticksmoved = 0;
  int tickstomove;
  switch (blockstomove) {
    case 1:
      {
        if (lastRPIcommand == 'a' || lastRPIcommand == 'd') {
          tickstomove = 230;
        }
        else {
          tickstomove = 238;
        }
        break;
      }
    case 2:
      {
        tickstomove = 560;
        break;
      }
    case 3:
      {
        tickstomove = 850;
        break;
      }
    case 4:
      {
        tickstomove = 1150;
        break;
      }
    case 5:
      {
        tickstomove = 1430;
        break;
      }
    case 6:
      {
        tickstomove = 1740;
        break;
      }
    case 7:
      {
        tickstomove = 2050;
        break;
      }
    case 8:
      {
        tickstomove = 2330;
        break;
      }
    case 9:
      {
        tickstomove = 2620;
        break;
      }
    case 10:
      {
        tickstomove = 2950;
        break;
      }
    case 11:
      {
        tickstomove = 3250;
        break;
      }
    case 12:
      {
        tickstomove = 3520;
        break;
      }
    case 13:
      {
        tickstomove = 3820;
        break;
      }
    case 14:
      {
        tickstomove = 4140;
        break;
      }
    case 15:
      {
        tickstomove = 4370;
        break;
      }
  }

  while (1) {
    if (E1ticksmoved > tickstomove || E2ticksmoved > tickstomove) {
      /*Serial.print("E1 ticks moved: ");
        Serial.println(E1ticksmoved);
        Serial.print("E2 ticks moved: ");
        Serial.println(E2ticksmoved);*/
      md.setBrakes(M1speed, M2speed);
      delay(100);
      md.setBrakes(400, 400);
      delay(100);
      md.setBrakes(0, 0);
      /*if (E1ticksmoved > E2ticksmoved) {
        int correction = E1ticksmoved - E2ticksmoved;
        ticksE2Corrector(correction);
        }
        else if (E2ticksmoved > E1ticksmoved) {
        int correction = E2ticksmoved - E1ticksmoved;
        ticksE1Corrector(correction);
        }*/
      break;
    }
    PIDController(1);
  }
}

void backward(int blockstomove) {
  E1ticks = 0;
  E2ticks = 0;
  E1ticksmoved = 0;
  E2ticksmoved = 0;
  int tickstomove =  210 * blockstomove;
  while (1) {
    if (E1ticksmoved > tickstomove || E2ticksmoved > tickstomove) {
      /*Serial.print("E1 ticks moved: ");
        Serial.println(E1ticksmoved);
        Serial.print("E2 ticks moved: ");
        Serial.println(E2ticksmoved);*/
      md.setBrakes(M1speed, M2speed);
      delay(100);
      md.setBrakes(400, 400);
      delay(100);
      md.setBrakes(0, 0);
      break;
    }
    PIDController(2);
  }
}
void left(int degreetomove) {
  E1ticks = 0;
  E2ticks = 0;
  E1ticksmoved = 0;
  E2ticksmoved = 0;
  int tickstomove = 0;
  if (degreetomove == 45) {
    tickstomove = 105; //ticks 30
  }
  else if (degreetomove == 90) {
    tickstomove = 327; //320(lounge)ticks 30 done
  }
  else if (degreetomove == 180) {
    tickstomove = 720; //ticks 30 done
  }
  while (1) {
    if (E1ticksmoved > tickstomove || E2ticksmoved > tickstomove) {
      /*Serial.print("E1 ticks moved: ");
        Serial.println(E1ticksmoved);
        Serial.print("E2 ticks moved: ");
        Serial.println(E2ticksmoved);*/
      md.setBrakes(M1speed, invertedM2speed);
      delay(100);
      md.setBrakes(400, -400);
      delay(100);
      md.setBrakes(0, 0);
      int correction1 = E1ticksmoved - tickstomove;
      int correction2 = E2ticksmoved - tickstomove;
      /*if (correction1 < 0 || correction1 > 0) {
        ticksE1Corrector(correction1);
        }
        if (correction2 < 0 || correction2 > 0) {
        ticksE2Corrector(correction2);
        }*/
      /*if (E1ticksmoved > E2ticksmoved) {
        int correction = E1ticksmoved - E2ticksmoved;
        ticksE2Corrector(correction);
        }
        else if (E2ticksmoved > E1ticksmoved) {
        int correction = E2ticksmoved - E1ticksmoved;
        ticksE1Corrector(correction);
        }*/
      break;
    }
    PIDController(3);
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
    tickstomove = 330; //ticks 30 done
  }
  else if (degreetomove == 180) {
    tickstomove = 720; //ticks 30 done
  }
  while (1) {
    if (E1ticksmoved > tickstomove || E2ticksmoved > tickstomove) {
      /*Serial.print("E1 ticks moved: ");
        Serial.println(E1ticksmoved);
        Serial.print("E2 ticks moved: ");
        Serial.println(E2ticksmoved);*/
      md.setBrakes(invertedM1speed, M2speed);
      delay(100);
      md.setBrakes(-400, 400);
      delay(100);
      md.setBrakes(0, 0);
      int correction1 = E1ticksmoved - tickstomove;
      int correction2 = E2ticksmoved - tickstomove;
      /*if (correction1 < 0 || correction1 > 0) {
        ticksE1Corrector(correction1);
        }
        if (correction2 < 0 || correction2 > 0) {
        ticksE2Corrector(correction2);
        }*/
      /*if (E1ticksmoved > E2ticksmoved) {
        int correction = E1ticksmoved - E2ticksmoved;
        ticksE2Corrector(correction);
        }
        else if (E2ticksmoved > E1ticksmoved) {
        int correction = E2ticksmoved - E1ticksmoved;
        ticksE1Corrector(correction);
        }*/
      break;
    }
    PIDController(4);
  }
}

/*-----Sensor-----*/
void sensorReading() {
  int marginerror = 4;
  //int blkFR = (sensorFrontRight.getDistance() + marginerror) / 10;
  //int blkFL = (sensorFrontLeft.getDistance() + marginerror) / 10;
  //int blkFM = (sensorFrontMiddle.getDistance() + marginerror) / 10;
  //int blkLB = (sensorLeftBack.getDistance() + marginerror) / 10;
  //int blkLF = (sensorLeftFront.getDistance() + marginerror) / 10;

  int disFR = sensorFrontRight.getDistance();
  int blkFR = 0;
  if (disFR >= 9 && disFR <= 13) {
    blkFR = 1;
  }
  else if (disFR >= 17 && disFR <= 22) {
    blkFR = 2;
  }
  else if (disFR >= 26 && disFR <= 32) {
    blkFR = 3;
  }
  else if (disFR >= 35 && disFR <= 44) {
    blkFR = 4;
  }

  int disFL = sensorFrontLeft.getDistance();
  int blkFL = 0;
  if (disFL >= 9 && disFL <= 13) {
    blkFL = 1;
  }
  else if (disFL >= 18 && disFL <= 22) {
    blkFL = 2;
  }
  else if (disFL >= 28 && disFL <= 33) {
    blkFL = 3;
  }
  else if (disFL >= 38 && disFL <= 45) {
    blkFL = 4;
  }

  int disLR = sensorLongRight.getDistance();
  int blkLR = 0;
  if (disLR <= 19) {
    blkLR = 2;
  }
  else if (disLR >= 21 && disLR <= 24) {
    blkLR = 3;
  }
  else if (disLR >= 26 && disLR <= 31) {
    blkLR = 4;
  }
  else if (disLR >= 33 && disLR <= 40) {
    blkLR = 5;
  }
  else if (disLR >= 41 && disLR <= 50) {
    blkLR = 6;
  }

  int disFM = sensorFrontMiddle.getDistance();
  int blkFM = 0;
  if (disFM >= 9 && disFM <= 13) {
    blkFM = 1;
  }
  else if (disFM >= 19 && disFM <= 24) {
    blkFM = 2;
  }
  else if (disFM >= 30 && disFM <= 35) {
    blkFM = 3;
  }
  else if (disFM >= 39 && disFM <= 48) {
    blkFM = 4;
  }

  int disLB = sensorLeftBack.getDistance();
  int blkLB = 0;
  if (disLB >= 9 && disLB <= 13) {
    blkLB = 1;
  }
  else if (disLB >= 17 && disLB <= 21) {
    blkLB = 2;
  }
  else if (disLB >= 26 && disLB <= 31) {
    blkLB = 3;
  }
  else if (disLB >= 34 && disLB <= 42) {
    blkLB = 4;
  }

  int disLF = sensorLeftFront.getDistance();
  int blkLF = 0;
  if (disLF >= 9 && disLF <= 13) {
    blkLF = 1;
  }
  else if (disLF >= 18 && disLF <= 21) {
    blkLF = 2;
  }
  else if (disLF >= 25 && disLF <= 29) {
    blkLF = 3;
  }
  else if (disLF >= 32 && disLF <= 36) {
    blkLF = 4;
  }
  int totalblockcal[] = {blkLB, blkLF, blkFL, blkFM, blkFR, blkLR,
                         blkLB, blkLF, blkFL, blkFM, blkFR, blkLR,
                         blkLB, blkLF, blkFL, blkFM, blkFR, blkLR,
                         blkLB, blkLF, blkFL, blkFM, blkFR, blkLR,
                         blkLB, blkLF, blkFL, blkFM, blkFR, blkLR,
                         blkLB, blkLF, blkFL, blkFM, blkFR, blkLR,
                         blkLB, blkLF, blkFL, blkFM, blkFR, blkLR,
                         blkLB, blkLF, blkFL, blkFM, blkFR, blkLR,
                         blkLB, blkLF, blkFL, blkFM, blkFR, blkLR,
                         blkLB, blkLF, blkFL, blkFM, blkFR, blkLR,
                         blkLB, blkLF, blkFL, blkFM, blkFR, blkLR
                        };

  String convertedtotalblockcal = "P";

  for (int i = 0; i < 66; i++) {
    convertedtotalblockcal += totalblockcal[i];
    if (i < 65) {
      convertedtotalblockcal += ",";
    }
  }
  Serial.println(convertedtotalblockcal);
}

/*-----Calibrate-----*/
void frontCalibrate() {
  while (sensorFrontLeft.getDistance() != 10 || sensorFrontRight.getDistance() != 10)
  {
    if (sensorFrontLeft.getDistance() < 10 && sensorFrontRight.getDistance() < 10) {
      md.setSpeeds(-100, -100);
    }
    else if (sensorFrontLeft.getDistance() > 10 && sensorFrontRight.getDistance() > 10) {
      md.setSpeeds(100, 100);
    }
    else if (sensorFrontLeft.getDistance() < 10 && sensorFrontRight.getDistance() > 10) {
      md.setM2Speed(-100);
      if (sensorFrontLeft.getDistance() == 10) {
        md.setBrakes(0, 100);
        md.setM1Speed(100);
      }
    }
    else if (sensorFrontLeft.getDistance() > 10 && sensorFrontRight.getDistance() < 10) {
      md.setM1Speed(-100);
      if (sensorFrontLeft.getDistance() == 10) {
        md.setBrakes(100, 0);
        md.setM2Speed(100);
      }
    }
  }
  md.setBrakes(400, 400);
  md.setBrakes(0, 0);
  delay(100);
}

void leftCalibrate() {
  int difference = 0;
  while (1) {
    /*if (sensorLeftFront.getDistance() <= 10 || sensorLeftBack.getDistance() <= 10 || sensorLeftFront.getDistance() >= 12 || sensorLeftBack.getDistance() >= 12) {
      left(90);
      frontCalibrate();
      right(90);
      }*/
    difference = (sensorLeftFront.getDistance() - 1) - sensorLeftBack.getDistance();
    if (leftcaldirection == 4) {
      if (difference >= 1) {
        md.setBrakes(0, 0);
        md.setM2Speed(-100);
        delay(100);
      }
      else if (difference <= -1) {
        md.setBrakes(0, 0);
        md.setM1Speed(-100);
        delay(100);
      }
      else {
        md.setBrakes(0, 0);
        break;
      }
      leftcaldirection = 0;
    }
    else {
      if (difference >= 1) {
        md.setBrakes(0, 0);
        md.setM1Speed(100);
        delay(100);
      }
      else if (difference <= -1) {
        md.setBrakes(0, 0);
        md.setM2Speed(100);
        delay(100);
      }
      else {
        md.setBrakes(0, 0);
        break;
      }
      leftcaldirection++;
    }
  }
}

void initialCalibrate() {
  /*left(90);
    delay(200);
    left(180);
    delay(200);
    left(180);
    delay(200);
    right(180);
    delay(200);
    right(180);
    delay(200);*/
  left(180);
  delay(200);
  frontCalibrate();
  delay(200);
  right(90);
  delay(200);
  frontCalibrate();
  delay(200);
  right(90);
  delay(200);
  leftCalibrate();
  delay(200);
  leftCalibrate();
}

void ticksE1Corrector(int correctionticks) {
  int temp = E1ticks;
  E1ticks = 0;
  md.setM1Speed(100);
  /*if (correctionticks < 0) {
    md.setM1Speed(100);
    }
    else if (correctionticks > 0) {
    md.setM1Speed(-100);
    }
    while (correctionticks > E1ticks) {
    Serial.print("M1 Moved for Correction: ");
    Serial.println(E1ticks);
    }*/
  md.setM1Brake(100);
  E1ticks = temp;
}

void ticksE2Corrector(int correctionticks) {
  int temp = E2ticks;
  E2ticks = 0;
  md.setM2Speed(100);
  /*if (correctionticks < 0) {
    md.setM2Speed(100);
    }
    else if (correctionticks > 0) {
    md.setM2Speed(-100);
    }
    while (correctionticks > E2ticks) {
    Serial.print("M2 Moved for Correction: ");
    Serial.println(E2ticks);
    }*/
  md.setM2Brake(100);
  E2ticks = temp;
}

/*-----PID-----*/
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
    md.setSpeeds(invertedM1speed, invertedM2speed);
  }
  else if (directionflag == 3) {
    md.setSpeeds(M1speed, invertedM2speed);
  }
  else if (directionflag == 4) {
    md.setSpeeds(invertedM1speed, M2speed);
  }
  /*Serial.print("E1 Ticks: ");
    Serial.print(E1ticks);
    Serial.print(" M1 Speed: ");
    Serial.println(M1speed);
    Serial.print("E2 Ticks: ");
    Serial.print(E2ticks);
    Serial.print(" M2 Speed: ");
    Serial.println(M2speed);*/
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

/*-----ISR-----*/
void E1Increment() {
  E1ticks++;
}

void E2Increment() {
  E2ticks++;
}

/*-----Verification after action-----*/
void done() {
  Serial.println("PD");
}
