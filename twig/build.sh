#!/bin/sh

echo "Creating Makefile.am"
cat > Makefile.am <<EOF
bin_PROGRAMS=twig
twig_SOURCES=twig.c
EOF

echo "Running autoscan..."
autoscan

echo "Creating configure.ac..."
sed -e 's/FULL-PACKAGE-NAME/twig/' \
    -e 's/VERSION/1.0/'   \
    -e 's|BUG-REPORT-ADDRESS|msoulier@digitaltorque.ca|' \
    -e '10i\
    AM_INIT_AUTOMAKE' \
        < configure.scan > configure.ac

echo "Creating additional files..."
touch NEWS README AUTHORS ChangeLog

echo "Running autoreconf..."
autoreconf -iv

echo "Running configure..."
./configure

echo "Running make distcheck to package sources..."
make distcheck
