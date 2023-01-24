#include <pthread.h>

#ifndef VARIABLES_H_
#define VARIABLES_H_

#define int uart0_filestream;
#define float internalTemp = 0;
#define float externalTemp = 0;
#define float userTemp = 0;
#define int valueFan = 0;
#define int valueResistor = 0;
#define long millisAux = 0;
#define long millisCounter = 0;
#define int systemState = 0;
#define int funcState = 0;
#define int modeState = 0;
#define int menuChoice = 0;
#define float ki = 0;
#define float kp = 0;
#define float kd = 0;
#define pthread_t ovenThread;
#define pthread_t reportThread;

#endif /* VARIABLES_H_ */