#!/bin/sh -ex

base="$(dirname `realpath $0`)"

cd "$base"

export SQLITE3_LIB_DIR="$base/sqlite3"
export PKG_CONFIG_PATH="$SQLITE3_LIB_DIR/pkgconfig"
export SQLITE3_STATIC=1

pkg-config sqlite3 --cflags --libs

exec cargo build --release $@
