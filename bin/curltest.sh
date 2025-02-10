#!/bin/sh

if [ $# -lt 1 ]; then
    echo "Usage: $0 <url>" 1>&2
    exit 1
fi

URL=$1

curl "$URL" -s -o /dev/null -w \
    "response_code: %{http_code}
dns_time: %{time_namelookup}
connect_time: %{time_connect}
pretransfer_time: %{time_pretransfer}
starttransfer_time: %{time_starttransfer}
total_time: %{time_total}
"
