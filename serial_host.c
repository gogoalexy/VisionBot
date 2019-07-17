#include "serial_host.h"

int initSerial(char* port)
{
    // Open the serial port.
    int fd = open(port, O_RDWR);
    // Create new termios struct, we call it 'tty' for convention
    struct termios tty;
    memset(&tty, 0, sizeof(tty));
    // Read in existing settings, and handle any error
    if(tcgetattr(fd, &tty) != 0) {
        printf("Error %i from tcgetattr: %s\n", errno, strerror(errno));
    }

    tty.c_cflag &= ~PARENB; // Clear parity bit, disabling parity (most common)
    tty.c_cflag &= ~CSTOPB; // Clear stop field, only one stop bit used in communication (most common)
    tty.c_cflag |= CS8; // 8 bits per byte (most common)
    tty.c_cflag &= ~CRTSCTS; // Disable RTS/CTS hardware flow control (most common)
    tty.c_cflag |= CREAD | CLOCAL; // Turn on READ & ignore ctrl lines (CLOCAL = 1)
    tty.c_lflag &= ~ICANON;
    tty.c_lflag &= ~ECHO; // Disable echo
    tty.c_lflag &= ~ECHOE; // Disable erasure
    tty.c_lflag &= ~ECHONL; // Disable new-line echo
    tty.c_lflag &= ~ISIG; // Disable interpretation of INTR, QUIT and SUSP
    tty.c_iflag &= ~(IXON | IXOFF | IXANY); // Turn off s/w flow ctrl
    tty.c_iflag &= ~(IGNBRK|BRKINT|PARMRK|ISTRIP|INLCR|IGNCR|ICRNL); // Disable any special handling of received bytes
    tty.c_oflag &= ~OPOST; // Prevent special interpretation of output bytes (e.g. newline chars)
    tty.c_oflag &= ~ONLCR; // Prevent conversion of newline to carriage return/line feed
    // tty.c_oflag &= ~OXTABS; // Prevent conversion of tabs to spaces (NOT PRESENT ON LINUX)
    // tty.c_oflag &= ~ONOEOT; // Prevent removal of C-d chars (0x004) in output (NOT PRESENT ON LINUX)
    tty.c_cc[VTIME] = 10;    // Wait for up to 0.1s (10 deciseconds), returning as soon as any data is received.
    tty.c_cc[VMIN] = 26;
    // Set in/out baud rate
    cfsetispeed(&tty, BAUD);
    cfsetospeed(&tty, BAUD);

    // Save tty settings, also checking for error
    if (tcsetattr(fd, TCSANOW, &tty) != 0) {
        printf("Error %i from tcsetattr: %s\n", errno, strerror(errno));
    }
    return fd;
}

int getOpticFlow(int fd, int8_t buffer[], size_t length)
{
    // On success, the number of bytes written is returned.  On error, -1 is
    // returned, and errno is set to indicate the cause of the error.
    uint8_t msg[] = {0x01};
    write(fd, msg, sizeof(msg));

    memset(buffer, '\0', length);
    // Read bytes. The behaviour of read() (e.g. does it block?,
    // how long does it block for?) depends on the configuration
    // settings above, specifically VMIN and VTIME
    int num_bytes = read(fd, buffer, length);
    // n is the number of bytes read. n may be 0 if no bytes were received, and can also be -1 to signal an error.
    if (num_bytes < 0) {
        printf("Error reading: %s", strerror(errno));
    }
    return num_bytes;
}

int closeSerial(int fd)
{
    return close(fd);
}
