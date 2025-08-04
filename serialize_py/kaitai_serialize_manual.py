#!/usr/bin/env python3

good_database_path = "test_kaitai.py.good.db"
bad_database_path = "test_kaitai.py.bad.db"

# FIXME vlq_base128_be.VlqBase128Be has no value setter
# expected API: vlq_base128_be.VlqBase128Be.from_value(123)
"""
>>> import vlq_base128_be
>>> i = vlq_base128_be.VlqBase128Be()
>>> i.value = 123
AttributeError: property 'value' of 'VlqBase128Be' object has no setter
"""

import io

# https://github.com/kaitai-io/kaitai_struct_python_runtime
import kaitaistruct

import kaitaistruct_sqlite3
import vlq_base128_be
import pyvlq # https://github.com/osoken/pyvlq/blob/main/src/pyvlq/core.py

def set_value(on_kn, v):
    keys = on_kn.split(".")
    on = keys.pop(0)
    o = eval(on)
    for key in keys[:-1]:
      o = getattr(o, key)
    key = keys.pop()
    print(f"setting {on_kn} = {v!r}")
    setattr(o, key, v)
    return v

def print_keys(on):
    o = eval(on)
    ignore = ("close", "from_bytes", "from_file", "from_io")
    f = lambda a: "a" <= a[0] <= "z" and a not in ignore
    print(f"{on} keys:", " ".join(filter(f, dir(o))))

def print_value(on_kn):
    keys = on_kn.split(".")
    on = keys.pop(0)
    val = eval(on)
    print(f"{on_kn} = ", end="")
    try:
      for key in keys:
        val = getattr(val, key)
      print(repr(val))
    except Exception as exc: print("error:", exc)

def print_value(on_kn):
    print(f"{on_kn} = ", end="")
    try:
      val = eval(on_kn)
      print(repr(val))
    except Exception as exc: print("error:", exc)

def check(on):
    o = eval(on)
    try: print(f"checking {on}: ", end=""); o._check(); print("ok")
    except Exception as exc: print("error:", exc)

def write(on):
    o = eval(on)
    _io.seek(0) # fix: _write__seq does not seek before writing
    try: print(f"writing {on}: ", end=""); o._write(_io); print("ok")
    except Exception as exc: print("error:", exc)

page_size = 4096

num_pages = 2

# _io = kaitaistruct.KaitaiStream(io.BytesIO(bytearray(num_pages * page_size)))
# FIXME add extra space for database header
_io = kaitaistruct.KaitaiStream(io.BytesIO(bytearray(num_pages * page_size + 100)))

if 1:
    root = kaitaistruct_sqlite3.Sqlite3(_io)
else:
    class PatchedSqlite3(kaitaistruct_sqlite3.Sqlite3):
        def _write(self, io=None):
            self._write__seq(io)
            # self._fetch_instances() # this would throw
            self._io.write_back_child_streams()
    root = PatchedSqlite3(_io)

# print("kaitaistruct_sqlite3", dir(kaitaistruct_sqlite3))
# print("root", dir(root))

root.header = root.DatabaseHeader(root._io, root, root._root)

print_keys("root")
print_keys("root.header")

print_value("root.header.len_page")
# AttributeError: 'Sqlite3' object has no attribute 'len_page_mod'

# u2 @ 0x10 = 16
set_value("root.header.page_size_raw", page_size if page_size < 65536 else 1)
print_value("root.header.len_page") # derived from root.header.page_size_raw
print_keys("root.header")

write("root")
# AttributeError: 'Sqlite3' object has no attribute 'magic'

#  00000000: 5351 4c69 7465 2066 6f72 6d61 7420 3300  SQLite format 3.
set_value("root.header.magic", b"SQLite format 3\0") # 16 bytes @ 0x0
# set_value("root.header.magic", b"some_magic_strr\0") # test
print_keys("root.header")

write("root")
# AttributeError: 'Sqlite3' object has no attribute 'read_version'. Did you mean: 'write_version'?

set_value("root.header.read_version", 0)
print_keys("root.header")

write("root")
# AttributeError: 'Sqlite3' object has no attribute 'reserved_space'

#  00000000: 5351 4c69 7465 2066 6f72 6d61 7420 3300  SQLite format 3.
set_value("root.header.magic", b"SQLite format 3\0") # 16 bytes @ 0x0

#  00000010: 1000 0101 0040 2020 0000 0001 0000 0002  .....@  ........
set_value("root.header.len_page_mod", page_size if page_size < 65536 else 1) # u2 @ 0x10: 4096 == 0x1000
set_value("root.header.write_version", 1) # u1 @ 0x12
set_value("root.header.read_version", 1) # u1 @ 0x13
set_value("root.header.page_reserved_space_size", 0) # u1 @ 0x14
set_value("root.header.max_payload_fraction", 64) # u1 @ 0x15: 64 == 0x40
set_value("root.header.min_payload_fraction", 32) # u1 @ 0x16: 32 == 0x20
set_value("root.header.leaf_payload_fraction", 32) # u1 @ 0x17: 32 == 0x20
set_value("root.header.file_change_counter", 1) # u4 @ 0x18
set_value("root.header.num_pages", num_pages) # u4 @ 0x1b

#  00000020: 0000 0000 0000 0000 0000 0001 0000 0004  ................
# set_value("root.header.first_freelist_trunk_page", 0) # u4 @ 0x20
root.header.first_freelist_trunk_page = root.FreelistTrunkPagePointer() # u4 @ 0x20#
root.header.first_freelist_trunk_page.page_number = 0
set_value("root.header.num_freelist_pages", 0) # u4 @ 0x24
set_value("root.header.schema_cookie", 1) # u4 @ 0x28
set_value("root.header.schema_format", 4) # u4 @ 0x2b

#  00000030: 0000 0000 0000 0000 0000 0001 0000 0000  ................
set_value("root.header.default_page_cache_size", 0) # u4 @ 0x30
set_value("root.header.largest_root_page", 0) # u4 @ 0x34
set_value("root.header.text_encoding", 1) # utf8 # u4 @ 0x38
set_value("root.header.user_version", 0) # u4 @ 0x3b

#  00000040: 0000 0000 0000 0000 0000 0000 0000 0000  ................
set_value("root.header.is_incremental_vacuum", 0) # u4 @ 0x40
set_value("root.header.application_id", 0) # u4 @ 0x44

#  00000050: 0000 0000 0000 0000 0000 0000 0000 0001  ................
set_value("root.header.reserved_header_bytes", b"\x00" * 20) # 20 bytes @ 0x48
set_value("root.header.version_valid_for", 1) # u4 @ 0x5b

#            0011 2233 4455 6677 8899 aabb ccdd eeff
#  00000060: 002e 8a11 0d00 0000 010f cc00 0fcc 0000  ................
#                                          ^^^^ cell_ptr.ofs_content
#                                          ^^^^ page.cell_pointers[0] @ 0x6c
#                                       ^^ page.num_frag_free_bytes
#                                  ^^^^ page.ofs_cell_content_area_raw
#                             ^^ ^^ page.num_cells
set_value("root.header.sqlite_version_number", 0x002e8a11) # u4 @ 0x60
# page = set_value("root.header.root_page", root.BtreePage()) # old
page_number = 1
root.pages = []
# page = set_value("root.header.root_page", root.BtreePage(page_number))
page = root.BtreePage(page_number)

# try to fix root._write
# https://github.com/kaitai-io/kaitai_struct/issues/1245
page.cell_content_area__to_write = False

root.pages.append(page)
page.database_header = root.header
page._root = root
check("root")
# FIXME Check failed: root_page, expected: <kaitaistruct_sqlite3.Sqlite3 object at 0x7fc4d624f620>, actual: None
page.page_type = 0x0d # cell_table_leaf # u1 @ 0x64
page.first_freeblock = 0 # u2 @ 0x65
page.num_cells = 1 # u2 @ 0x67
# TODO seek to page.ofs_cells and write cells
# page.ofs_cells = 0x0fcc # u2
page.ofs_cell_content_area_raw = 0x0fcc # u2 @ 0x69
page.num_frag_free_bytes = 0 # u1 @ 0x6b
# page.right_ptr = 0 # only for (page_type == 2 or page_type == 5) # u4
# print("dir root:", dir(root))
page.cell_pointers = [] # 0x6c

cell_ptr = root.CellPointer()
cell_ptr.ofs_content = 0x0fcc # u2 @ 0x6c
cell_ptr._parent = page
cell_ptr._root = root
page.cell_pointers.append(cell_ptr)

if 0:

  # cell = root.CellTableLeaf() # old
  cell = root.TableLeafCell()
  cell._root = root

  # no!
  # TODO write cell to cell_ptr.ofs_content
  ############### page.cell_pointers.append(cell)

  root._io.seek(cell_ptr.ofs_content)
  root._io.write_bytes(b"\xbe\xef") # beef

  """
    table_leaf_cell:
      doc-ref: 'https://www.sqlite.org/fileformat2.html#b_tree_pages'
      seq:
        - id: payload_size
          type: vlq_base128_be
          doc: |
            total number of bytes of payload,
            including any overflow
        - id: row_id
          type: vlq_base128_be
          doc: |
            integer key, a.k.a. "rowid"
        - id: payload
          type:
            switch-on: '(payload_size.value > _root.header.table_max_overflow_payload_size ? 1 : 0)'
            cases:
              0: record
              1: overflow_record(payload_size.value, _root.header.table_max_overflow_payload_size)
  """

  # NOTE cell.len_payload is derived from len(content_str)
  # cell.payload_size = vlq_base128_be.VlqBase128Be.from_bytes(b"\x0f") # 0x0f @ 0x69
  cell.payload_size = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(15)) # 0x0f @ 0x69
  cell.payload_size._read() # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
  print_value("cell.payload_size.value")

  # cell.row_id = vlq_base128_be.VlqBase128Be.from_bytes(b"\xcc\x00") # 0xcc00 @ 0x6a
  cell.row_id = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(9728)) # 0xcc00 @ 0x6a
  cell.row_id._read() # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
  print_value("cell.row_id.value")

  # FIXME move payload to page.ofs_cells = 0x0fc0

  record_offset = page.ofs_cell_content_area_raw # 0x0fcc
  root._io.write_bytes(b"\xbe\xef") # FIXME no effect?
  root._io.seek(record_offset) # FIXME no effect?
  root._io.write_bytes(b"\xbe\xef") # FIXME no effect?
  print_value("root._io.tell()")
  print_value("dir(root._io)")

  # payload = cell.payload = root.CellPayload() # old
  record = cell.payload = root.Record()
  # record = cell.payload = root.OverflowRecord(payload_size=12, overflow_payload_size_max=34) # ?

  # TODO what?
  record_header_size = 0 # ValueError: negative count
  record_header_size = 1 # kaitaistruct.ConsistencyError: Check failed: entries, expected: 0, actual: 0
  record_header_size = 2
  record_header_size = 3 # kaitaistruct.ConsistencyError: Check failed: entries, expected: 0, actual: 1
  record_header_size = 4 # kaitaistruct.ConsistencyError: Check failed: entries, expected: 0, actual: 2
  record_header_size = 2

  """
    record:
      doc-ref: 'https://sqlite.org/fileformat2.html#record_format'
      seq:
        - id: header_size
          type: vlq_base128_be
        - id: header
          type: record_header
          size: header_size.value - 1
        - id: values
          type: value(header.value_types[_index])
          repeat: expr
          repeat-expr: header.value_types.size
    record_header:
      seq:
        - id: value_types
          type: serial_type
          repeat: eos
  """

  record.header_size = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(record_header_size))
  record.header_size._read() # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
  print_value("record.header_size.value") # 2

  record.header = root.RecordHeader()
  record.header.value_types = []

  record.values = []

  content_str = "asdf" # len: 4
  content_str = "CREATE TABLE test (id INTEGER)" # len: 30

  serial_type = root.SerialType()
  serial_type_raw_value = 12 + len(content_str) * 2 + 1 # odd = str, even = bytes
  serial_type.raw_value = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(serial_type_raw_value))
  serial_type.raw_value._read() # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
  print_value("serial_type.raw_value.value")
  record.header.value_types.append(serial_type)

  """
  record.record_header_size = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(record_header_size))
  record.record_header_size._read() # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
  print_value("record.record_header_size.value")
  """
  record.column_contents = []

  if 0:
    serials = record.column_serials = root.Serials()
    serials.entries = []

    entry = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(0))
    entry._read() # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
    serials.entries.append(entry)

    """
      serials:
        seq:
          - id: entries
            type: vlq_base128_be
            repeat: eos
    """

    serial = root.Serial()
    """
          is_string:
            value: 'code.value >= 13 and (code.value % 2 == 1)'
    """

    serial_code_value = 12 + len(content_str) * 2 + 1 # odd = str, even = bytes
    serial.code = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(serial_code_value))
    serial.code._read() # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
    print_value("serial.code.value")

    content = root.ColumnContent(ser=serial)
    # size: serial_type.len_content
    content.as_str = content_str
    record.column_contents.append(content)

  content = root.StringUtf8(len_value=len(content_str))
  content.value = content_str

  record.values.append(content)

print("root", dir(root)) # debug

print_keys("root")

# FIXME
"""
checking s: ok
writing s: error: requested invalid -1 amount of bytes
"""

check("root")
# Check failed: root_page, expected: <kaitaistruct_sqlite3.Sqlite3 object at 0x7fc4d624f620>, actual: None

write("root")
# 'Sqlite3' object has no attribute 'reserved_space'

# TODO seek to page.ofs_cells = 0x0fc0 and write cells
#  00000fb0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
# -00000fc0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
# +00000fc0: 0000 0000 0000 0000 0000 0000 3201 0617  ............2...
#                                          ^ 0x0fc0 + 12 = 0x0fcc = 4044



# try to fix root._write
# https://github.com/kaitai-io/kaitai_struct/issues/1245
root.pages__to_write = False

_io.seek(0) # fix: _write__seq does not seek before writing

if 1:
  # no. _write calls _fetch_instances which throws
  # https://github.com/kaitai-io/kaitai_struct/issues/1245
  print(f"writing root"); root._write(_io)
else:
  print(f"writing root"); root._write__seq(_io); root._io.write_back_child_streams()

print("writing done")

_io.seek(0)
_bytes = _io.read_bytes(num_pages * page_size)
# print(_bytes)

print("writing", bad_database_path)
with open(bad_database_path, "wb") as f:
    f.write(_bytes)

import sqlite3
con = sqlite3.connect(bad_database_path)
try: con.execute("select * from sqlite_schema")
except Exception as exc: print(exc)
# sqlite3.DatabaseError: file is not a database

import subprocess
import shlex
import os

if not os.path.exists(good_database_path):
  args = [
    "sqlite3",
    good_database_path,
    "create table test (id INTEGER)",
  ]
  print(">", shlex.join(args))
  subprocess.run(args)

# TODO rewrite diff in python
args = [
  "diff", "--color=always", "-u",
  "<(", "xxd", bad_database_path, ")", # red
  "<(", "xxd", good_database_path, ")", # green
  # "|", "head", "-n20",
  "|", "head", "-n100",
]
args = ["bash", "-c", " ".join(args)]
print(">", shlex.join(args))
subprocess.run(args)
