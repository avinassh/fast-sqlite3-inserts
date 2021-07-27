#!/bin/sh -ex

base="$(dirname `realpath $0`)"

cd "$base"

clang -O2 -flto -march=native -c sqlite3.c -o sqlite3.o
ar crus libsqlite3.a sqlite3.o

mkdir -p pkgconfig
exec cat >pkgconfig/sqlite3.pc << EOF
# Package Information for pkg-config

prefix="${base}"
exec_prefix=\${prefix}
libdir=\${exec_prefix}
includedir=\${prefix}

Name: SQLite
Description: SQL database engine
Version: 3.36.0
Libs: -L\${libdir} -lsqlite3 -lm -ldl -lz -lpthread
Cflags: -I\${includedir}
EOF
