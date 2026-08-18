#!/bin/sh
set -eu
case "${1:-}" in
  v-coral)
    printf '%s\n' 'VCC-H03:v-coral' >> .carrier-events.log
    printf '%s\n' 'EVIDENCE:v-coral:failed'
    exit 7
    ;;
  v-mint)
    printf '%s\n' 'VCC-H03:v-mint' >> .carrier-events.log
    printf '%s\n' 'EVIDENCE:v-mint:unexpected'
    ;;
  *) exit 64 ;;
esac
