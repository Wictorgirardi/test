#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <unistd.h> 

#include "uart_defs.h"
#include "crc16.h"

const int initUart(){
    ssize_t uart_filestream = -1;
    const char uart_path[] = "/dev/serial0";
    uart_filestream = open(uart_path, O_RDWR | O_NOCTTY | O_NDELAY);
    if(uart_filestream == -1){
        printf("Não foi possível iniciar a Uart.\n");
    }
    else {
        printf("UART inicializado.\n");
    }
    struct termios options;
    tcgetattr(uart_filestream, &options);
    options.c_cflag = B9600 | CS8 | CLOCAL | CREAD;
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;
    options.c_lflag = 0;
    tcflush(uart_filestream, TCIFLUSH);
    tcsetattr(uart_filestream, TCSANOW, &options);
    return uart_filestream;
}

void requestToUart(int uart_filestream, unsigned char code){
    unsigned char package[7] = {0x01, 0x23, code, 0x07, 0x03, 0x02, 0x06};
    short crc = calcula_CRC(package, 7);

    unsigned char message[9];
    memcpy(message, &package, 7);
    memcpy(&message[7], &crc, 2);
    int check = write(uart_filestream, &message[0], 9);
    if(check < 0){
        printf("Ocorreu um erro na comunicação com o UART\n");
    }
}

void sendToUart(int uart_filestream, unsigned char code, int value){
    unsigned char package[7] = {0x01, 0x16, code, 0x07, 0x03, 0x02, 0x06};
    unsigned char message[13];

    memcpy(message, &package, 7);
    memcpy(&message[7], &value, 4);

    short crc = calcula_CRC(message, 11);

    memcpy(&message[11], &crc, 2);
    int check = write(uart_filestream, &message[0], 13);

if(check < 0){
    printf("Ocorreu um erro na comunicação com o UART\n");
}
}

const Number_type readFromUart(int uart_filestream, unsigned char code){
unsigned char buffer[10];
const Number_type number = {-1, -1.0};
int content = read(uart_filestream, buffer, 10);
if(!content){
    printf("Nenhum dado foi recebido\n");
}
else if(content < 0){
    printf("Erro ao ler dados\n");
}
else {
    buffer[content] = '\0';
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

void sendToUartByte(int uart_filestream, unsigned char code, char value) {
unsigned char package[7] = {0x01, 0x16, code, 0x07, 0x03, 0x02, 0x06};
unsigned char message[10];
memcpy(message, &package, 7);
memcpy(&message[7], &value, 1);

short crc = calcula_CRC(message, 8);

memcpy(&message[8], sizeof(short), &crc, 2);

int check = write(uart_filestream, &message[0], 10);

if(check < 0){
    printf("Ocorreu um erro na comunicação com o UART\n");
}
}