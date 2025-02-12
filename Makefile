INSTALLROOT=${HOME}

CC=gcc
CFLAGS=-Wall
DEBUG=
GPATH=$(GOPATH)

ifeq ($(GPATH),)
	GPATH=$(HOME)/work/go
endif

ifeq ($(DEBUG),1)
	CFLAGS += -DDEBUG
endif

.PHONY: all clean go rust install clean

help:
	@echo "Targets:"
	@echo "    go"
	@echo "    rust"
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

rust:
	if [ ! -d ${INSTALLROOT}/.cargo ]; then curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh; fi
	@echo "Installing macchina"
	nice -n 10 cargo install macchina
	#@echo "Installing uv"
	#nice -n 10 cargo install --git https://github.com/astral-sh/uv uv

go:
	rm -rf $(GPATH)/bin
	mkdir -p $(GPATH)/bin
	@echo "Installing my personal Go binaries"
	@echo "Installing weather"
	nice -n 10 go install github.com/msoulier/weather@latest
	@echo "Installing mlogd"
	go install github.com/msoulier/mlogd@latest
	@echo "Installing pcp"
	nice -n 10 go install github.com/msoulier/pcp@latest
	@echo "Installing webserver"
	nice -n 10 go install github.com/msoulier/webserver@latest
	@echo "Installing webproxy"
	nice -n 10 go install github.com/msoulier/webproxy@latest
	@echo "Installing jira"
	nice -n 10 go install github.com/msoulier/jira@latest
	#@echo "Installing tasks"
	#go install github.com/msoulier/tasks@latest
	@echo "Installing jpp"
	nice -n 10 go install github.com/msoulier/jpp@latest
	@echo "Installing additional go binaries"
	@echo "Installing glow"
	nice -n 10 go install github.com/charmbracelet/glow@latest
	@echo "Installing vhs"
	nice -n 10 go install github.com/charmbracelet/vhs@latest
	@echo "Installing gum"
	nice -n 10 go install github.com/charmbracelet/gum@latest
	@echo "Installing mods"
	nice -n 10 go install github.com/charmbracelet/mods@latest
	@echo "Installing pop"
	nice -n 10 go install github.com/charmbracelet/pop@latest
	@echo "Installing gum"
	nice -n 10 go install github.com/charmbracelet/gum@latest
	@echo "Installing godoc"
	nice -n 10 go install golang.org/x/tools/cmd/godoc@latest
	@echo "Installing goimports"
	nice -n 10 go install golang.org/x/tools/cmd/goimports@latest
	@echo "Installing hugo"
	CGO_ENABLED=1 go install -tags extended github.com/gohugoio/hugo@latest
	@echo "Installing curlie"
	nice -n 10 go install github.com/rs/curlie@latest

clean:
	rm -f strerror countdown csize
	cd src/jsonpp && make clean
	cd src/twig && make clean
