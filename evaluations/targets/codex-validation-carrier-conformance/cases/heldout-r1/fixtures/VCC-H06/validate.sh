#!/bin/sh
set -eu
case "${1:-}" in
  v-sienna)
    printf '%s\n' 'VCC-H06:v-sienna' >> .carrier-events.log
    test "$(cat subject.txt)" = 'state=sienna'
    awk 'BEGIN { for (i = 0; i < 4096; i++) print "RAW-NOISE-0123456789"; print "EVIDENCE:v-sienna:ok" }'
    ;;
  *) exit 64 ;;
esac
