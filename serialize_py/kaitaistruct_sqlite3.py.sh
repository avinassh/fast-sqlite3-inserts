#!/usr/bin/env bash

set -eux

false &&
if [ -e kaitaistruct_sqlite3.py ]; then
  echo "keeping kaitaistruct_sqlite3.py"
  exit
fi

if ! [ -e kaitai_struct_formats/ ]; then
  if false; then
    git clone --depth=1 https://github.com/kaitai-io/kaitai_struct_formats
  else
    # sqlite3.ksy with support for lazy pages
    # needed to parse large databases (larger than RAM)
    # https://github.com/kaitai-io/kaitai_struct_formats/pull/661
    git clone --depth=1 https://github.com/milahu/kaitai_struct_formats --branch fix-sqlite3
  fi
fi

# NOTE this requires kaitai-struct-compiler with serialization support
# which can be installed with nix-shell
# https://github.com/kaitai-io/kaitai_struct/issues/1060
# https://github.com/kaitai-io/kaitai_struct_compiler/tree/serialization

kaitai-struct-compiler --read-write --no-auto-read --target python --import-path kaitai_struct_formats/ kaitai_struct_formats/database/sqlite3.ksy
mv sqlite3.py kaitaistruct_sqlite3.py

# https://github.com/kaitai-io/kaitai_struct/issues/1246
# fix: late binding breaks write_back_handler
s='s/def handler(parent, _io__raw__m_pages=_io__raw__m_pages):'
s+='/def handler(parent, _io__raw__m_pages=_io__raw__m_pages, i=i):/'
sed -i "$s" kaitaistruct_sqlite3.py
