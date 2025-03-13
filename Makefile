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
	@echo "    mcount"
	@echo "    csize"
	@echo "    all"
	@echo "    install"
	@echo "    clean"

all: strerror mcount csize

install: all
	if [ ! -d ${INSTALLROOT}/bin ]; then mkdir ${INSTALLROOT}/bin; fi
	cp bin/* ${INSTALLROOT}/bin && chmod 755 ${INSTALLROOT}/bin/*
	cd src/jsonpp && make install INSTALLROOT=${INSTALLROOT}
	cd src/twig && make && cp twig ${INSTALLROOT}/bin
	mv strerror ${INSTALLROOT}/bin
	mv mcount ${INSTALLROOT}/bin
	mv csize ${INSTALLROOT}/bin

strerror: src/strerror.c
	$(CC) $(CFLAGS) -o strerror src/strerror.c

mcount: src/mcount.c
	$(CC) $(CFLAGS) -o mcount src/mcount.c

csize: src/csize.c
	$(CC) $(CFLAGS) -o csize src/csize.c

clean:
	rm -f strerror mcount csize
	cd src/jsonpp && make clean
	cd src/twig && make clean
