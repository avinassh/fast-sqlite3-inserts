import io
import kaitaistruct
import kaitaistruct_sqlite3
import vlq_base128_be
import pyvlq

root_size = 8192

def get_root(_io=None, check=True):
    if not _io:
        _io = kaitaistruct.KaitaiStream(io.BytesIO(bytearray(root_size)))
    root = kaitaistruct_sqlite3.Sqlite3(_io=_io, _parent=None, _root=None)
    root.header = kaitaistruct_sqlite3.Sqlite3.DatabaseHeader(_io=root._io, _parent=root, _root=root._root)
    def init_header(header):
        header.magic = b'SQLite format 3\x00'
        header.page_size_raw = 4096 # 0x1000
        header.write_version = kaitaistruct_sqlite3.Sqlite3.FormatVersion.legacy # 1
        header.read_version = kaitaistruct_sqlite3.Sqlite3.FormatVersion.legacy # 1
        header.page_reserved_space_size = 0
        header.max_payload_fraction = 64 # 0x40
        header.min_payload_fraction = 32 # 0x20
        header.leaf_payload_fraction = 32 # 0x20
        header.file_change_counter = 1
        header.num_pages = 2
        header.first_freelist_trunk_page = kaitaistruct_sqlite3.Sqlite3.FreelistTrunkPagePointer(_io=root._io, _parent=header, _root=header._root)
        def init_first_freelist_trunk_page(first_freelist_trunk_page):
            first_freelist_trunk_page.page_number = 0
            first_freelist_trunk_page.page = None
        init_first_freelist_trunk_page(header.first_freelist_trunk_page)
        header.num_freelist_pages = 0
        header.schema_cookie = 1
        header.schema_format = 4
        header.default_page_cache_size = 0
        header.largest_root_page = 0
        header.text_encoding = 1
        header.user_version = 0
        header.is_incremental_vacuum = 0
        header.application_id = 0
        header.reserved_header_bytes = 20 * b'\x00'
        header.version_valid_for = 1
        header.sqlite_version_number = 3050001 # 0x2e8a11
    init_header(root.header)
    root.pages = []
    root.pages.append(kaitaistruct_sqlite3.Sqlite3.BtreePage(page_number=1, _io=root._io, _parent=root, _root=root._root))
    def init_page(page):
        page.page_type = kaitaistruct_sqlite3.Sqlite3.BtreePageType.table_leaf_page # 13 = 0xd
        page.first_freeblock = 0
        page.num_cells = 1
        page.ofs_cell_content_area_raw = 4044 # 0xfcc
        page.num_frag_free_bytes = 0
        page.cell_pointers = []
        page.cell_pointers.append(kaitaistruct_sqlite3.Sqlite3.CellPointer(_io=root._io, _parent=page, _root=page._root))
        def init_cell_pointer(cell_pointer):
            cell_pointer.ofs_content = 4044 # 0xfcc
            cell_pointer.content = kaitaistruct_sqlite3.Sqlite3.TableLeafCell(_io=root._io, _parent=cell_pointer, _root=cell_pointer._root)
            def init_content(content):
                content.payload_size = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(50))
                # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
                content.payload_size._read()
                content.row_id = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(1))
                # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
                content.row_id._read()
                content.payload = kaitaistruct_sqlite3.Sqlite3.Record(_io=root._io, _parent=content, _root=content._root)
                def init_payload(payload):
                    payload.header_size = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(6))
                    # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
                    payload.header_size._read()
                    payload._raw_header = b'\x17\x15\x15\x01I'
                    payload.header = kaitaistruct_sqlite3.Sqlite3.RecordHeader(_io=root._io, _parent=payload, _root=payload._root)
                    def init_header(header):
                        header.value_types = []
                        header.value_types.append(kaitaistruct_sqlite3.Sqlite3.SerialType(_io=root._io, _parent=header, _root=header._root))
                        def init_value_type(value_type):
                            value_type.raw_value = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(23))
                            # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
                            value_type.raw_value._read()
                        init_value_type(header.value_types[0])
                        header.value_types.append(kaitaistruct_sqlite3.Sqlite3.SerialType(_io=root._io, _parent=header, _root=header._root))
                        def init_value_type(value_type):
                            value_type.raw_value = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(21))
                            # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
                            value_type.raw_value._read()
                        init_value_type(header.value_types[1])
                        header.value_types.append(kaitaistruct_sqlite3.Sqlite3.SerialType(_io=root._io, _parent=header, _root=header._root))
                        def init_value_type(value_type):
                            value_type.raw_value = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(21))
                            # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
                            value_type.raw_value._read()
                        init_value_type(header.value_types[2])
                        header.value_types.append(kaitaistruct_sqlite3.Sqlite3.SerialType(_io=root._io, _parent=header, _root=header._root))
                        def init_value_type(value_type):
                            value_type.raw_value = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(1))
                            # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
                            value_type.raw_value._read()
                        init_value_type(header.value_types[3])
                        header.value_types.append(kaitaistruct_sqlite3.Sqlite3.SerialType(_io=root._io, _parent=header, _root=header._root))
                        def init_value_type(value_type):
                            value_type.raw_value = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(73))
                            # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
                            value_type.raw_value._read()
                        init_value_type(header.value_types[4])
                    init_header(payload.header)
                    payload.values = []
                    def get_value_serial_type():
                        value_serial_type = kaitaistruct_sqlite3.Sqlite3.SerialType(_io=root._io, _parent=payload, _root=payload._root)
                        value_serial_type.raw_value = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(23))
                        # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
                        value_serial_type.raw_value._read()
                        return value_serial_type
                    payload.values.append(kaitaistruct_sqlite3.Sqlite3.Value(serial_type=get_value_serial_type(), _io=root._io, _parent=payload, _root=payload._root))
                    def init_value(value):
                        value.value = kaitaistruct_sqlite3.Sqlite3.StringUtf8(len_value=5, _io=root._io, _parent=value, _root=value._root)
                        def init_value(value):
                            value.value = 'table'
                        init_value(value.value)
                    init_value(payload.values[0])
                    def get_value_serial_type():
                        value_serial_type = kaitaistruct_sqlite3.Sqlite3.SerialType(_io=root._io, _parent=payload, _root=payload._root)
                        value_serial_type.raw_value = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(21))
                        # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
                        value_serial_type.raw_value._read()
                        return value_serial_type
                    payload.values.append(kaitaistruct_sqlite3.Sqlite3.Value(serial_type=get_value_serial_type(), _io=root._io, _parent=payload, _root=payload._root))
                    def init_value(value):
                        value.value = kaitaistruct_sqlite3.Sqlite3.StringUtf8(len_value=4, _io=root._io, _parent=value, _root=value._root)
                        def init_value(value):
                            value.value = 'test'
                        init_value(value.value)
                    init_value(payload.values[1])
                    def get_value_serial_type():
                        value_serial_type = kaitaistruct_sqlite3.Sqlite3.SerialType(_io=root._io, _parent=payload, _root=payload._root)
                        value_serial_type.raw_value = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(21))
                        # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
                        value_serial_type.raw_value._read()
                        return value_serial_type
                    payload.values.append(kaitaistruct_sqlite3.Sqlite3.Value(serial_type=get_value_serial_type(), _io=root._io, _parent=payload, _root=payload._root))
                    def init_value(value):
                        value.value = kaitaistruct_sqlite3.Sqlite3.StringUtf8(len_value=4, _io=root._io, _parent=value, _root=value._root)
                        def init_value(value):
                            value.value = 'test'
                        init_value(value.value)
                    init_value(payload.values[2])
                    def get_value_serial_type():
                        value_serial_type = kaitaistruct_sqlite3.Sqlite3.SerialType(_io=root._io, _parent=payload, _root=payload._root)
                        value_serial_type.raw_value = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(1))
                        # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
                        value_serial_type.raw_value._read()
                        return value_serial_type
                    payload.values.append(kaitaistruct_sqlite3.Sqlite3.Value(serial_type=get_value_serial_type(), _io=root._io, _parent=payload, _root=payload._root))
                    def init_value(value):
                        value.value = 2
                    init_value(payload.values[3])
                    def get_value_serial_type():
                        value_serial_type = kaitaistruct_sqlite3.Sqlite3.SerialType(_io=root._io, _parent=payload, _root=payload._root)
                        value_serial_type.raw_value = vlq_base128_be.VlqBase128Be.from_bytes(pyvlq.encode(73))
                        # fix: AttributeError: 'VlqBase128Be' object has no attribute 'groups'
                        value_serial_type.raw_value._read()
                        return value_serial_type
                    payload.values.append(kaitaistruct_sqlite3.Sqlite3.Value(serial_type=get_value_serial_type(), _io=root._io, _parent=payload, _root=payload._root))
                    def init_value(value):
                        value.value = kaitaistruct_sqlite3.Sqlite3.StringUtf8(len_value=30, _io=root._io, _parent=value, _root=value._root)
                        def init_value(value):
                            value.value = 'CREATE TABLE test (id INTEGER)'
                        init_value(value.value)
                    init_value(payload.values[4])
                init_payload(content.payload)
            init_content(cell_pointer.content)
        init_cell_pointer(page.cell_pointers[0])
        page.reserved_space = None
    init_page(root.pages[0])
    root.pages.append(kaitaistruct_sqlite3.Sqlite3.BtreePage(page_number=2, _io=root._io, _parent=root, _root=root._root))
    def init_page(page):
        page.page_type = kaitaistruct_sqlite3.Sqlite3.BtreePageType.table_leaf_page # 13 = 0xd
        page.first_freeblock = 0
        page.num_cells = 0
        page.ofs_cell_content_area_raw = 4096 # 0x1000
        page.num_frag_free_bytes = 0
        page.cell_pointers = []
        page.reserved_space = None
    init_page(root.pages[1])
    if check:
        root._check()
    return root

def get_io():
    root = get_root()
    _io = root._io
    if 1:
        # no. _write calls _fetch_instances which throws
        root._write(_io)
    else:
        root._write__seq(_io)
        # root._fetch_instances() # this would throw
        root._io.write_back_child_streams()
    return _io

def get_bytes():
    _io = get_io()
    _io.seek(0)
    return _io.read_bytes_full()
