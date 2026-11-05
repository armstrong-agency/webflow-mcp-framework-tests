#!/bin/sh
# Checks every hash in PREREGISTRATION.md. The two files revised after the runs
# are checked against their pre-registered copies in preregistered/scripts/.
cd "$(dirname "$0")" || exit 2
grep -E '^ +[0-9a-f]{64}  ' PREREGISTRATION.md \
  | sed -E 's/^ +//; s#  scripts/(e1a_key|vocab)\.py#  preregistered/scripts/\1.py#' \
  | shasum -a 256 -c
