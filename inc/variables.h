#include <pthread.h>

#ifndef VARIABLES_H_
#define VARIABLES_H_

#define uart0_filestream;
#define internalTemp 0;
#define externalTemp 0;
#define userTemp  0;
#define valueFan  0;
#define valueResistor 0;
#define millisAux  0;
long millisCounter  = 0;
#define systemState  0;
#define funcState  0;
#define modeState  0;
#define menuChoice  0;
float ki = 0;
float kp = 0;
float kd = 0;
pthread_t ovenThread;
pthread_t reportThread;

#endif /* VARIABLES_H_ */