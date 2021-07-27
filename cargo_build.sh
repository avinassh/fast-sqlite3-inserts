#!/bin/sh -ex

base="$(dirname `realpath $0`)"

cd "$base"

# SQLITE3_LIB_DIR is necessary the directory of statically linked library.
# Otherwise, libsqlite3-sys would just use the global dynamic library
export SQLITE3_LIB_DIR="$base/sqlite3"
# SQLITE3_STATIC is necessary to statically linked with libsqlite3.a
export SQLITE3_STATIC=1
# SQLITE3_INCLUDE_DIR is necessary since libsqlite3-sys does not use sqlite3.pc
# found using `SQLITE3_LIB_DIR` for locating the header.
export SQLITE3_INCLUDE_DIR="$SQLITE3_LIB_DIR"

export PKG_CONFIG_PATH="$SQLITE3_LIB_DIR/pkgconfig"

exec cargo build --release -vv $@
