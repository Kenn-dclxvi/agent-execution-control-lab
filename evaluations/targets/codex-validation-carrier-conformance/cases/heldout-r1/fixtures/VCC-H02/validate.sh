#!/bin/sh
set -eu
case "${1:-}" in
  v-ochre)
    printf '%s\n' 'VCC-H02:v-ochre' >> .carrier-events.log
    test "$(cat subject.txt)" = 'state=amber'
    printf '%s\n' 'EVIDENCE:v-ochre:ok'
    ;;
  v-slate)
    printf '%s\n' 'VCC-H02:v-slate' >> .carrier-events.log
    test "$(cat subject.txt)" = 'state=amber'
    printf '%s\n' 'EVIDENCE:v-slate:ok'
    ;;
  *) exit 64 ;;
esac
