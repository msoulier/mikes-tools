#!/usr/bin/awk -f

BEGIN {
    interested = 0
    result = 0
}

/^Summary/ { interested = ! interested; next }

interested { print }

/^Recommended Result/ { interested = ! interested; result = 1; next }

result && !/^$/ { print; result = 0 }
