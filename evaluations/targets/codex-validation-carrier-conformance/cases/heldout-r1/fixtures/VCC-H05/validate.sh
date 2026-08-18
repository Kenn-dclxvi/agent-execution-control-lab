#!/bin/sh
set -eu
case "${1:-}" in
  v-indigo)
    printf '%s\n' 'VCC-H05:v-indigo:start' >> .carrier-events.log
    sleep 2
    test "$(cat subject.txt)" = 'state=indigo'
    printf '%s\n' 'VCC-H05:v-indigo:terminal' >> .carrier-events.log
    printf '%s\n' 'EVIDENCE:v-indigo:ok'
    ;;
  *) exit 64 ;;
esac
