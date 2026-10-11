#!/usr/bin/env bash
# frozen-records: see .github/workflows/frozen-records.yml.
set -u
[ -n "${BASE:-}" ] || { echo "No pull request base; nothing to compare."; exit 0; }
DR1='decisions/DR-0001-49gaion-v1-0-0-day-zero.md'
fail=0
while IFS=$'\t' read -r st a b; do
  [ -n "$st" ] || continue
  case "$a ${b:-}" in *decisions/DR-*) ;; *) continue;; esac
  case "$st" in
    A)  if [ "$REPO" = 49GAION ] && [[ "$a" =~ ^decisions/DR-[0-9]{4}-[a-z0-9-]+\.md$ ]]; then echo "ok   added $a"
        else echo "FAIL added $a (new decision records are added only in the 49GAION hub, as decisions/DR-####-*.md)"; fail=1; fi ;;
    D)  if [ "$REPO" != 49GAION ] && [ "$a" = "$DR1" ]; then echo "ok   deleted copy $a (the record is kept in the hub)"
        else echo "FAIL deleted $a (decision records are never deleted)"; fail=1; fi ;;
    *)  echo "FAIL $st $a ${b:-} (decision records are never edited or renamed)"; fail=1 ;;
  esac
done < <(git diff --name-status -M "$BASE"...HEAD)
[ $fail -eq 0 ] && echo "frozen-records: clean" || echo "::error::A decision record was edited, renamed or deleted (listed above). Records are never edited; record a new decision instead."
exit $fail
