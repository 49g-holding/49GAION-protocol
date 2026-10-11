#!/usr/bin/env bash
# no-org-names scanner.
# Two checks:
#  FULL  - organisation-specific names, hosts, 49-prefixed codes and the bare name of one organisation's product.
#          Applied to every tracked text file except .github/ and
#          tests/fixtures/no-org-names/bad-names.txt. Only text between the markers
#          <!-- no-org-names:verbatim-start --> and <!-- no-org-names:verbatim-end -->
#          (the approved product-release section of the 49GAION README) is skipped.
#  PILOT - private organisation detail (company names, private hosts and domains, e-mail
#          addresses, Drive and folder IDs or paths, user IDs, IP addresses, company legal
#          names, and the company written other than 49G). Applied to the same files,
#          markers ignored.
# Usage: no-org-names.sh             -> scan the repository in the current directory
#        no-org-names.sh --lines F   -> lines of F flagged by FULL (fixture test)
#        no-org-names.sh --file F    -> lines of F flagged by FULL or PILOT
set -u
PATTERN='(?i)49[\s_-]*gr[o]up|founder[ -]office|ceo[ -]office|engineering[ -]foundry|cto[ -]office|\bEF\b|\bITI\b|(?<![/\w])49(aioc|hoac|hop)[-\w]*|49gfo|founder-personal|bit[l]ease|\b49G\b|(?<!\w)49a[i]on\b'
PILOT='(?i)49[\s_-]*gr[o]up|bit[l]ease|drive\.google\.com|docs\.google\.com|/folders/|my drive/|(?-i:\b(?=1)(?=[A-Za-z0-9_-]*[A-Z])(?=[A-Za-z0-9_-]*[a-z])(?=[A-Za-z0-9_-]*[0-9])[A-Za-z0-9_-]{25,44}\b)|(?-i:\bU(?=[0-9A-Z]*[0-9])[0-9A-Z]{8,11}\b)|[\w.+-]+@[a-z0-9-]+\.[a-z]{2,}|\b\d{1,3}(?:\.\d{1,3}){3}\b|\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:internal|local|lan|corp|intranet)\b|(?<![\w.-])(?:[a-z0-9-]+\.)*49g?\.(?:dev|com|io|net|org|ai|app|cloud|co\.uk|uk)\b|\b(?:ltd|llc|plc|fze|fzco|fz-llc|gmbh)\b'
allow() { sed -E 's#https?://github\.com/49g-holding/49GAION(-protocol|-aioc)?([/#][A-Za-z0-9._/#-]*)?#<GH>#g; s#49g-holding/49GAION(-protocol|-aioc)?\b#<GHREPO>#g; s#\b49g-holding\b#<GHORG>#g'; }
lines() { awk -v F="$1" '/no-org-names:verbatim-start/{s=1} !s{print F":"NR": "$0} /no-org-names:verbatim-end/{s=0}' "$1"; }
raw() { awk -v F="$1" '{print F":"NR": "$0}' "$1"; }
check() { lines "$1" | allow | grep -P "$PATTERN"; raw "$1" | allow | grep -P "$PILOT"; }
if [ "${1:-}" = "--lines" ]; then lines "$2" | allow | grep -P "$PATTERN"; exit 0; fi
if [ "${1:-}" = "--file" ]; then check "$2" | sort -u; exit 0; fi
git ls-files | grep -v -E '^\.github/' | grep -v -x 'tests/fixtures/no-org-names/bad-names.txt' | while IFS= read -r f; do
  [ -f "$f" ] && grep -Iq . "$f" || continue
  check "$f"
done | sort -u
exit 0
