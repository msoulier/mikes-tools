#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

int
main(int argc, char *argv[])
{
    if (argc == 2)
    {
        errno = atoi(argv[1]);
        perror("error is");
        exit(0);
    }
    else
    {
        fprintf(stderr, "Usage: %s <error code>\n", argv[0]);
        exit(1);
    }
}
