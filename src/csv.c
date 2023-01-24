#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include "variables.h"

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
