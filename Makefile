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

.PHONY: all clean go

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

all: go rust strerror countdown csize

install:
	mkdir -p ${INSTALLROOT}/bin
	install -d ${INSTALLROOT}/.irssi/scripts
	install -m 755 bin/sane-filenames.py ${INSTALLROOT}/bin/sf.py
	install -m 755 bin/mike_notify.pl ${INSTALLROOT}/.irssi/scripts/mike_notify.pl
	install -m 755 bin/vga-on.py ${INSTALLROOT}/bin/vga-on.py
	install -m 755 bin/vga-off.sh ${INSTALLROOT}/bin/vga-off.sh
	install -m 755 bin/weather.py ${INSTALLROOT}/bin/weather.py
	install -m 755 bin/lid2suspend.py ${INSTALLROOT}/bin/lid2suspend.py
	install -m 755 bin/manage-photos.py ${INSTALLROOT}/bin/manage-photos.py
	install -m 755 bin/rclone_proton_push.sh ${INSTALLROOT}/bin/rclone_proton_push.sh
	cd src/jsonpp && make install INSTALLROOT=${INSTALLROOT}
	cd src/twig && make && cp twig ${INSTALLROOT}/bin
	mv $(GPATH)/bin/* $(INSTALLROOT)/bin
	cp strerror ${INSTALLROOT}/bin
	cp countdown ${INSTALLROOT}/bin
	cp csize ${INSTALLROOT}/bin

strerror: strerror.c
	$(CC) $(CFLAGS) -o strerror strerror.c

countdown: countdown.c
	$(CC) $(CFLAGS) -o countdown countdown.c

csize: csize.c
	$(CC) $(CFLAGS) -o csize csize.c

rust:
	@echo "Installing macchina"
	cargo install macchina
	@echo "Installing uv"
	cargo install --git https://github.com/astral-sh/uv uv

go:
	rm -rf $(GPATH)/bin
	mkdir -p $(GPATH)/bin
	@echo "Installing my personal Go binaries"
	@echo "Installing weather"
	go install github.com/msoulier/weather@latest
	#@echo "Installing mlogd"
	#go install github.com/msoulier/mlogd@latest
	@echo "Installing pcp"
	go install github.com/msoulier/pcp@latest
	@echo "Installing webserver"
	go install github.com/msoulier/webserver@latest
	@echo "Installing webproxy"
	go install github.com/msoulier/webproxy@latest
	@echo "Installing jira"
	go install github.com/msoulier/jira@latest
	#@echo "Installing tasks"
	#go install github.com/msoulier/tasks@latest
	@echo "Installing jpp"
	go install github.com/msoulier/jpp@latest
	@echo "Installing additional go binaries"
	@echo "Installing glow"
	go install github.com/charmbracelet/glow@latest
	@echo "Installing vhs"
	go install github.com/charmbracelet/vhs@latest
	@echo "Installing gum"
	go install github.com/charmbracelet/gum@latest
	@echo "Installing mods"
	go install github.com/charmbracelet/mods@latest
	@echo "Installing pop"
	go install github.com/charmbracelet/pop@latest
	@echo "Installing gum"
	go install github.com/charmbracelet/gum@latest
	@echo "Installing godoc"
	go install golang.org/x/tools/cmd/godoc@latest
	@echo "Installing goimports"
	go install golang.org/x/tools/cmd/goimports@latest
	@echo "Installing hugo"
	CGO_ENABLED=1 go install -tags extended github.com/gohugoio/hugo@latest
	@echo "Installing curlie"
	go install github.com/rs/curlie@latest

clean:
	rm -f strerror countdown csize
	cd src/jsonpp && make clean
	cd src/twig && make clean
