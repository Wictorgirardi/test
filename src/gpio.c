#include <gpio.h>
#include <softPwm.h>
#include <wiringPi.h>

#include "gpio.h"

void turnOnResistor(int resistorValue) {
  pinMode(4, OUTPUT);
  softPwmCreate(4, 0, 100);
  softPwmWrite(4, resistorValue);
}

void turnOffResistor() {
  if(wiringPiSetup() == -1){
	  exit(1);
  }
  pinMode(4, OUTPUT);
  softPwmCreate(4, 0, 100);
  softPwmWrite(4, 0);
}

void turnOnFan(int fanValue) {
  pinMode(5, OUTPUT);
  softPwmCreate(5, 0, 100);
  softPwmWrite(5, fanValue);
}

void turnOffFan() {
  if(wiringPiSetup() == -1){
  	exit(1);
  }
  pinMode(5, OUTPUT);
  softPwmCreate(5, 0, 100);
  softPwmWrite(5, 0);
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
