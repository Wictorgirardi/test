#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wiringPi.h>
#include <softPwm.h>
#include <time.h>
#include <pthread.h>
#include <signal.h>
#include <unistd.h>
#include <termios.h>
#include <fcntl.h>
#include <unistd.h>
#include "pid.h"
#include "bme280.h"
#include "gpio.h"
#include "uart.h"
#include "i2c.h"
#include "uart_defs.h"

int uart0_filestream;
float internalTemp = 0;
float externalTemp = 0;
float userTemp = 0;
int valueFan = 0;
int valueResistor = 0;
long millisAux = 0;
long millisCounter = 0;
// 1 ligado 0 desligado
int systemState = 0;
// 1 funcionando 0 parado
int funcState = 0;
// 1 curva/terminal 0 dashboard
int modeState = 0;
int menuChoice = 0;
int stop_dashboard_loop = 0;
float ki = 0;
float kp = 0;
float kd = 0;
pthread_t ovenThread;
pthread_t reportThread;
struct bme280_dev bme;


void *writeReport(void *arg) {
    while(1){
        time_t rawtime;
        struct tm *timeinfo;
        time(&rawtime);
        timeinfo = localtime(&rawtime);
        FILE *fp = fopen("data.csv", "a");
        fprintf(fp, "%s,%.2f,%.2f,%.2f,%d,%d\n", asctime(timeinfo), internalTemp, externalTemp, userTemp, valueFan, valueResistor);
        fclose(fp);
        millisAux = millisCounter;
        sleep(1);
    }
}

void *controlTemp(void *arg) {
    
    float TI, TR, TE;
    printf("KP: %f KI: %f KD:%f\n", kp, ki, kd);
    pidSetupConstants(kp, ki, kd); // 30.0, 0.2, 400.0
    pthread_create(&reportThread, NULL, writeReport, NULL);
    do {
        requestToUart(uart0_filestream, GET_INTERNAL_TEMP);
        TI = readFromUart(uart0_filestream, GET_INTERNAL_TEMP).float_value;
        internalTemp = TI;
        double value = pidControl(TI);
        pwmControl(value);
        if (value > 0) {
            valueFan = 0;
            valueResistor = value;
        } else {
            if (value <= -40) {
                valueResistor = 0;
                valueFan = value * -1;
            } else {
                valueFan = 0;
            }
        }

        if(menuChoice==2){
            requestToUart(uart0_filestream, GET_REF_TEMP);
            TR = readFromUart(uart0_filestream, GET_REF_TEMP).float_value;
            userTemp = TR;
            pidUpdateReferences(TR);
        } else if(menuChoice==2){
            TR = userTemp;
        }

        TE = stream_sensor_data_normal_mode(&bme);
        externalTemp = TE;
        printf("\nTemperaturas\nInterna: %.2f\nReferencia: %.2f\nExterna(I2C): %.2f\n", TI, TR, TE);
        if(TR > TI && TI != -1){
            turnOnResistor(100);
            turnOffFan();
            value = 100;
            sendToUart(uart0_filestream, SEND_CTRL_SIGNAL, value);
        } else if(TR <= TI && TR != -1) {
            turnOffResistor();
            turnOnFan(100);
            value = -100;
            sendToUart(uart0_filestream, SEND_CTRL_SIGNAL, value);
        }
	delay(2000);
    } while (funcState == 1);
    pthread_exit(0);
}

int shouldStopDashboard() {
    int userInput;
    if (scanf("%i", &userInput) == 1) {
        if (userInput == 3) {
            return 1;
        }
    }
    return 0;
}

void handleManualInput() {
    printf("\nEntre com o valor de kp:\n");
    scanf("%f", &kp);
    printf("\nEntre com o valor de ki:\n");
    scanf("%f", &ki);
    printf("\nEntre com o valor de kd:\n");
    scanf("%f", &kd);
    printf("\nEntre com a temperatura desejada do forno: ");
    scanf("%f", &userTemp);
    pidUpdateReferences(userTemp);
    modeState = 1;
    funcState = 1;
    pthread_create(&ovenThread, NULL, controlTemp, NULL);
}

void handleDashboardInput() {
    int command;
    kp = 30.0;
    ki = 0.2;
    kd = 400.0;
    while(!stop_dashboard_loop) {
        requestToUart(uart0_filestream, GET_USER_CMD);
        command = readFromUart(uart0_filestream, GET_USER_CMD).int_value;
        readCommand(command);
        delay(2000);
    }
}

void initMenu() {
    printf("Seja bem vindo ao trabalho 2 de FSE - Wictor Girardi!\n\n\n\n\n");
    int menuChoice;
    printf("\nDeseja entrar com dados manuais ou ter o controle pela dashboard? \n1 - Manual\n2 - Dashboard\n");
    while(menuChoice != 1 && menuChoice != 2){
        scanf("%d",&menuChoice);
    }
    if(menuChoice == 2){
        handleDashboardInput();
    } else if (menuChoice == 1){
        handleManualInput();
    }
}


void readCommand(int command) {
    switch(command) {
        case 0xA1:
            printf("FORNO - ON\n");
            sendToUartByte(uart0_filestream, SEND_SYSTEM_STATE, 1);
            systemState = 1;
            break;
        case 0xA2:
            printf("FORNO - OFF\n");
            sendToUartByte(uart0_filestream, SEND_SYSTEM_STATE, 0);
            systemState = 0;
            break;
        case 0XA3:
            printf("HEAT - ON\n");
            sendToUartByte(uart0_filestream, SEND_FUNC_STATE, 1);
            funcState = 1;
            pthread_create(&ovenThread, NULL, controlTemp, NULL);
            break;
        case 0XA4:
            printf("HEAT - OFF\n");
            sendToUartByte(uart0_filestream, SEND_FUNC_STATE, 0);
            funcState = 0;
            break;
        default:
            break;
    }
}

void closeComponents() {
    turnOffResistor();
    turnOffFan();
    close(uart0_filestream);
    pthread_cancel(reportThread);
    pthread_cancel(ovenThread);
    exit(0);
}

int main () {

    FILE *fp = fopen("data.csv", "w+");
    fprintf(fp, "DATE,TEMP_INT,TEMP_EXT,TEMP_USR,VAL_FAN,VAL_RES;\n");
    fclose(fp);
    if (wiringPiSetup () == -1) { 
        exit (1);
    }
    turnOffResistor();
    turnOffFan();
    uart0_filestream = initUart();
    bme = bme_start();
    signal(SIGINT, closeComponents);
    initMenu();
     while(1) {
        // check for user input or other events that should stop the dashboard loop
        if (shouldStopDashboard() == 1) {
            stop_dashboard_loop = 1;
            initMenu();
        }
    }
    return 0;
}