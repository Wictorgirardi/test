#include <fcntl.h>  //Used for UART
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>  //Used for UART
#include <unistd.h>   //Used for UART

#include "uart.h"
#include "crc16.h"

int initUart(){
    int uart0_filestream = -1;
    char uart_path[] = "/dev/serial0";
    uart0_filestream = open(uart_path, O_RDWR | O_NOCTTY | O_NDELAY);
    if(uart0_filestream == -1){
        printf("Erro - Não foi possível iniciar a UART.\n");
    }
    else {
        printf("UART inicializada!\n");
    }
    struct termios options;
    tcgetattr(uart0_filestream, &options);
    options.c_cflag = B9600 | CS8 | CLOCAL | CREAD;
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;
    options.c_lflag = 0;
    tcflush(uart0_filestream, TCIFLUSH);
    tcsetattr(uart0_filestream, TCSANOW, &options);
    return uart0_filestream;
}

void requestToUart(int uart0_filestream, unsigned char code){
    unsigned char package[7] = {0x01, 0x23, code, 0x03, 0x02, 0x00, 0x00};
    short crc = calcula_CRC(package, 7);

    unsigned char message[9];
    memcpy(message, &package, 7);
    memcpy(&message[7], &crc, 2);
    int check = write(uart0_filestream, &message[0], 9);
    if(check < 0){
        printf("Ocorreu um erro na comunicação com o UART\n");
    }

    sleep(1);
}

void sendToUart(int uart0_filestream, unsigned char code, int value){
    unsigned char package[7] = {0x01, 0x16, code, 0x03, 0x02, 0x00, 0x00};
    unsigned char message[13];

    memcpy(message, &package, 7);
    memcpy(&message[7], &value, 4);

    short crc = calcula_CRC(message, 11);

    memcpy(&message[11], &crc, 2);

    int check = write(uart0_filestream, &message[0], 13);

    if(check < 0){
        printf("Ocorreu um erro na comunicação com o UART\n");
    }
    sleep(1);
}

Number_type readFromUart(int uart0_filestream, unsigned char code){
    unsigned char buffer[20];
    Number_type number = {-1, -1.0};

    int receivedBytes = read(uart0_filestream, buffer, 20);
    if(receivedBytes == 0){
        printf("Nenhum dado disponível.\n");
    }
    else if(receivedBytes < 0){
        printf("Erro na leitura.\n");
    }
    else {
        buffer[receivedBytes] = '\0';
        if (code == 0xC3){
            memcpy(&number.int_value, &buffer[3], sizeof(int));
        }
        else{
            memcpy(&number.float_value, &buffer[3], sizeof(float));
        }
        return number;
    }
    return number; 
}

void sendToUartByte(int uart0_filestream, unsigned char code, char value) {
    unsigned char package[7] = {0x01, 0x16, code, 0x03, 0x02, 0x00, 0x00};
    unsigned char message[10];

    memcpy(message, &package, 7);
    memcpy(&message[7], &value, 1);

    short crc = calcula_CRC(message, 8);

    memcpy(&message[8], &crc, 2);

    int check = write(uart0_filestream, &message[0], 10);

    if(check < 0){
        printf("Ocorreu um erro na comunicação com o UART\n");
    }
    sleep(1);
}

void closeUart(int uart0_filestream){
    printf("Finalizando conexão UART!\n");
    close(uart0_filestream);
}
