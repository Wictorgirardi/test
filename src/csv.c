#include <time.h>
#include <stdio.h>
#include <stdlib.h>

float internalTemp = 0;
float externalTemp = 0;
float userTemp = 0;
int valueFan = 0;
int valueResistor = 0;
long millisAux = 0;
long millisCounter = 0;

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
