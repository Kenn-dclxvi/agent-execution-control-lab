#!/bin/sh
set -eu
case "${1:-}" in
  v-ivory)
    printf '%s\n' 'VCC-H04:v-ivory' >> .carrier-events.log
    test "$(cat subject.txt)" = 'state=violet'
    printf '%s\n' 'EVIDENCE:v-ivory:ok'
    ;;
  v-russet)
    printf '%s\n' 'VCC-H04:v-russet' >> .carrier-events.log
    printf '%s\n' 'EVIDENCE:v-russet:failed'
    exit 9
    ;;
  v-cyan)
    printf '%s\n' 'VCC-H04:v-cyan' >> .carrier-events.log
    printf '%s\n' 'EVIDENCE:v-cyan:unexpected'
    ;;
  *) exit 64 ;;
esac
