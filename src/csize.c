#include <stdio.h>

#ifdef __clang__

#elif __GNUC__

#endif

int main(void) {
    printf("int size on this platform is %ld bits\n", sizeof(int)*8);
    printf("short int size on this platform is %ld bits\n", sizeof(short int)*8);
    printf("long int size on this platform is %ld bits\n", sizeof(long int)*8);
    printf("long long int size on this platform is %ld bits\n", sizeof(long int)*8);
    printf("float size on this platform is %ld bits\n", sizeof(float)*8);
    printf("double size on this platform is %ld bits\n", sizeof(double)*8);
    printf("long double size on this platform is %ld bits\n", sizeof(long double)*8);
#ifdef __GNUC__
    printf("using gcc version %d.%d.%d\n", __GNUC__, __GNUC_MINOR__, __GNUC_PATCHLEVEL__);
#endif

    return 0;
}
