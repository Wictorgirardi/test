#include "pid.h"
#include <stdio.h>

double outMeasurement, controlSignal;
double reference = 0.0;
double Kp = 0.0;  // Ganho Proporcional
double Ki = 0.0;  // Ganho Integral
double Kd = 0.0;  // Ganho Derivativo
int T = 1.0;      // Período de Amostragem (ms)
unsigned long lastTime;
double totalError, previousError = 0.0;
int controlSignalMAX = 100.0;
int controlSignalMIN = -100.0;

void pidSetupConstants(double Kp_, double Ki_, double Kd_){
    Kp = Kp_;
    Ki = Ki_;
    Kd = Kd_;
}

void pidUpdateReferences(float reference_){
    reference = (double) reference_;
}

double pidControl(double outMeasurement){
  
    double error = reference - outMeasurement;
    totalError += error; // Acumula o error (Termo Integral)

    if (totalError >= controlSignalMAX){
        totalError = controlSignalMAX;
    } else if (totalError <= controlSignalMIN){
        totalError = controlSignalMIN;
    }

    double deltaError = error - previousError; // Diferença entre os erros (Termo Derivativo)
    controlSignal = Kp*error + (Ki*T)*totalError + (Kd/T)*deltaError; // PID calcula sinal de controle

    if (controlSignal >= controlSignalMAX){
        controlSignal = controlSignalMAX;
    } else if (controlSignal <= controlSignalMIN) {
        controlSignal = controlSignalMIN;
    }

    previousError = error;

    return controlSignal;
}
