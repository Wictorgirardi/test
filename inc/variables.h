#include <pthread.h>

#ifndef VARIABLES_H_
#define VARIABLES_H_


int uart0_filestream;
float internalTemp = 0;
float externalTemp = 0;
float userTemp = 0;
int valueFan = 0;
int valueResistor = 0;
long millisAux = 0;
long millisCounter = 0;
int systemState = 0;
int funcState = 0;
int modeState = 0;
int menuChoice = 0;
float ki = 0;
float kp = 0;
float kd = 0;
pthread_t ovenThread;
pthread_t reportThread;
struct bme280_dev bme;

#endif /* VARIABLES_H_ */