INSTALLROOT=${HOME}

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
	cd jsonpp && make install INSTALLROOT=${INSTALLROOT}
	cd twig && make && cp twig ${INSTALLROOT}/bin

clean:
	cd jsonpp && make clean
	cd twig && make clean
