#ifndef CONTROL_LCD_
#define CONTROL_LCD_

#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <stdlib.h>
#include <stdio.h>

// Define some device parameters
#define I2C_ADDR_LCD 0x27 // I2C device address

// Define some device constants
#define LCD_CHR 1 // Mode - Sending data
#define LCD_CMD 0 // Mode - Sending command

#define LINE1 0x80 // 1st line
#define LINE2 0xC0 // 2nd line

#define LCD_BACKLIGHT 0x08 // On
// LCD_BACKLIGHT = 0x00  # Off

#define ENABLE 0b00000100 // Enable bit


void startDisplay(void);
void printTemp(float intTemp, float extTemp, float refTemp);
void printHeating();
void lcdByte(int bits, int mode);
void lcdToggleEnable(int bits);
void clrLcd(void);    // clr LCD return home

// added by Lewis
void typeFloat(float myFloat);
void displayLoc(int line);
void typeln(const char *s);
void typeInt(int myInt);

#endif