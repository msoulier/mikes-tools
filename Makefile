INSTALLROOT=${HOME}

CC=gcc
CFLAGS=-Wall
DEBUG=

ifeq ($(DEBUG),1)
	CFLAGS += -DDEBUG
endif

.PHONY: all clean install clean

help:
	@echo "Targets:"
	@echo "    strerror"
	@echo "    countdown"
	@echo "    csize"
	@echo "    all"
	@echo "    install"
	@echo "    clean"

all: go strerror countdown csize

install: all
	if [ ! -d ${INSTALLROOT}/bin ]; then mkdir ${INSTALLROOT}/bin; fi
	cp bin/* ${INSTALLROOT}/bin && chmod 755 ${INSTALLROOT}/bin/*
	cd src/jsonpp && make install INSTALLROOT=${INSTALLROOT}
	cd src/twig && make && cp twig ${INSTALLROOT}/bin
	mv $(GPATH)/bin/* $(INSTALLROOT)/bin
	mv strerror ${INSTALLROOT}/bin
	mv countdown ${INSTALLROOT}/bin
	mv csize ${INSTALLROOT}/bin

strerror: src/strerror.c
	$(CC) $(CFLAGS) -o strerror src/strerror.c

countdown: src/countdown.c
	$(CC) $(CFLAGS) -o countdown src/countdown.c

csize: src/csize.c
	$(CC) $(CFLAGS) -o csize src/csize.c

clean:
	rm -f strerror countdown csize
	cd src/jsonpp && make clean
	cd src/twig && make clean
