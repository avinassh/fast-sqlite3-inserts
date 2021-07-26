#!/bin/sh -ex

base="$(dirname `realpath $0`)"

cd "$base"

export PKG_CONFIG_PATH="$base/sqlite3"
export SQLITE3_STATIC=1

exec cargo build --release $@
