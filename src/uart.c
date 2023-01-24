#include <fcntl.h> // Contains file controls like O_RDWR
#include <stdio.h> // Contains printf
#include <stdlib.h> // Contains exit
#include <string.h> // Contains string functions
#include <termios.h> // Contains POSIX terminal control definitions
#include <unistd.h>  // write(), read(), close()

#include "uart_defs.h" // Contains UART definitions
#include "crc16.h" // Contains CRC16 definitions

int initUart(){
    int uart_filestream = -1;
    char uart_path[] = "/dev/serial0";
    uart_filestream = open(uart_path, O_RDWR | O_NOCTTY | O_NDELAY);
    if(uart_filestream == -1){
        printf("Erro ao abrir o UART\n");
        exit(1);
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
    sleep(1);
}

void sendToUart(int uart_filestream, unsigned char code, int value){
    unsigned char package[7] = {0x01, 0x16, code, 0x07, 0x03, 0x02, 0x06};
    unsigned char message[13];

    memcpy(message, &package, 7);
    memcpy(&message[7], &value, 4);

    short crc = calcula_CRC(message, 11);

    memcpy(&message[11], &crc, 2);

    int check = write(uart_filestream, &message[0], 13);
    sleep(1);
}

Number_type readFromUart(int uart_filestream, unsigned char code){
    unsigned char buffer[20];
    Number_type number = {-1, -1.0};

    int content = read(uart_filestream, buffer, 20);
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

    memcpy(&message[8], &crc, 2);

    int check = write(uart_filestream, &message[0], 10);

    if(check < 0){
        printf("Ocorreu um erro na comunicação com o UART\n");
    }
    sleep(1);
}
