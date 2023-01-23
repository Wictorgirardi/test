#include "display.h"

int fd;

void printTemp(float intTemp, float extTemp, float refTemp)   {

  if (wiringPiSetup () == -1) exit (1);

  fd = wiringPiI2CSetup(I2C_ADDR_LCD);

  startDisplay();
  displayLoc(LINE1);
  typeln("TI: ");
  typeFloat(intTemp);
  typeln(" TE: ");
  typeFloat(extTemp);
  displayLoc(LINE2);
  typeln(" TR: ");
  typeFloat(refTemp);
}

void typeFloat(float myFloat)   {
  char buffer[20];
  sprintf(buffer, "%4.2f",  myFloat);
  typeln(buffer);
}

void typeInt(int myInt)   {
  char buffer[20];
  sprintf(buffer, "%d",  myInt);
  typeln(buffer);
}

void clrLcd(void)   {
  lcdByte(0x01, LCD_CMD);
  lcdByte(0x02, LCD_CMD);
}

void displayLoc(int line)   {
  lcdByte(line, LCD_CMD);
}

void typeln(const char *s)   {

  while ( *s ) lcdByte(*(s++), LCD_CHR);

}

void lcdByte(int bits, int mode)   {
  //Send byte to data pins
  // bits = the data
  // mode = 1 for data, 0 for command
  int bits_high;
  int bits_low;
  // uses the two half byte writes to LCD
  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT;
  bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT;

  // High bits
  wiringPiI2CReadReg8(fd, bits_high);
  lcdToggleEnable(bits_high);

  // Low bits
  wiringPiI2CReadReg8(fd, bits_low);
  lcdToggleEnable(bits_low);

}

void lcdToggleEnable(int bits)   {
  delayMicroseconds(500);
  wiringPiI2CReadReg8(fd, (bits | ENABLE));
  delayMicroseconds(500);
  wiringPiI2CReadReg8(fd, (bits & ~ENABLE));
  delayMicroseconds(500);
}


void startDisplay()   {
  // Initialise display
  lcdByte(0x33, LCD_CMD); // Initialise
  lcdByte(0x32, LCD_CMD); // Initialise
  lcdByte(0x06, LCD_CMD); // Cursor move direction
  lcdByte(0x0C, LCD_CMD); // 0x0F On, Blink Off
  lcdByte(0x28, LCD_CMD); // Data length, number of lines, font size
  lcdByte(0x01, LCD_CMD); // Clear display
  delayMicroseconds(500);
}
