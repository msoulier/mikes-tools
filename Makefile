INSTALLROOT=${HOME}

install:
	install -d ${INSTALLROOT}/bin
	install -d ${INSTALLROOT}/.irssi/scripts
	install -m 755 sane-filenames.py ${INSTALLROOT}/bin/sane-filenames
	install -m 644 mike_notify.pl ${INSTALLROOT}/.irssi/scripts/mike_notify.pl
	install -m 755 vga-on.py ${INSTALLROOT}/bin/vga-on
	install -m 755 vga-off.sh ${INSTALLROOT}/bin/vga-off
	install -m 755 weather.py ${INSTALLROOT}/bin/weather
	install -m 755 lid2suspend.py ${INSTALLROOT}/bin/lid2suspend
