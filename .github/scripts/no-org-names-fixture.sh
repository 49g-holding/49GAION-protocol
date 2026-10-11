#!/usr/bin/env bash
# Fixture test for the no-org-names scanner: every line of bad-names.txt must be flagged
# and no line of good-names.txt may be flagged. S (env) is the scanner to test; CI passes
# the one from main.
set -u
D=tests/fixtures/no-org-names; S="${S:-.github/scripts/no-org-names.sh}"; fail=0
total=$(grep -c . $D/bad-names.txt); flagged=$(bash $S --lines $D/bad-names.txt | wc -l)
echo "bad-names: $flagged of $total flagged"; [ "$flagged" -eq "$total" ] || fail=1
good=$(bash $S --file $D/good-names.txt); [ -z "$good" ] && echo "good-names: none flagged" || { echo "good-names flagged:"; echo "$good"; fail=1; }
exit $fail
