#include <gpio.h>
#include <softPwm.h>
#include <wiringPi.h>

#include "gpio.h"

#define RESISTOR 4
#define FAN 5

void turnOnResistor(int resistorValue) {
  pinMode(RESISTOR, OUTPUT);
  softPwmCreate(RESISTOR, 0, 100);
  softPwmWrite(RESISTOR, resistorValue);
}

void turnOffResistor() {
  if(wiringPiSetup() == -1){
	  exit(1);
  }
  pinMode(RESISTOR, OUTPUT);
  softPwmCreate(RESISTOR, 0, 100);
  softPwmWrite(RESISTOR, 0);
}

void turnOnFan(int fanValue) {
  pinMode(FAN, OUTPUT);
  softPwmCreate(FAN, 0, 100);
  softPwmWrite(FAN, fanValue);
}

void turnOffFan() {
  if(wiringPiSetup() == -1){
  	exit(1);
  }
  pinMode(FAN, OUTPUT);
  softPwmCreate(FAN, 0, 100);
  softPwmWrite(FAN, 0);
}

void pwmControl(int pwmIntensity) {
  if (pwmIntensity > 0) {
    turnOnResistor(pwmIntensity);
    turnOffFan();
  } else {
    if(pwmIntensity <= -40) {
      turnOnFan(pwmIntensity * -1);
    } else {
      turnOffFan();
    }
    turnOffResistor();
  }
}
