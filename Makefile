INSTALLROOT=${HOME}

install:
	install -d ${INSTALLROOT}/bin
	install -d ${INSTALLROOT}/.irssi/scripts
	install -m 755 sane-filenames.py ${INSTALLROOT}/bin/sf.py
	install -m 755 mike_notify.pl ${INSTALLROOT}/.irssi/scripts/mike_notify.pl
	install -m 755 vga-on.py ${INSTALLROOT}/bin/vga-on.py
	install -m 755 vga-off.sh ${INSTALLROOT}/bin/vga-off.sh
	install -m 755 weather.py ${INSTALLROOT}/bin/weather.py
	install -m 755 lid2suspend.py ${INSTALLROOT}/bin/lid2suspend.py
	install -m 755 manage-photos.py ${INSTALLROOT}/bin/manage-photos.py
	cd jsonpp && make install INSTALLROOT=${INSTALLROOT}
	cd twig && make && cp twig ${INSTALLROOT}/bin

clean:
	cd jsonpp && make clean
	cd twig && make clean
