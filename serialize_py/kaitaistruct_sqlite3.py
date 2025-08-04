# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import ReadWriteKaitaiStruct, KaitaiStream, BytesIO
from enum import IntEnum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

import vlq_base128_be
class Sqlite3(ReadWriteKaitaiStruct):
    """SQLite3 is a popular serverless SQL engine, implemented as a library
    to be used within other applications. It keeps its databases as
    regular disk files.
    
    Every database file is segmented into pages. First page (starting at
    the very beginning) is special: it contains a file-global header
    which specifies some data relevant to proper parsing (i.e. format
    versions, size of page, etc). After the header, normal contents of
    the first page follow.
    
    Each page would be of some type (btree, ptrmap, lock_byte, or free),
    and generally, they would be reached via the links starting from the
    first page. The first page is always a btree page for the implicitly
    defined `sqlite_schema` table.
    
    This works well when parsing small database files. To parse large
    database files, see the documentation for /instances/pages.
    
    Further documentation:
    
    - https://www.sqlite.org/arch.html
    - https://medium.com/the-polyglot-programmer/what-would-sqlite-look-like-if-written-in-rust-part-3-edd2eefda473
    - https://cstack.github.io/db_tutorial/parts/part7.html
    
    Original sources:
    
    - https://github.com/sqlite/sqlite/blob/master/src/btree.h
    - https://github.com/sqlite/sqlite/blob/master/src/btree.c
    
    .. seealso::
       Source - https://www.sqlite.org/fileformat2.html
    """

    class FormatVersion(IntEnum):
        legacy = 1
        wal = 2

    class BtreePageType(IntEnum):
        index_interior_page = 2
        table_interior_page = 5
        index_leaf_page = 10
        table_leaf_page = 13

    class PtrmapPageType(IntEnum):
        root_page = 1
        free_page = 2
        overflow1 = 3
        overflow2 = 4
        btree = 5

    class Serial(IntEnum):
        nil = 0
        two_comp_8 = 1
        two_comp_16 = 2
        two_comp_24 = 3
        two_comp_32 = 4
        two_comp_48 = 5
        two_comp_64 = 6
        ieee754_64 = 7
        integer_0 = 8
        integer_1 = 9
        internal_1 = 10
        internal_2 = 11
        blob = 12
        string_utf8 = 13
        string_utf16_le = 14
        string_utf16_be = 15
    def __init__(self, _io=None, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._should_write_pages = False
        self.pages__to_write = True

    def _read(self):
        self.header = Sqlite3.DatabaseHeader(self._io, self, self._root)
        self.header._read()


    def _fetch_instances(self):
        pass
        self.header._fetch_instances()
        _ = self.pages
        for i in range(len(self._m_pages)):
            pass
            _on = (0 if (i == self.header.idx_lock_byte_page) else (1 if  (((i >= self.header.idx_first_ptrmap_page)) and ((i <= self.header.idx_last_ptrmap_page)))  else 2))
            if _on == 0:
                pass
                self.pages[i]._fetch_instances()
            elif _on == 1:
                pass
                self.pages[i]._fetch_instances()
            elif _on == 2:
                pass
                self.pages[i]._fetch_instances()
            else:
                pass



    def _write__seq(self, io=None):
        super(Sqlite3, self)._write__seq(io)
        self._should_write_pages = self.pages__to_write
        self.header._write__seq(self._io)


    def _check(self):
        pass
        if self.header._root != self._root:
            raise kaitaistruct.ConsistencyError(u"header", self.header._root, self._root)
        if self.header._parent != self:
            raise kaitaistruct.ConsistencyError(u"header", self.header._parent, self)

    class LockBytePage(ReadWriteKaitaiStruct):
        """The lock-byte page is the single page of the database file that contains the bytes at offsets between
        1073741824 and 1073742335, inclusive. A database file that is less than or equal to 1073741824 bytes
        in size contains no lock-byte page. A database file larger than 1073741824 contains exactly one
        lock-byte page.
        The lock-byte page is set aside for use by the operating-system specific VFS implementation in implementing
        the database file locking primitives. SQLite does not use the lock-byte page.
        """
        def __init__(self, page_number, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self.page_number = page_number

        def _read(self):
            pass


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Sqlite3.LockBytePage, self)._write__seq(io)


        def _check(self):
            pass


    class FreelistTrunkPagePointer(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self._should_write_page = False
            self.page__to_write = True

        def _read(self):
            self.page_number = self._io.read_u4be()


        def _fetch_instances(self):
            pass
            if (self.page_number != 0):
                pass
                _ = self.page
                self.page._fetch_instances()



        def _write__seq(self, io=None):
            super(Sqlite3.FreelistTrunkPagePointer, self)._write__seq(io)
            self._should_write_page = self.page__to_write
            self._io.write_u4be(self.page_number)


        def _check(self):
            pass

        @property
        def page(self):
            if self._should_write_page:
                self._write_page()
            if hasattr(self, '_m_page'):
                return self._m_page

            if (self.page_number != 0):
                pass
                io = self._root._io
                _pos = io.pos()
                io.seek(((self.page_number - 1) * self._root.header.page_size))
                self._raw__m_page = io.read_bytes(self._root.header.page_size)
                _io__raw__m_page = KaitaiStream(BytesIO(self._raw__m_page))
                self._m_page = Sqlite3.FreelistTrunkPage(_io__raw__m_page, self, self._root)
                self._m_page._read()
                io.seek(_pos)

            return getattr(self, '_m_page', None)

        @page.setter
        def page(self, v):
            self._m_page = v

        def _write_page(self):
            self._should_write_page = False
            if (self.page_number != 0):
                pass
                io = self._root._io
                _pos = io.pos()
                io.seek(((self.page_number - 1) * self._root.header.page_size))
                _io__raw__m_page = KaitaiStream(BytesIO(bytearray(self._root.header.page_size)))
                io.add_child_stream(_io__raw__m_page)
                _pos2 = io.pos()
                io.seek(io.pos() + (self._root.header.page_size))
                def handler(parent, _io__raw__m_page=_io__raw__m_page):
                    self._raw__m_page = _io__raw__m_page.to_byte_array()
                    if (len(self._raw__m_page) != self._root.header.page_size):
                        raise kaitaistruct.ConsistencyError(u"raw(page)", len(self._raw__m_page), self._root.header.page_size)
                    parent.write_bytes(self._raw__m_page)
                _io__raw__m_page.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
                self.page._write__seq(_io__raw__m_page)
                io.seek(_pos)



        def _check_page(self):
            pass
            if (self.page_number != 0):
                pass
                if self.page._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"page", self.page._root, self._root)
                if self.page._parent != self:
                    raise kaitaistruct.ConsistencyError(u"page", self.page._parent, self)



    class BtreePage(ReadWriteKaitaiStruct):
        def __init__(self, page_number, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self.page_number = page_number
            self._should_write_reserved_space = False
            self.reserved_space__to_write = True

        def _read(self):
            self.page_type = KaitaiStream.resolve_enum(Sqlite3.BtreePageType, self._io.read_u1())
            self.first_freeblock = self._io.read_u2be()
            self.num_cells = self._io.read_u2be()
            self.ofs_cell_content_area_raw = self._io.read_u2be()
            self.num_frag_free_bytes = self._io.read_u1()
            if  (((self.page_type == Sqlite3.BtreePageType.index_interior_page)) or ((self.page_type == Sqlite3.BtreePageType.table_interior_page))) :
                pass
                self.right_ptr = Sqlite3.BtreePagePointer(self._io, self, self._root)
                self.right_ptr._read()

            self.cell_pointers = []
            for i in range(self.num_cells):
                _t_cell_pointers = Sqlite3.CellPointer(self._io, self, self._root)
                _t_cell_pointers._read()
                self.cell_pointers.append(_t_cell_pointers)



        def _fetch_instances(self):
            pass
            if  (((self.page_type == Sqlite3.BtreePageType.index_interior_page)) or ((self.page_type == Sqlite3.BtreePageType.table_interior_page))) :
                pass
                self.right_ptr._fetch_instances()

            for i in range(len(self.cell_pointers)):
                pass
                self.cell_pointers[i]._fetch_instances()

            if (self._root.header.page_reserved_space_size != 0):
                pass
                _ = self.reserved_space



        def _write__seq(self, io=None):
            super(Sqlite3.BtreePage, self)._write__seq(io)
            self._should_write_reserved_space = self.reserved_space__to_write
            self._io.write_u1(int(self.page_type))
            self._io.write_u2be(self.first_freeblock)
            self._io.write_u2be(self.num_cells)
            self._io.write_u2be(self.ofs_cell_content_area_raw)
            self._io.write_u1(self.num_frag_free_bytes)
            if  (((self.page_type == Sqlite3.BtreePageType.index_interior_page)) or ((self.page_type == Sqlite3.BtreePageType.table_interior_page))) :
                pass
                self.right_ptr._write__seq(self._io)

            for i in range(len(self.cell_pointers)):
                pass
                self.cell_pointers[i]._write__seq(self._io)



        def _check(self):
            pass
            if  (((self.page_type == Sqlite3.BtreePageType.index_interior_page)) or ((self.page_type == Sqlite3.BtreePageType.table_interior_page))) :
                pass
                if self.right_ptr._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"right_ptr", self.right_ptr._root, self._root)
                if self.right_ptr._parent != self:
                    raise kaitaistruct.ConsistencyError(u"right_ptr", self.right_ptr._parent, self)

            if (len(self.cell_pointers) != self.num_cells):
                raise kaitaistruct.ConsistencyError(u"cell_pointers", len(self.cell_pointers), self.num_cells)
            for i in range(len(self.cell_pointers)):
                pass
                if self.cell_pointers[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"cell_pointers", self.cell_pointers[i]._root, self._root)
                if self.cell_pointers[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"cell_pointers", self.cell_pointers[i]._parent, self)


        @property
        def ofs_cell_content_area(self):
            if hasattr(self, '_m_ofs_cell_content_area'):
                return self._m_ofs_cell_content_area

            self._m_ofs_cell_content_area = (65536 if (self.ofs_cell_content_area_raw == 0) else self.ofs_cell_content_area_raw)
            return getattr(self, '_m_ofs_cell_content_area', None)

        def _invalidate_ofs_cell_content_area(self):
            del self._m_ofs_cell_content_area
        @property
        def reserved_space(self):
            if self._should_write_reserved_space:
                self._write_reserved_space()
            if hasattr(self, '_m_reserved_space'):
                return self._m_reserved_space

            if (self._root.header.page_reserved_space_size != 0):
                pass
                _pos = self._io.pos()
                self._io.seek((self._root.header.page_size - self._root.header.page_reserved_space_size))
                self._m_reserved_space = self._io.read_bytes_full()
                self._io.seek(_pos)

            return getattr(self, '_m_reserved_space', None)

        @reserved_space.setter
        def reserved_space(self, v):
            self._m_reserved_space = v

        def _write_reserved_space(self):
            self._should_write_reserved_space = False
            if (self._root.header.page_reserved_space_size != 0):
                pass
                _pos = self._io.pos()
                self._io.seek((self._root.header.page_size - self._root.header.page_reserved_space_size))
                self._io.write_bytes(self.reserved_space)
                if not self._io.is_eof():
                    raise kaitaistruct.ConsistencyError(u"reserved_space", self._io.size() - self._io.pos(), 0)
                self._io.seek(_pos)



        def _check_reserved_space(self):
            pass
            if (self._root.header.page_reserved_space_size != 0):
                pass



    class BtreePagePointer(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self._should_write_page = False
            self.page__to_write = True

        def _read(self):
            self.page_number = self._io.read_u4be()


        def _fetch_instances(self):
            pass
            if (self.page_number != 0):
                pass
                _ = self.page
                self.page._fetch_instances()



        def _write__seq(self, io=None):
            super(Sqlite3.BtreePagePointer, self)._write__seq(io)
            self._should_write_page = self.page__to_write
            self._io.write_u4be(self.page_number)


        def _check(self):
            pass

        @property
        def page(self):
            if self._should_write_page:
                self._write_page()
            if hasattr(self, '_m_page'):
                return self._m_page

            if (self.page_number != 0):
                pass
                io = self._root._io
                _pos = io.pos()
                io.seek(((self.page_number - 1) * self._root.header.page_size))
                self._raw__m_page = io.read_bytes(self._root.header.page_size)
                _io__raw__m_page = KaitaiStream(BytesIO(self._raw__m_page))
                self._m_page = Sqlite3.BtreePage(self.page_number, _io__raw__m_page, self, self._root)
                self._m_page._read()
                io.seek(_pos)

            return getattr(self, '_m_page', None)

        @page.setter
        def page(self, v):
            self._m_page = v

        def _write_page(self):
            self._should_write_page = False
            if (self.page_number != 0):
                pass
                io = self._root._io
                _pos = io.pos()
                io.seek(((self.page_number - 1) * self._root.header.page_size))
                _io__raw__m_page = KaitaiStream(BytesIO(bytearray(self._root.header.page_size)))
                io.add_child_stream(_io__raw__m_page)
                _pos2 = io.pos()
                io.seek(io.pos() + (self._root.header.page_size))
                def handler(parent, _io__raw__m_page=_io__raw__m_page):
                    self._raw__m_page = _io__raw__m_page.to_byte_array()
                    if (len(self._raw__m_page) != self._root.header.page_size):
                        raise kaitaistruct.ConsistencyError(u"raw(page)", len(self._raw__m_page), self._root.header.page_size)
                    parent.write_bytes(self._raw__m_page)
                _io__raw__m_page.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
                self.page._write__seq(_io__raw__m_page)
                io.seek(_pos)



        def _check_page(self):
            pass
            if (self.page_number != 0):
                pass
                if self.page._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"page", self.page._root, self._root)
                if self.page._parent != self:
                    raise kaitaistruct.ConsistencyError(u"page", self.page._parent, self)
                if (self.page.page_number != self.page_number):
                    raise kaitaistruct.ConsistencyError(u"page", self.page.page_number, self.page_number)



    class OverflowPage(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.next_page_number = Sqlite3.OverflowPagePointer(self._io, self, self._root)
            self.next_page_number._read()
            self.content = self._io.read_bytes((self._root.header.page_size - 4))


        def _fetch_instances(self):
            pass
            self.next_page_number._fetch_instances()


        def _write__seq(self, io=None):
            super(Sqlite3.OverflowPage, self)._write__seq(io)
            self.next_page_number._write__seq(self._io)
            self._io.write_bytes(self.content)


        def _check(self):
            pass
            if self.next_page_number._root != self._root:
                raise kaitaistruct.ConsistencyError(u"next_page_number", self.next_page_number._root, self._root)
            if self.next_page_number._parent != self:
                raise kaitaistruct.ConsistencyError(u"next_page_number", self.next_page_number._parent, self)
            if (len(self.content) != (self._root.header.page_size - 4)):
                raise kaitaistruct.ConsistencyError(u"content", len(self.content), (self._root.header.page_size - 4))


    class Int0(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            pass


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Sqlite3.Int0, self)._write__seq(io)


        def _check(self):
            pass


    class OverflowRecord(ReadWriteKaitaiStruct):
        def __init__(self, payload_size, overflow_payload_size_max, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self.payload_size = payload_size
            self.overflow_payload_size_max = overflow_payload_size_max

        def _read(self):
            self.inline_payload = self._io.read_bytes((self.inline_payload_size if (self.inline_payload_size <= self.overflow_payload_size_max) else self._root.header.overflow_min_payload_size))
            self.overflow_page_number = Sqlite3.OverflowPagePointer(self._io, self, self._root)
            self.overflow_page_number._read()


        def _fetch_instances(self):
            pass
            self.overflow_page_number._fetch_instances()


        def _write__seq(self, io=None):
            super(Sqlite3.OverflowRecord, self)._write__seq(io)
            self._io.write_bytes(self.inline_payload)
            self.overflow_page_number._write__seq(self._io)


        def _check(self):
            pass
            if (len(self.inline_payload) != (self.inline_payload_size if (self.inline_payload_size <= self.overflow_payload_size_max) else self._root.header.overflow_min_payload_size)):
                raise kaitaistruct.ConsistencyError(u"inline_payload", len(self.inline_payload), (self.inline_payload_size if (self.inline_payload_size <= self.overflow_payload_size_max) else self._root.header.overflow_min_payload_size))
            if self.overflow_page_number._root != self._root:
                raise kaitaistruct.ConsistencyError(u"overflow_page_number", self.overflow_page_number._root, self._root)
            if self.overflow_page_number._parent != self:
                raise kaitaistruct.ConsistencyError(u"overflow_page_number", self.overflow_page_number._parent, self)

        @property
        def inline_payload_size(self):
            if hasattr(self, '_m_inline_payload_size'):
                return self._m_inline_payload_size

            self._m_inline_payload_size = (self._root.header.overflow_min_payload_size + ((self.payload_size - self._root.header.overflow_min_payload_size) % (self._root.header.usable_size - 4)))
            return getattr(self, '_m_inline_payload_size', None)

        def _invalidate_inline_payload_size(self):
            del self._m_inline_payload_size

    class FreelistTrunkPage(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.next_page = Sqlite3.FreelistTrunkPagePointer(self._io, self, self._root)
            self.next_page._read()
            self.num_free_pages = self._io.read_u4be()
            self.free_pages = []
            for i in range(self.num_free_pages):
                self.free_pages.append(self._io.read_u4be())



        def _fetch_instances(self):
            pass
            self.next_page._fetch_instances()
            for i in range(len(self.free_pages)):
                pass



        def _write__seq(self, io=None):
            super(Sqlite3.FreelistTrunkPage, self)._write__seq(io)
            self.next_page._write__seq(self._io)
            self._io.write_u4be(self.num_free_pages)
            for i in range(len(self.free_pages)):
                pass
                self._io.write_u4be(self.free_pages[i])



        def _check(self):
            pass
            if self.next_page._root != self._root:
                raise kaitaistruct.ConsistencyError(u"next_page", self.next_page._root, self._root)
            if self.next_page._parent != self:
                raise kaitaistruct.ConsistencyError(u"next_page", self.next_page._parent, self)
            if (len(self.free_pages) != self.num_free_pages):
                raise kaitaistruct.ConsistencyError(u"free_pages", len(self.free_pages), self.num_free_pages)
            for i in range(len(self.free_pages)):
                pass



    class StringUtf16Be(ReadWriteKaitaiStruct):
        def __init__(self, len_value, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self.len_value = len_value

        def _read(self):
            self.value = (self._io.read_bytes(self.len_value)).decode("UTF-16BE")


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Sqlite3.StringUtf16Be, self)._write__seq(io)
            self._io.write_bytes((self.value).encode(u"UTF-16BE"))


        def _check(self):
            pass
            if (len((self.value).encode(u"UTF-16BE")) != self.len_value):
                raise kaitaistruct.ConsistencyError(u"value", len((self.value).encode(u"UTF-16BE")), self.len_value)


    class NullValue(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            pass


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Sqlite3.NullValue, self)._write__seq(io)


        def _check(self):
            pass


    class Int1(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            pass


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Sqlite3.Int1, self)._write__seq(io)


        def _check(self):
            pass


    class OverflowPagePointer(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self._should_write_page = False
            self.page__to_write = True

        def _read(self):
            self.page_number = self._io.read_u4be()


        def _fetch_instances(self):
            pass
            if (self.page_number != 0):
                pass
                _ = self.page
                self.page._fetch_instances()



        def _write__seq(self, io=None):
            super(Sqlite3.OverflowPagePointer, self)._write__seq(io)
            self._should_write_page = self.page__to_write
            self._io.write_u4be(self.page_number)


        def _check(self):
            pass

        @property
        def page(self):
            if self._should_write_page:
                self._write_page()
            if hasattr(self, '_m_page'):
                return self._m_page

            if (self.page_number != 0):
                pass
                io = self._root._io
                _pos = io.pos()
                io.seek(((self.page_number - 1) * self._root.header.page_size))
                self._raw__m_page = io.read_bytes(self._root.header.page_size)
                _io__raw__m_page = KaitaiStream(BytesIO(self._raw__m_page))
                self._m_page = Sqlite3.OverflowPage(_io__raw__m_page, self, self._root)
                self._m_page._read()
                io.seek(_pos)

            return getattr(self, '_m_page', None)

        @page.setter
        def page(self, v):
            self._m_page = v

        def _write_page(self):
            self._should_write_page = False
            if (self.page_number != 0):
                pass
                io = self._root._io
                _pos = io.pos()
                io.seek(((self.page_number - 1) * self._root.header.page_size))
                _io__raw__m_page = KaitaiStream(BytesIO(bytearray(self._root.header.page_size)))
                io.add_child_stream(_io__raw__m_page)
                _pos2 = io.pos()
                io.seek(io.pos() + (self._root.header.page_size))
                def handler(parent, _io__raw__m_page=_io__raw__m_page):
                    self._raw__m_page = _io__raw__m_page.to_byte_array()
                    if (len(self._raw__m_page) != self._root.header.page_size):
                        raise kaitaistruct.ConsistencyError(u"raw(page)", len(self._raw__m_page), self._root.header.page_size)
                    parent.write_bytes(self._raw__m_page)
                _io__raw__m_page.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
                self.page._write__seq(_io__raw__m_page)
                io.seek(_pos)



        def _check_page(self):
            pass
            if (self.page_number != 0):
                pass
                if self.page._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"page", self.page._root, self._root)
                if self.page._parent != self:
                    raise kaitaistruct.ConsistencyError(u"page", self.page._parent, self)



    class SerialType(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.raw_value = vlq_base128_be.VlqBase128Be(self._io)
            self.raw_value._read()


        def _fetch_instances(self):
            pass
            self.raw_value._fetch_instances()


        def _write__seq(self, io=None):
            super(Sqlite3.SerialType, self)._write__seq(io)
            self.raw_value._write__seq(self._io)


        def _check(self):
            pass

        @property
        def type(self):
            if hasattr(self, '_m_type'):
                return self._m_type

            self._m_type = KaitaiStream.resolve_enum(Sqlite3.Serial, ((12 if ((self.raw_value.value % 2) == 0) else ((13 + self._root.header.text_encoding) - 1)) if (self.raw_value.value >= 12) else self.raw_value.value))
            return getattr(self, '_m_type', None)

        def _invalidate_type(self):
            del self._m_type
        @property
        def len_blob_string(self):
            if hasattr(self, '_m_len_blob_string'):
                return self._m_len_blob_string

            if (self.raw_value.value >= 12):
                pass
                self._m_len_blob_string = ((self.raw_value.value - 12) // 2 if ((self.raw_value.value % 2) == 0) else (self.raw_value.value - 13) // 2)

            return getattr(self, '_m_len_blob_string', None)

        def _invalidate_len_blob_string(self):
            del self._m_len_blob_string

    class IndexLeafCell(ReadWriteKaitaiStruct):
        """
        .. seealso::
           Source - https://www.sqlite.org/fileformat2.html#b_tree_pages
        """
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.payload_size = vlq_base128_be.VlqBase128Be(self._io)
            self.payload_size._read()
            _on = (1 if (self.payload_size.value > self._root.header.index_max_overflow_payload_size) else 0)
            if _on == 0:
                pass
                self.payload = Sqlite3.Record(self._io, self, self._root)
                self.payload._read()
            elif _on == 1:
                pass
                self.payload = Sqlite3.OverflowRecord(self.payload_size.value, self._root.header.index_max_overflow_payload_size, self._io, self, self._root)
                self.payload._read()


        def _fetch_instances(self):
            pass
            self.payload_size._fetch_instances()
            _on = (1 if (self.payload_size.value > self._root.header.index_max_overflow_payload_size) else 0)
            if _on == 0:
                pass
                self.payload._fetch_instances()
            elif _on == 1:
                pass
                self.payload._fetch_instances()


        def _write__seq(self, io=None):
            super(Sqlite3.IndexLeafCell, self)._write__seq(io)
            self.payload_size._write__seq(self._io)
            _on = (1 if (self.payload_size.value > self._root.header.index_max_overflow_payload_size) else 0)
            if _on == 0:
                pass
                self.payload._write__seq(self._io)
            elif _on == 1:
                pass
                self.payload._write__seq(self._io)


        def _check(self):
            pass
            _on = (1 if (self.payload_size.value > self._root.header.index_max_overflow_payload_size) else 0)
            if _on == 0:
                pass
                if self.payload._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload._root, self._root)
                if self.payload._parent != self:
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload._parent, self)
            elif _on == 1:
                pass
                if self.payload._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload._root, self._root)
                if self.payload._parent != self:
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload._parent, self)
                if (self.payload.payload_size != self.payload_size.value):
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload.payload_size, self.payload_size.value)
                if (self.payload.overflow_payload_size_max != self._root.header.index_max_overflow_payload_size):
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload.overflow_payload_size_max, self._root.header.index_max_overflow_payload_size)


    class PointerMapPage(ReadWriteKaitaiStruct):
        """A ptrmap page contains back-links from child to parent.
        See also: /types/pointer_map_entry.
        
        Pointer map pages (or "ptrmap pages")
        are extra pages inserted into the database
        to make the operation of auto_vacuum and
        incremental_vacuum modes more efficient.
        
        Ptrmap pages must exist in any database file
        which has a non-zero largest root b-tree page value
        in db.header.largest_root_page.
        
        If db.header.largest_root_page is zero,
        then the database must not contain ptrmap pages.
        
        The first ptrmap page (on page 2)
        will contain back pointer information
        for pages 3 through J+2, inclusive.
        
        The second pointer map page will be on page J+3
        and that ptrmap page will provide back pointer information
        for pages J+4 through 2*J+3 inclusive.
        
        And so forth for the entire database file.
        
        ```py
        page_size = 512
        page_reserved_space_size = 0
        U = usable_size = page_size - page_reserved_space_size # 512
        J = pointer_map_page_entries_max = usable_size // 5 # 102
        
        # pointer map 1
        X = 1
        N = pointer_map_page_number_raw = ((X - 1) * J) + 1 + X # 2
        A = first_linked_page_number = N + 1 # 3
        Z = last_linked_page_number = N + J # 104 = J + 2
        
        # pointer map 2
        X = 2
        N = pointer_map_page_number = ((X - 1) * J) + 1 + X # 105 = J + 3
        A = first_linked_page_number = N + 1 # 106 = J + 4
        Z = last_linked_page_number = N + J # 207 = (2 * J) + 3
        
        # pointer map 3
        X = 3
        N = pointer_map_page_number = ((X - 1) * J) + 1 + X # 208
        A = first_linked_page_number = N + 1 # 209
        Z = last_linked_page_number = N + J # 310
        
        # pointer map 4
        X = 4
        N = pointer_map_page_number = ((X - 1) * J) + 1 + X # 311
        A = first_linked_page_number = N + 1 # 312
        Z = last_linked_page_number = N + J # 413
        ```
        
        actual pointer_map_page_number:
        
        ```py
        NR = pointer_map_page_number_raw = ((X - 1) * J) + 1 + X # 2
        N = pointer_map_page_number = (
          pointer_map_page_number_raw
          if (pointer_map_page_number_raw != lock_byte_page_number)
          else (pointer_map_page_number_raw + 1)
        )
        ```
        
        .. seealso::
           Source - https://www.sqlite.org/fileformat2.html#pointer_map_or_ptrmap_pages
        """
        def __init__(self, pointer_map_page_number, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self.pointer_map_page_number = pointer_map_page_number

        def _read(self):
            self.entries = []
            for i in range(self.num_entries):
                _t_entries = Sqlite3.PointerMapEntry(self._io, self, self._root)
                _t_entries._read()
                self.entries.append(_t_entries)



        def _fetch_instances(self):
            pass
            for i in range(len(self.entries)):
                pass
                self.entries[i]._fetch_instances()



        def _write__seq(self, io=None):
            super(Sqlite3.PointerMapPage, self)._write__seq(io)
            for i in range(len(self.entries)):
                pass
                self.entries[i]._write__seq(self._io)



        def _check(self):
            pass
            if (len(self.entries) != self.num_entries):
                raise kaitaistruct.ConsistencyError(u"entries", len(self.entries), self.num_entries)
            for i in range(len(self.entries)):
                pass
                if self.entries[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"entries", self.entries[i]._root, self._root)
                if self.entries[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"entries", self.entries[i]._parent, self)


        @property
        def last_linked_page_number(self):
            if hasattr(self, '_m_last_linked_page_number'):
                return self._m_last_linked_page_number

            self._m_last_linked_page_number = (self.last_linked_page_number_max if (self.last_linked_page_number_max <= self._root.header.num_pages) else self._root.header.num_pages)
            return getattr(self, '_m_last_linked_page_number', None)

        def _invalidate_last_linked_page_number(self):
            del self._m_last_linked_page_number
        @property
        def last_linked_page_number_max(self):
            if hasattr(self, '_m_last_linked_page_number_max'):
                return self._m_last_linked_page_number_max

            self._m_last_linked_page_number_max = (self.pointer_map_page_number + self.pointer_map_page_entries_max)
            return getattr(self, '_m_last_linked_page_number_max', None)

        def _invalidate_last_linked_page_number_max(self):
            del self._m_last_linked_page_number_max
        @property
        def first_linked_page_number(self):
            if hasattr(self, '_m_first_linked_page_number'):
                return self._m_first_linked_page_number

            self._m_first_linked_page_number = (self.pointer_map_page_number + 1)
            return getattr(self, '_m_first_linked_page_number', None)

        def _invalidate_first_linked_page_number(self):
            del self._m_first_linked_page_number
        @property
        def num_entries(self):
            if hasattr(self, '_m_num_entries'):
                return self._m_num_entries

            self._m_num_entries = ((self.last_linked_page_number - self.first_linked_page_number) + 1)
            return getattr(self, '_m_num_entries', None)

        def _invalidate_num_entries(self):
            del self._m_num_entries
        @property
        def pointer_map_page_entries_max(self):
            if hasattr(self, '_m_pointer_map_page_entries_max'):
                return self._m_pointer_map_page_entries_max

            self._m_pointer_map_page_entries_max = self._root.header.usable_size // 5
            return getattr(self, '_m_pointer_map_page_entries_max', None)

        def _invalidate_pointer_map_page_entries_max(self):
            del self._m_pointer_map_page_entries_max

    class IndexInteriorCell(ReadWriteKaitaiStruct):
        """
        .. seealso::
           Source - https://www.sqlite.org/fileformat2.html#b_tree_pages
        """
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.left_child_page = Sqlite3.BtreePagePointer(self._io, self, self._root)
            self.left_child_page._read()
            self.payload_size = vlq_base128_be.VlqBase128Be(self._io)
            self.payload_size._read()
            _on = (1 if (self.payload_size.value > self._root.header.index_max_overflow_payload_size) else 0)
            if _on == 0:
                pass
                self.payload = Sqlite3.Record(self._io, self, self._root)
                self.payload._read()
            elif _on == 1:
                pass
                self.payload = Sqlite3.OverflowRecord(self.payload_size.value, self._root.header.index_max_overflow_payload_size, self._io, self, self._root)
                self.payload._read()


        def _fetch_instances(self):
            pass
            self.left_child_page._fetch_instances()
            self.payload_size._fetch_instances()
            _on = (1 if (self.payload_size.value > self._root.header.index_max_overflow_payload_size) else 0)
            if _on == 0:
                pass
                self.payload._fetch_instances()
            elif _on == 1:
                pass
                self.payload._fetch_instances()


        def _write__seq(self, io=None):
            super(Sqlite3.IndexInteriorCell, self)._write__seq(io)
            self.left_child_page._write__seq(self._io)
            self.payload_size._write__seq(self._io)
            _on = (1 if (self.payload_size.value > self._root.header.index_max_overflow_payload_size) else 0)
            if _on == 0:
                pass
                self.payload._write__seq(self._io)
            elif _on == 1:
                pass
                self.payload._write__seq(self._io)


        def _check(self):
            pass
            if self.left_child_page._root != self._root:
                raise kaitaistruct.ConsistencyError(u"left_child_page", self.left_child_page._root, self._root)
            if self.left_child_page._parent != self:
                raise kaitaistruct.ConsistencyError(u"left_child_page", self.left_child_page._parent, self)
            _on = (1 if (self.payload_size.value > self._root.header.index_max_overflow_payload_size) else 0)
            if _on == 0:
                pass
                if self.payload._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload._root, self._root)
                if self.payload._parent != self:
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload._parent, self)
            elif _on == 1:
                pass
                if self.payload._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload._root, self._root)
                if self.payload._parent != self:
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload._parent, self)
                if (self.payload.payload_size != self.payload_size.value):
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload.payload_size, self.payload_size.value)
                if (self.payload.overflow_payload_size_max != self._root.header.index_max_overflow_payload_size):
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload.overflow_payload_size_max, self._root.header.index_max_overflow_payload_size)


    class PointerMapEntry(ReadWriteKaitaiStruct):
        """
        .. seealso::
           Source - https://www.sqlite.org/fileformat2.html#pointer_map_or_ptrmap_pages
        """
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.type = KaitaiStream.resolve_enum(Sqlite3.PtrmapPageType, self._io.read_u1())
            self.page_number = self._io.read_u4be()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Sqlite3.PointerMapEntry, self)._write__seq(io)
            self._io.write_u1(int(self.type))
            self._io.write_u4be(self.page_number)


        def _check(self):
            pass


    class StringUtf8(ReadWriteKaitaiStruct):
        def __init__(self, len_value, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self.len_value = len_value

        def _read(self):
            self.value = (self._io.read_bytes(self.len_value)).decode("UTF-8")


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Sqlite3.StringUtf8, self)._write__seq(io)
            self._io.write_bytes((self.value).encode(u"UTF-8"))


        def _check(self):
            pass
            if (len((self.value).encode(u"UTF-8")) != self.len_value):
                raise kaitaistruct.ConsistencyError(u"value", len((self.value).encode(u"UTF-8")), self.len_value)


    class RecordHeader(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.value_types = []
            i = 0
            while not self._io.is_eof():
                _t_value_types = Sqlite3.SerialType(self._io, self, self._root)
                _t_value_types._read()
                self.value_types.append(_t_value_types)
                i += 1



        def _fetch_instances(self):
            pass
            for i in range(len(self.value_types)):
                pass
                self.value_types[i]._fetch_instances()



        def _write__seq(self, io=None):
            super(Sqlite3.RecordHeader, self)._write__seq(io)
            for i in range(len(self.value_types)):
                pass
                if self._io.is_eof():
                    raise kaitaistruct.ConsistencyError(u"value_types", self._io.size() - self._io.pos(), 0)
                self.value_types[i]._write__seq(self._io)

            if not self._io.is_eof():
                raise kaitaistruct.ConsistencyError(u"value_types", self._io.size() - self._io.pos(), 0)


        def _check(self):
            pass
            for i in range(len(self.value_types)):
                pass
                if self.value_types[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"value_types", self.value_types[i]._root, self._root)
                if self.value_types[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"value_types", self.value_types[i]._parent, self)



    class StringUtf16Le(ReadWriteKaitaiStruct):
        def __init__(self, len_value, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self.len_value = len_value

        def _read(self):
            self.value = (self._io.read_bytes(self.len_value)).decode("UTF-16LE")


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Sqlite3.StringUtf16Le, self)._write__seq(io)
            self._io.write_bytes((self.value).encode(u"UTF-16LE"))


        def _check(self):
            pass
            if (len((self.value).encode(u"UTF-16LE")) != self.len_value):
                raise kaitaistruct.ConsistencyError(u"value", len((self.value).encode(u"UTF-16LE")), self.len_value)


    class TableInteriorCell(ReadWriteKaitaiStruct):
        """
        .. seealso::
           Source - https://www.sqlite.org/fileformat2.html#b_tree_pages
        """
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.left_child_page = Sqlite3.BtreePagePointer(self._io, self, self._root)
            self.left_child_page._read()
            self.row_id = vlq_base128_be.VlqBase128Be(self._io)
            self.row_id._read()


        def _fetch_instances(self):
            pass
            self.left_child_page._fetch_instances()
            self.row_id._fetch_instances()


        def _write__seq(self, io=None):
            super(Sqlite3.TableInteriorCell, self)._write__seq(io)
            self.left_child_page._write__seq(self._io)
            self.row_id._write__seq(self._io)


        def _check(self):
            pass
            if self.left_child_page._root != self._root:
                raise kaitaistruct.ConsistencyError(u"left_child_page", self.left_child_page._root, self._root)
            if self.left_child_page._parent != self:
                raise kaitaistruct.ConsistencyError(u"left_child_page", self.left_child_page._parent, self)


    class DatabaseHeader(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.magic = self._io.read_bytes(16)
            if not (self.magic == b"\x53\x51\x4C\x69\x74\x65\x20\x66\x6F\x72\x6D\x61\x74\x20\x33\x00"):
                raise kaitaistruct.ValidationNotEqualError(b"\x53\x51\x4C\x69\x74\x65\x20\x66\x6F\x72\x6D\x61\x74\x20\x33\x00", self.magic, self._io, u"/types/database_header/seq/0")
            self.page_size_raw = self._io.read_u2be()
            self.write_version = KaitaiStream.resolve_enum(Sqlite3.FormatVersion, self._io.read_u1())
            self.read_version = KaitaiStream.resolve_enum(Sqlite3.FormatVersion, self._io.read_u1())
            self.page_reserved_space_size = self._io.read_u1()
            self.max_payload_fraction = self._io.read_u1()
            self.min_payload_fraction = self._io.read_u1()
            self.leaf_payload_fraction = self._io.read_u1()
            self.file_change_counter = self._io.read_u4be()
            self.num_pages = self._io.read_u4be()
            self.first_freelist_trunk_page = Sqlite3.FreelistTrunkPagePointer(self._io, self, self._root)
            self.first_freelist_trunk_page._read()
            self.num_freelist_pages = self._io.read_u4be()
            self.schema_cookie = self._io.read_u4be()
            self.schema_format = self._io.read_u4be()
            self.default_page_cache_size = self._io.read_u4be()
            self.largest_root_page = self._io.read_u4be()
            self.text_encoding = self._io.read_u4be()
            self.user_version = self._io.read_u4be()
            self.is_incremental_vacuum = self._io.read_u4be()
            self.application_id = self._io.read_u4be()
            self.reserved_header_bytes = self._io.read_bytes(20)
            self.version_valid_for = self._io.read_u4be()
            self.sqlite_version_number = self._io.read_u4be()


        def _fetch_instances(self):
            pass
            self.first_freelist_trunk_page._fetch_instances()


        def _write__seq(self, io=None):
            super(Sqlite3.DatabaseHeader, self)._write__seq(io)
            self._io.write_bytes(self.magic)
            self._io.write_u2be(self.page_size_raw)
            self._io.write_u1(int(self.write_version))
            self._io.write_u1(int(self.read_version))
            self._io.write_u1(self.page_reserved_space_size)
            self._io.write_u1(self.max_payload_fraction)
            self._io.write_u1(self.min_payload_fraction)
            self._io.write_u1(self.leaf_payload_fraction)
            self._io.write_u4be(self.file_change_counter)
            self._io.write_u4be(self.num_pages)
            self.first_freelist_trunk_page._write__seq(self._io)
            self._io.write_u4be(self.num_freelist_pages)
            self._io.write_u4be(self.schema_cookie)
            self._io.write_u4be(self.schema_format)
            self._io.write_u4be(self.default_page_cache_size)
            self._io.write_u4be(self.largest_root_page)
            self._io.write_u4be(self.text_encoding)
            self._io.write_u4be(self.user_version)
            self._io.write_u4be(self.is_incremental_vacuum)
            self._io.write_u4be(self.application_id)
            self._io.write_bytes(self.reserved_header_bytes)
            self._io.write_u4be(self.version_valid_for)
            self._io.write_u4be(self.sqlite_version_number)


        def _check(self):
            pass
            if (len(self.magic) != 16):
                raise kaitaistruct.ConsistencyError(u"magic", len(self.magic), 16)
            if not (self.magic == b"\x53\x51\x4C\x69\x74\x65\x20\x66\x6F\x72\x6D\x61\x74\x20\x33\x00"):
                raise kaitaistruct.ValidationNotEqualError(b"\x53\x51\x4C\x69\x74\x65\x20\x66\x6F\x72\x6D\x61\x74\x20\x33\x00", self.magic, None, u"/types/database_header/seq/0")
            if self.first_freelist_trunk_page._root != self._root:
                raise kaitaistruct.ConsistencyError(u"first_freelist_trunk_page", self.first_freelist_trunk_page._root, self._root)
            if self.first_freelist_trunk_page._parent != self:
                raise kaitaistruct.ConsistencyError(u"first_freelist_trunk_page", self.first_freelist_trunk_page._parent, self)
            if (len(self.reserved_header_bytes) != 20):
                raise kaitaistruct.ConsistencyError(u"reserved_header_bytes", len(self.reserved_header_bytes), 20)

        @property
        def num_ptrmap_pages(self):
            """The number of ptrmap pages in the database."""
            if hasattr(self, '_m_num_ptrmap_pages'):
                return self._m_num_ptrmap_pages

            self._m_num_ptrmap_pages = ((self.num_pages // self.num_ptrmap_entries_max + 1) if (self.idx_first_ptrmap_page > 0) else 0)
            return getattr(self, '_m_num_ptrmap_pages', None)

        def _invalidate_num_ptrmap_pages(self):
            del self._m_num_ptrmap_pages
        @property
        def idx_last_ptrmap_page(self):
            """The index (0-based) of the last ptrmap page (inclusive)."""
            if hasattr(self, '_m_idx_last_ptrmap_page'):
                return self._m_idx_last_ptrmap_page

            self._m_idx_last_ptrmap_page = ((self.idx_first_ptrmap_page + self.num_ptrmap_pages) - (0 if ((self.idx_first_ptrmap_page + self.num_ptrmap_pages) >= self.idx_lock_byte_page) else 1))
            return getattr(self, '_m_idx_last_ptrmap_page', None)

        def _invalidate_idx_last_ptrmap_page(self):
            del self._m_idx_last_ptrmap_page
        @property
        def idx_first_ptrmap_page(self):
            """The index (0-based) of the first ptrmap page."""
            if hasattr(self, '_m_idx_first_ptrmap_page'):
                return self._m_idx_first_ptrmap_page

            self._m_idx_first_ptrmap_page = (1 if (self.largest_root_page > 0) else 0)
            return getattr(self, '_m_idx_first_ptrmap_page', None)

        def _invalidate_idx_first_ptrmap_page(self):
            del self._m_idx_first_ptrmap_page
        @property
        def overflow_min_payload_size(self):
            """The minimum amount of payload that must be stored on the btree page before spilling is allowed."""
            if hasattr(self, '_m_overflow_min_payload_size'):
                return self._m_overflow_min_payload_size

            self._m_overflow_min_payload_size = (((self.usable_size - 12) * 32) // 255 - 23)
            return getattr(self, '_m_overflow_min_payload_size', None)

        def _invalidate_overflow_min_payload_size(self):
            del self._m_overflow_min_payload_size
        @property
        def num_ptrmap_entries_max(self):
            """The maximum number of ptrmap entries per ptrmap page."""
            if hasattr(self, '_m_num_ptrmap_entries_max'):
                return self._m_num_ptrmap_entries_max

            self._m_num_ptrmap_entries_max = self.usable_size // 5
            return getattr(self, '_m_num_ptrmap_entries_max', None)

        def _invalidate_num_ptrmap_entries_max(self):
            del self._m_num_ptrmap_entries_max
        @property
        def idx_lock_byte_page(self):
            if hasattr(self, '_m_idx_lock_byte_page'):
                return self._m_idx_lock_byte_page

            self._m_idx_lock_byte_page = 1073741824 // self.page_size
            return getattr(self, '_m_idx_lock_byte_page', None)

        def _invalidate_idx_lock_byte_page(self):
            del self._m_idx_lock_byte_page
        @property
        def page_size(self):
            """The database page size in bytes."""
            if hasattr(self, '_m_page_size'):
                return self._m_page_size

            self._m_page_size = (65536 if (self.page_size_raw == 1) else self.page_size_raw)
            return getattr(self, '_m_page_size', None)

        def _invalidate_page_size(self):
            del self._m_page_size
        @property
        def table_max_overflow_payload_size(self):
            """The maximum amount of payload that can be stored directly on the b-tree page without spilling onto an overflow page. Value for table page."""
            if hasattr(self, '_m_table_max_overflow_payload_size'):
                return self._m_table_max_overflow_payload_size

            self._m_table_max_overflow_payload_size = (self.usable_size - 35)
            return getattr(self, '_m_table_max_overflow_payload_size', None)

        def _invalidate_table_max_overflow_payload_size(self):
            del self._m_table_max_overflow_payload_size
        @property
        def index_max_overflow_payload_size(self):
            """The maximum amount of payload that can be stored directly on the b-tree page without spilling onto an overflow page. Value for index page."""
            if hasattr(self, '_m_index_max_overflow_payload_size'):
                return self._m_index_max_overflow_payload_size

            self._m_index_max_overflow_payload_size = (((self.usable_size - 12) * 64) // 255 - 23)
            return getattr(self, '_m_index_max_overflow_payload_size', None)

        def _invalidate_index_max_overflow_payload_size(self):
            del self._m_index_max_overflow_payload_size
        @property
        def usable_size(self):
            """The "usable size" of a database page."""
            if hasattr(self, '_m_usable_size'):
                return self._m_usable_size

            self._m_usable_size = (self.page_size - self.page_reserved_space_size)
            return getattr(self, '_m_usable_size', None)

        def _invalidate_usable_size(self):
            del self._m_usable_size

    class TableLeafCell(ReadWriteKaitaiStruct):
        """
        .. seealso::
           Source - https://www.sqlite.org/fileformat2.html#b_tree_pages
        """
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.payload_size = vlq_base128_be.VlqBase128Be(self._io)
            self.payload_size._read()
            self.row_id = vlq_base128_be.VlqBase128Be(self._io)
            self.row_id._read()
            _on = (1 if (self.payload_size.value > self._root.header.table_max_overflow_payload_size) else 0)
            if _on == 0:
                pass
                self.payload = Sqlite3.Record(self._io, self, self._root)
                self.payload._read()
            elif _on == 1:
                pass
                self.payload = Sqlite3.OverflowRecord(self.payload_size.value, self._root.header.table_max_overflow_payload_size, self._io, self, self._root)
                self.payload._read()


        def _fetch_instances(self):
            pass
            self.payload_size._fetch_instances()
            self.row_id._fetch_instances()
            _on = (1 if (self.payload_size.value > self._root.header.table_max_overflow_payload_size) else 0)
            if _on == 0:
                pass
                self.payload._fetch_instances()
            elif _on == 1:
                pass
                self.payload._fetch_instances()


        def _write__seq(self, io=None):
            super(Sqlite3.TableLeafCell, self)._write__seq(io)
            self.payload_size._write__seq(self._io)
            self.row_id._write__seq(self._io)
            _on = (1 if (self.payload_size.value > self._root.header.table_max_overflow_payload_size) else 0)
            if _on == 0:
                pass
                self.payload._write__seq(self._io)
            elif _on == 1:
                pass
                self.payload._write__seq(self._io)


        def _check(self):
            pass
            _on = (1 if (self.payload_size.value > self._root.header.table_max_overflow_payload_size) else 0)
            if _on == 0:
                pass
                if self.payload._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload._root, self._root)
                if self.payload._parent != self:
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload._parent, self)
            elif _on == 1:
                pass
                if self.payload._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload._root, self._root)
                if self.payload._parent != self:
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload._parent, self)
                if (self.payload.payload_size != self.payload_size.value):
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload.payload_size, self.payload_size.value)
                if (self.payload.overflow_payload_size_max != self._root.header.table_max_overflow_payload_size):
                    raise kaitaistruct.ConsistencyError(u"payload", self.payload.overflow_payload_size_max, self._root.header.table_max_overflow_payload_size)


    class CellPointer(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self._should_write_content = False
            self.content__to_write = True

        def _read(self):
            self.ofs_content = self._io.read_u2be()


        def _fetch_instances(self):
            pass
            _ = self.content
            _on = self._parent.page_type
            if _on == Sqlite3.BtreePageType.table_leaf_page:
                pass
                self.content._fetch_instances()
            elif _on == Sqlite3.BtreePageType.table_interior_page:
                pass
                self.content._fetch_instances()
            elif _on == Sqlite3.BtreePageType.index_leaf_page:
                pass
                self.content._fetch_instances()
            elif _on == Sqlite3.BtreePageType.index_interior_page:
                pass
                self.content._fetch_instances()


        def _write__seq(self, io=None):
            super(Sqlite3.CellPointer, self)._write__seq(io)
            self._should_write_content = self.content__to_write
            self._io.write_u2be(self.ofs_content)


        def _check(self):
            pass

        @property
        def content(self):
            if self._should_write_content:
                self._write_content()
            if hasattr(self, '_m_content'):
                return self._m_content

            _pos = self._io.pos()
            self._io.seek((((-100 if (self._parent.page_number == 1) else 0) + ((self._parent.page_number - 1) * self._root.header.page_size)) + self.ofs_content))
            _on = self._parent.page_type
            if _on == Sqlite3.BtreePageType.table_leaf_page:
                pass
                self._m_content = Sqlite3.TableLeafCell(self._io, self, self._root)
                self._m_content._read()
            elif _on == Sqlite3.BtreePageType.table_interior_page:
                pass
                self._m_content = Sqlite3.TableInteriorCell(self._io, self, self._root)
                self._m_content._read()
            elif _on == Sqlite3.BtreePageType.index_leaf_page:
                pass
                self._m_content = Sqlite3.IndexLeafCell(self._io, self, self._root)
                self._m_content._read()
            elif _on == Sqlite3.BtreePageType.index_interior_page:
                pass
                self._m_content = Sqlite3.IndexInteriorCell(self._io, self, self._root)
                self._m_content._read()
            self._io.seek(_pos)
            return getattr(self, '_m_content', None)

        @content.setter
        def content(self, v):
            self._m_content = v

        def _write_content(self):
            self._should_write_content = False
            _pos = self._io.pos()
            self._io.seek((((-100 if (self._parent.page_number == 1) else 0) + ((self._parent.page_number - 1) * self._root.header.page_size)) + self.ofs_content))
            _on = self._parent.page_type
            if _on == Sqlite3.BtreePageType.table_leaf_page:
                pass
                self.content._write__seq(self._io)
            elif _on == Sqlite3.BtreePageType.table_interior_page:
                pass
                self.content._write__seq(self._io)
            elif _on == Sqlite3.BtreePageType.index_leaf_page:
                pass
                self.content._write__seq(self._io)
            elif _on == Sqlite3.BtreePageType.index_interior_page:
                pass
                self.content._write__seq(self._io)
            self._io.seek(_pos)


        def _check_content(self):
            pass
            _on = self._parent.page_type
            if _on == Sqlite3.BtreePageType.table_leaf_page:
                pass
                if self.content._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"content", self.content._root, self._root)
                if self.content._parent != self:
                    raise kaitaistruct.ConsistencyError(u"content", self.content._parent, self)
            elif _on == Sqlite3.BtreePageType.table_interior_page:
                pass
                if self.content._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"content", self.content._root, self._root)
                if self.content._parent != self:
                    raise kaitaistruct.ConsistencyError(u"content", self.content._parent, self)
            elif _on == Sqlite3.BtreePageType.index_leaf_page:
                pass
                if self.content._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"content", self.content._root, self._root)
                if self.content._parent != self:
                    raise kaitaistruct.ConsistencyError(u"content", self.content._parent, self)
            elif _on == Sqlite3.BtreePageType.index_interior_page:
                pass
                if self.content._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"content", self.content._root, self._root)
                if self.content._parent != self:
                    raise kaitaistruct.ConsistencyError(u"content", self.content._parent, self)


    class Value(ReadWriteKaitaiStruct):
        def __init__(self, serial_type, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self.serial_type = serial_type

        def _read(self):
            _on = self.serial_type.type
            if _on == Sqlite3.Serial.integer_0:
                pass
                self.value = Sqlite3.Int0(self._io, self, self._root)
                self.value._read()
            elif _on == Sqlite3.Serial.two_comp_24:
                pass
                self.value = self._io.read_bits_int_be(24)
            elif _on == Sqlite3.Serial.nil:
                pass
                self.value = Sqlite3.NullValue(self._io, self, self._root)
                self.value._read()
            elif _on == Sqlite3.Serial.blob:
                pass
                self.value = Sqlite3.Blob(self.serial_type.len_blob_string, self._io, self, self._root)
                self.value._read()
            elif _on == Sqlite3.Serial.string_utf8:
                pass
                self.value = Sqlite3.StringUtf8(self.serial_type.len_blob_string, self._io, self, self._root)
                self.value._read()
            elif _on == Sqlite3.Serial.two_comp_16:
                pass
                self.value = self._io.read_s2be()
            elif _on == Sqlite3.Serial.ieee754_64:
                pass
                self.value = self._io.read_f8be()
            elif _on == Sqlite3.Serial.two_comp_8:
                pass
                self.value = self._io.read_s1()
            elif _on == Sqlite3.Serial.string_utf16_be:
                pass
                self.value = Sqlite3.StringUtf16Be(self.serial_type.len_blob_string, self._io, self, self._root)
                self.value._read()
            elif _on == Sqlite3.Serial.two_comp_48:
                pass
                self.value = self._io.read_bits_int_be(48)
            elif _on == Sqlite3.Serial.integer_1:
                pass
                self.value = Sqlite3.Int1(self._io, self, self._root)
                self.value._read()
            elif _on == Sqlite3.Serial.string_utf16_le:
                pass
                self.value = Sqlite3.StringUtf16Le(self.serial_type.len_blob_string, self._io, self, self._root)
                self.value._read()
            elif _on == Sqlite3.Serial.two_comp_32:
                pass
                self.value = self._io.read_s4be()
            elif _on == Sqlite3.Serial.two_comp_64:
                pass
                self.value = self._io.read_s8be()


        def _fetch_instances(self):
            pass
            _on = self.serial_type.type
            if _on == Sqlite3.Serial.integer_0:
                pass
                self.value._fetch_instances()
            elif _on == Sqlite3.Serial.two_comp_24:
                pass
            elif _on == Sqlite3.Serial.nil:
                pass
                self.value._fetch_instances()
            elif _on == Sqlite3.Serial.blob:
                pass
                self.value._fetch_instances()
            elif _on == Sqlite3.Serial.string_utf8:
                pass
                self.value._fetch_instances()
            elif _on == Sqlite3.Serial.two_comp_16:
                pass
            elif _on == Sqlite3.Serial.ieee754_64:
                pass
            elif _on == Sqlite3.Serial.two_comp_8:
                pass
            elif _on == Sqlite3.Serial.string_utf16_be:
                pass
                self.value._fetch_instances()
            elif _on == Sqlite3.Serial.two_comp_48:
                pass
            elif _on == Sqlite3.Serial.integer_1:
                pass
                self.value._fetch_instances()
            elif _on == Sqlite3.Serial.string_utf16_le:
                pass
                self.value._fetch_instances()
            elif _on == Sqlite3.Serial.two_comp_32:
                pass
            elif _on == Sqlite3.Serial.two_comp_64:
                pass


        def _write__seq(self, io=None):
            super(Sqlite3.Value, self)._write__seq(io)
            _on = self.serial_type.type
            if _on == Sqlite3.Serial.integer_0:
                pass
                self.value._write__seq(self._io)
            elif _on == Sqlite3.Serial.two_comp_24:
                pass
                self._io.write_bits_int_be(24, self.value)
            elif _on == Sqlite3.Serial.nil:
                pass
                self.value._write__seq(self._io)
            elif _on == Sqlite3.Serial.blob:
                pass
                self.value._write__seq(self._io)
            elif _on == Sqlite3.Serial.string_utf8:
                pass
                self.value._write__seq(self._io)
            elif _on == Sqlite3.Serial.two_comp_16:
                pass
                self._io.write_s2be(self.value)
            elif _on == Sqlite3.Serial.ieee754_64:
                pass
                self._io.write_f8be(self.value)
            elif _on == Sqlite3.Serial.two_comp_8:
                pass
                self._io.write_s1(self.value)
            elif _on == Sqlite3.Serial.string_utf16_be:
                pass
                self.value._write__seq(self._io)
            elif _on == Sqlite3.Serial.two_comp_48:
                pass
                self._io.write_bits_int_be(48, self.value)
            elif _on == Sqlite3.Serial.integer_1:
                pass
                self.value._write__seq(self._io)
            elif _on == Sqlite3.Serial.string_utf16_le:
                pass
                self.value._write__seq(self._io)
            elif _on == Sqlite3.Serial.two_comp_32:
                pass
                self._io.write_s4be(self.value)
            elif _on == Sqlite3.Serial.two_comp_64:
                pass
                self._io.write_s8be(self.value)


        def _check(self):
            pass
            _on = self.serial_type.type
            if _on == Sqlite3.Serial.integer_0:
                pass
                if self.value._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._root, self._root)
                if self.value._parent != self:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._parent, self)
            elif _on == Sqlite3.Serial.two_comp_24:
                pass
            elif _on == Sqlite3.Serial.nil:
                pass
                if self.value._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._root, self._root)
                if self.value._parent != self:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._parent, self)
            elif _on == Sqlite3.Serial.blob:
                pass
                if self.value._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._root, self._root)
                if self.value._parent != self:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._parent, self)
                if (self.value.len_value != self.serial_type.len_blob_string):
                    raise kaitaistruct.ConsistencyError(u"value", self.value.len_value, self.serial_type.len_blob_string)
            elif _on == Sqlite3.Serial.string_utf8:
                pass
                if self.value._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._root, self._root)
                if self.value._parent != self:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._parent, self)
                if (self.value.len_value != self.serial_type.len_blob_string):
                    raise kaitaistruct.ConsistencyError(u"value", self.value.len_value, self.serial_type.len_blob_string)
            elif _on == Sqlite3.Serial.two_comp_16:
                pass
            elif _on == Sqlite3.Serial.ieee754_64:
                pass
            elif _on == Sqlite3.Serial.two_comp_8:
                pass
            elif _on == Sqlite3.Serial.string_utf16_be:
                pass
                if self.value._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._root, self._root)
                if self.value._parent != self:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._parent, self)
                if (self.value.len_value != self.serial_type.len_blob_string):
                    raise kaitaistruct.ConsistencyError(u"value", self.value.len_value, self.serial_type.len_blob_string)
            elif _on == Sqlite3.Serial.two_comp_48:
                pass
            elif _on == Sqlite3.Serial.integer_1:
                pass
                if self.value._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._root, self._root)
                if self.value._parent != self:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._parent, self)
            elif _on == Sqlite3.Serial.string_utf16_le:
                pass
                if self.value._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._root, self._root)
                if self.value._parent != self:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._parent, self)
                if (self.value.len_value != self.serial_type.len_blob_string):
                    raise kaitaistruct.ConsistencyError(u"value", self.value.len_value, self.serial_type.len_blob_string)
            elif _on == Sqlite3.Serial.two_comp_32:
                pass
            elif _on == Sqlite3.Serial.two_comp_64:
                pass


    class Blob(ReadWriteKaitaiStruct):
        def __init__(self, len_value, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self.len_value = len_value

        def _read(self):
            self.value = self._io.read_bytes(self.len_value)


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Sqlite3.Blob, self)._write__seq(io)
            self._io.write_bytes(self.value)


        def _check(self):
            pass
            if (len(self.value) != self.len_value):
                raise kaitaistruct.ConsistencyError(u"value", len(self.value), self.len_value)


    class Record(ReadWriteKaitaiStruct):
        """
        .. seealso::
           Source - https://sqlite.org/fileformat2.html#record_format
        """
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.header_size = vlq_base128_be.VlqBase128Be(self._io)
            self.header_size._read()
            self._raw_header = self._io.read_bytes((self.header_size.value - 1))
            _io__raw_header = KaitaiStream(BytesIO(self._raw_header))
            self.header = Sqlite3.RecordHeader(_io__raw_header, self, self._root)
            self.header._read()
            self.values = []
            for i in range(len(self.header.value_types)):
                _t_values = Sqlite3.Value(self.header.value_types[i], self._io, self, self._root)
                _t_values._read()
                self.values.append(_t_values)



        def _fetch_instances(self):
            pass
            self.header_size._fetch_instances()
            self.header._fetch_instances()
            for i in range(len(self.values)):
                pass
                self.values[i]._fetch_instances()



        def _write__seq(self, io=None):
            super(Sqlite3.Record, self)._write__seq(io)
            self.header_size._write__seq(self._io)
            _io__raw_header = KaitaiStream(BytesIO(bytearray((self.header_size.value - 1))))
            self._io.add_child_stream(_io__raw_header)
            _pos2 = self._io.pos()
            self._io.seek(self._io.pos() + ((self.header_size.value - 1)))
            def handler(parent, _io__raw_header=_io__raw_header):
                self._raw_header = _io__raw_header.to_byte_array()
                if (len(self._raw_header) != (self.header_size.value - 1)):
                    raise kaitaistruct.ConsistencyError(u"raw(header)", len(self._raw_header), (self.header_size.value - 1))
                parent.write_bytes(self._raw_header)
            _io__raw_header.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
            self.header._write__seq(_io__raw_header)
            for i in range(len(self.values)):
                pass
                self.values[i]._write__seq(self._io)



        def _check(self):
            pass
            if self.header._root != self._root:
                raise kaitaistruct.ConsistencyError(u"header", self.header._root, self._root)
            if self.header._parent != self:
                raise kaitaistruct.ConsistencyError(u"header", self.header._parent, self)
            if (len(self.values) != len(self.header.value_types)):
                raise kaitaistruct.ConsistencyError(u"values", len(self.values), len(self.header.value_types))
            for i in range(len(self.values)):
                pass
                if self.values[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"values", self.values[i]._root, self._root)
                if self.values[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"values", self.values[i]._parent, self)
                if self.values[i].serial_type != self.header.value_types[i]:
                    raise kaitaistruct.ConsistencyError(u"values", self.values[i].serial_type, self.header.value_types[i])



    @property
    def pages(self):
        """This works well when parsing small database files.
        
        problem:
        the first access to db.pages
        for example `db.pages[0]`
        will loop and parse **all** pages.
        
        To parse large database files,
        the user should set
        the internal cache attribute `db._m_pages`
        so that any access to `db.pages`
        will use the cached value in `db._m_pages`.
        
        # import sqlite3.py generated from sqlite3.ksy
        import parser.sqlite3 as parser_sqlite3
        # create a lazy list class
        # accessing db.pages[i] will call pages_list.__getitem__(i)
        class PagesList:
            def __init__(self, db):
                self.db = db
            def __len__(self):
                return self.db.header.num_pages
            def __getitem__(self, i):  # i is 0-based
                db = self.db
                header = db.header
                if i < 0:  # -1 means last page, etc
                    i = header.num_pages + i
                assert (
                    0 <= i and i < header.num_pages
                ), f"page index is out of range: {i} is not in (0, {header.num_pages - 1})"
                # todo: maybe cache page
                # equality test: page_a.page_number == page_b.page_number
                _pos = db._io.pos()
                db._io.seek(i * header.page_size)
                if i == header.idx_lock_byte_page:
                    page = parser_sqlite3.Sqlite3.LockBytePage((i + 1), db._io, db, db._root)
                elif (
                    i >= header.idx_first_ptrmap_page and
                    i <= header.idx_last_ptrmap_page
                ):
                    page = parser_sqlite3.Sqlite3.PtrmapPage((i + 1), db._io, db, db._root)
                else:
                    page = parser_sqlite3.Sqlite3.BtreePage((i + 1), db._io, db, db._root)
                db._io.seek(_pos)
                return page
        # create a database parser
        database = "test.db"
        db = parser_sqlite3.Sqlite3.from_file(database)
        # patch the internal cache attribute of db.pages
        db._m_pages = PagesList(db)
        db._read()
        # now, this will parse **only** the first page
        page = db.pages[0]
        page._read()
        """
        if self._should_write_pages:
            self._write_pages()
        if hasattr(self, '_m_pages'):
            return self._m_pages

        _pos = self._io.pos()
        self._io.seek(100)
        self._raw__m_pages = []
        self._m_pages = []
        for i in range(self.header.num_pages):
            _on = (0 if (i == self.header.idx_lock_byte_page) else (1 if  (((i >= self.header.idx_first_ptrmap_page)) and ((i <= self.header.idx_last_ptrmap_page)))  else 2))
            if _on == 0:
                pass
                self._raw__m_pages.append(self._io.read_bytes(((self.header.page_size - 100) if (i == 0) else self.header.page_size)))
                _io__raw__m_pages = KaitaiStream(BytesIO(self._raw__m_pages[-1]))
                _t__m_pages = Sqlite3.LockBytePage((i + 1), _io__raw__m_pages, self, self._root)
                _t__m_pages._read()
                self._m_pages.append(_t__m_pages)
            elif _on == 1:
                pass
                self._raw__m_pages.append(self._io.read_bytes(((self.header.page_size - 100) if (i == 0) else self.header.page_size)))
                _io__raw__m_pages = KaitaiStream(BytesIO(self._raw__m_pages[-1]))
                _t__m_pages = Sqlite3.PointerMapPage((i + 1), _io__raw__m_pages, self, self._root)
                _t__m_pages._read()
                self._m_pages.append(_t__m_pages)
            elif _on == 2:
                pass
                self._raw__m_pages.append(self._io.read_bytes(((self.header.page_size - 100) if (i == 0) else self.header.page_size)))
                _io__raw__m_pages = KaitaiStream(BytesIO(self._raw__m_pages[-1]))
                _t__m_pages = Sqlite3.BtreePage((i + 1), _io__raw__m_pages, self, self._root)
                _t__m_pages._read()
                self._m_pages.append(_t__m_pages)
            else:
                pass
                self._m_pages.append(self._io.read_bytes(((self.header.page_size - 100) if (i == 0) else self.header.page_size)))

        self._io.seek(_pos)
        return getattr(self, '_m_pages', None)

    @pages.setter
    def pages(self, v):
        self._m_pages = v

    def _write_pages(self):
        self._should_write_pages = False
        _pos = self._io.pos()
        self._io.seek(100)
        self._raw__m_pages = []
        for i in range(len(self._m_pages)):
            pass
            _on = (0 if (i == self.header.idx_lock_byte_page) else (1 if  (((i >= self.header.idx_first_ptrmap_page)) and ((i <= self.header.idx_last_ptrmap_page)))  else 2))
            if _on == 0:
                pass
                _io__raw__m_pages = KaitaiStream(BytesIO(bytearray(((self.header.page_size - 100) if (i == 0) else self.header.page_size))))
                self._io.add_child_stream(_io__raw__m_pages)
                _pos2 = self._io.pos()
                self._io.seek(self._io.pos() + (((self.header.page_size - 100) if (i == 0) else self.header.page_size)))
                def handler(parent, _io__raw__m_pages=_io__raw__m_pages, i=i):
                    self._raw__m_pages.append(_io__raw__m_pages.to_byte_array())
                    if (len(self._raw__m_pages[(len(self._raw__m_pages) - 1)]) != ((self.header.page_size - 100) if (i == 0) else self.header.page_size)):
                        raise kaitaistruct.ConsistencyError(u"raw(pages)", len(self._raw__m_pages[(len(self._raw__m_pages) - 1)]), ((self.header.page_size - 100) if (i == 0) else self.header.page_size))
                    parent.write_bytes(self._raw__m_pages[(len(self._raw__m_pages) - 1)])
                _io__raw__m_pages.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
                self.pages[i]._write__seq(_io__raw__m_pages)
            elif _on == 1:
                pass
                _io__raw__m_pages = KaitaiStream(BytesIO(bytearray(((self.header.page_size - 100) if (i == 0) else self.header.page_size))))
                self._io.add_child_stream(_io__raw__m_pages)
                _pos2 = self._io.pos()
                self._io.seek(self._io.pos() + (((self.header.page_size - 100) if (i == 0) else self.header.page_size)))
                def handler(parent, _io__raw__m_pages=_io__raw__m_pages, i=i):
                    self._raw__m_pages.append(_io__raw__m_pages.to_byte_array())
                    if (len(self._raw__m_pages[(len(self._raw__m_pages) - 1)]) != ((self.header.page_size - 100) if (i == 0) else self.header.page_size)):
                        raise kaitaistruct.ConsistencyError(u"raw(pages)", len(self._raw__m_pages[(len(self._raw__m_pages) - 1)]), ((self.header.page_size - 100) if (i == 0) else self.header.page_size))
                    parent.write_bytes(self._raw__m_pages[(len(self._raw__m_pages) - 1)])
                _io__raw__m_pages.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
                self.pages[i]._write__seq(_io__raw__m_pages)
            elif _on == 2:
                pass
                _io__raw__m_pages = KaitaiStream(BytesIO(bytearray(((self.header.page_size - 100) if (i == 0) else self.header.page_size))))
                self._io.add_child_stream(_io__raw__m_pages)
                _pos2 = self._io.pos()
                self._io.seek(self._io.pos() + (((self.header.page_size - 100) if (i == 0) else self.header.page_size)))
                def handler(parent, _io__raw__m_pages=_io__raw__m_pages, i=i):
                    self._raw__m_pages.append(_io__raw__m_pages.to_byte_array())
                    if (len(self._raw__m_pages[(len(self._raw__m_pages) - 1)]) != ((self.header.page_size - 100) if (i == 0) else self.header.page_size)):
                        raise kaitaistruct.ConsistencyError(u"raw(pages)", len(self._raw__m_pages[(len(self._raw__m_pages) - 1)]), ((self.header.page_size - 100) if (i == 0) else self.header.page_size))
                    parent.write_bytes(self._raw__m_pages[(len(self._raw__m_pages) - 1)])
                _io__raw__m_pages.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
                self.pages[i]._write__seq(_io__raw__m_pages)
            else:
                pass
                self._io.write_bytes(self.pages[i])

        self._io.seek(_pos)


    def _check_pages(self):
        pass
        if (len(self.pages) != self.header.num_pages):
            raise kaitaistruct.ConsistencyError(u"pages", len(self.pages), self.header.num_pages)
        for i in range(len(self._m_pages)):
            pass
            _on = (0 if (i == self.header.idx_lock_byte_page) else (1 if  (((i >= self.header.idx_first_ptrmap_page)) and ((i <= self.header.idx_last_ptrmap_page)))  else 2))
            if _on == 0:
                pass
                if self.pages[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"pages", self.pages[i]._root, self._root)
                if self.pages[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"pages", self.pages[i]._parent, self)
                if (self.pages[i].page_number != (i + 1)):
                    raise kaitaistruct.ConsistencyError(u"pages", self.pages[i].page_number, (i + 1))
            elif _on == 1:
                pass
                if self.pages[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"pages", self.pages[i]._root, self._root)
                if self.pages[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"pages", self.pages[i]._parent, self)
                if (self.pages[i].pointer_map_page_number != (i + 1)):
                    raise kaitaistruct.ConsistencyError(u"pages", self.pages[i].pointer_map_page_number, (i + 1))
            elif _on == 2:
                pass
                if self.pages[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"pages", self.pages[i]._root, self._root)
                if self.pages[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"pages", self.pages[i]._parent, self)
                if (self.pages[i].page_number != (i + 1)):
                    raise kaitaistruct.ConsistencyError(u"pages", self.pages[i].page_number, (i + 1))
            else:
                pass
                if (len(self.pages[i]) != ((self.header.page_size - 100) if (i == 0) else self.header.page_size)):
                    raise kaitaistruct.ConsistencyError(u"pages", len(self.pages[i]), ((self.header.page_size - 100) if (i == 0) else self.header.page_size))



