#!/usr/bin/env bash
# fetch.sh <repo> <dir> <ref>: shallow-clone a public 49GAION repository at <ref>,
# falling back to main when <ref> is empty or no longer exists.
set -eu
repo=$1; dir=$2; ref=${3:-main}
url="https://github.com/49g-holding/$repo.git"
if [ -z "$ref" ] || ! git ls-remote --exit-code --heads "$url" "$ref" >/dev/null 2>&1; then ref=main; fi
echo "$repo at $ref"
git clone -q --depth 1 --branch "$ref" "$url" "$dir"
