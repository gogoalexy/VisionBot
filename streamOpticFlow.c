#include <stdio.h>
#include <stdint.h>
#include "serial_host.h"

int main()
{
    int8_t buf[26] = {0};
    const int fd = initSerial("/dev/ttyACM0");
    for(int i=0; i<10; ++i)
        getOpticFlow(fd, buf);
    closeSerial(fd);
    return 0;
}
