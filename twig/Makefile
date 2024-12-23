CC = gcc
CFLAGS = -Wall

twig: twig.o
	$(CC) $(CFLAGS) -o twig twig.o

twig.o: twig.c
	$(CC) $(CFLAGS) -c twig.c

clean:
	rm -f twig twig.o
