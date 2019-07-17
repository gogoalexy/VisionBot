#ifndef SERIAL_HOST_H

// C library headers
#include <stdio.h>
#include <string.h>
#include <stdint.h>
// Linux headers
#include <fcntl.h> // Contains file controls like O_RDWR
#include <errno.h> // Error integer and strerror() function
#include <termios.h> // Contains POSIX terminal control definitions
#include <unistd.h> // write(), read(), close()

#define BAUD B115200
#define sizePacket 26

#ifdef __cplusplus
extern "C" {
#endif

int initSerial(char* port);
int getOpticFlow(int fd, int8_t buffer[], size_t length);
int closeSerial(int fd);

#ifdef __cplusplus
}
#endif

#define SERIAL_HOST_H
#endif
