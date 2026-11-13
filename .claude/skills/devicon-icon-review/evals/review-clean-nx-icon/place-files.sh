#!/usr/bin/env bash
set -eu
# The fixture replaces devicon.json: refuse to run in a repository root
if [ -e .git ]; then
  echo "place-files.sh: run this in an empty test folder, not in a repository root" >&2
  exit 1
fi
cp -R "$(dirname "$0")/files/." .
