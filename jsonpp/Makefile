PREFIX=${HOME}
CC=g++
CFLAGS=-Wall -DLINUX --std=c++11 -I.
OBJS=jsonpp.o
LIBS=
OS := $(shell uname -s)
DEBUG=0

# Using jsoncpp from git
# 42e892d96e47b1f6e29844cc705e148ec4856448
# amalgamated

ifeq ($(DEBUG),1)
	CFLAGS += -ggdb -fsanitize=address
endif

ifeq ($(OS),Linux)
	CFLAGS+=-DLINUX
endif

all: jsonpp

jsonpp: $(OBJS)
	$(CC) $(CFLAGS) -o jsonpp $(OBJS) $(LIBS)

jsonpp.o: jsonpp.cpp nlohmann/json.hpp
	$(CC) $(CFLAGS) -c jsonpp.cpp

install: jsonpp
	cp jsonpp $(PREFIX)/bin

tags:
	ctags *.cpp *.hpp

clean:
	rm -f *.a *.o jsonpp
