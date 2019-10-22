#include <stdio.h>
#include <stdint.h>
#include "serial_host.h"

int main()
{
    int8_t buf[sizePacket] = {0};
    const int fd = initSerial("/dev/ttyACM0");
    for(int i=0; i<10; ++i)
    {
        getOpticFlow(fd, buf, sizePacket);
        /*int8_t msg[] = {0x01};
        write(fd, msg, sizeof(msg));
        memset(&buf, '\0', sizeof(buf));
        int num_bytes = read(fd, &buf, sizeof(buf));
        // n is the number of bytes read. n may be 0 if no bytes were received, and can also be -1 to signal an error.
        if (num_bytes < 0) {
            printf("Error reading: %s", strerror(errno));
        }*/
        sleep(1);
        for (int j=0; j<sizePacket; ++j)
            printf("%d ", buf[j]);
        printf("\n");
    }
    closeSerial(fd);
    return 0;
}
