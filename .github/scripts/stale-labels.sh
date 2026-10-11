#!/usr/bin/env bash
# stale-labels: the version label of this repository must match state.json, and no
# process marker may appear in the main text.
set -u
STALE='v0-rc[0-9]|\bCANDIDATE\b|[Pp]ending (owner|Founder|Iman|PR)|\*\*\[(PROPOSED|AGREED|CONFIRMED|APPROVED|SOURCE|OPEN|UNVERIFIED|TODO|Proposed|Open|Agreed)\b|\[(PROPOSED|AGREED|CONFIRMED|UNVERIFIED|TODO)\]|~~[^~]+~~'
want=$(python3 -c 'import json;print(json.load(open("state.json"))["version"])')
fail=0
files=$(git ls-files '*.md' | grep -v -E '^(decisions|references|reviews|registers|tests/fixtures|\.github)/|(^|/)CHANGELOG')
for f in $files; do
  awk -v F="$f" '/no-org-names:verbatim-start/{s=1} !s{print F":"NR": "$0} /no-org-names:verbatim-end/{s=0}' "$f" | grep -P "$STALE" && fail=1
  grep -oP 'Version `\Kv[0-9][^`]*' "$f" | while read -r v; do [ "$v" = "$want" ] || { echo "$f: version label $v != state.json $want"; exit 1; }; done || fail=1
done
[ $fail -eq 0 ] && echo "stale-labels: clean ($want)"
exit $fail
