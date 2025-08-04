# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import ReadWriteKaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class VlqBase128Be(ReadWriteKaitaiStruct):
    """A variable-length unsigned integer using base128 encoding. 1-byte groups
    consist of 1-bit flag of continuation and 7-bit value chunk, and are ordered
    "most significant group first", i.e. in "big-endian" manner.
    
    This particular encoding is specified and used in:
    
    * Standard MIDI file format
    * ASN.1 BER encoding
    * RAR 5.0 file format
    
    More information on this encoding is available at
    https://en.wikipedia.org/wiki/Variable-length_quantity
    
    This particular implementation supports serialized values to up 8 bytes long.
    """
    def __init__(self, _io=None, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self

    def _read(self):
        self.groups = []
        i = 0
        while True:
            _t_groups = VlqBase128Be.Group(self._io, self, self._root)
            _t_groups._read()
            _ = _t_groups
            self.groups.append(_)
            if not (_.has_next):
                break
            i += 1


    def _fetch_instances(self):
        pass
        for i in range(len(self.groups)):
            pass
            self.groups[i]._fetch_instances()



    def _write__seq(self, io=None):
        super(VlqBase128Be, self)._write__seq(io)
        for i in range(len(self.groups)):
            pass
            self.groups[i]._write__seq(self._io)



    def _check(self):
        pass
        if (len(self.groups) == 0):
            raise kaitaistruct.ConsistencyError(u"groups", len(self.groups), 0)
        for i in range(len(self.groups)):
            pass
            if self.groups[i]._root != self._root:
                raise kaitaistruct.ConsistencyError(u"groups", self.groups[i]._root, self._root)
            if self.groups[i]._parent != self:
                raise kaitaistruct.ConsistencyError(u"groups", self.groups[i]._parent, self)
            _ = self.groups[i]
            if (not (_.has_next) != (i == (len(self.groups) - 1))):
                raise kaitaistruct.ConsistencyError(u"groups", not (_.has_next), (i == (len(self.groups) - 1)))


    class Group(ReadWriteKaitaiStruct):
        """One byte group, clearly divided into 7-bit "value" chunk and 1-bit "continuation" flag.
        """
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.b = self._io.read_u1()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(VlqBase128Be.Group, self)._write__seq(io)
            self._io.write_u1(self.b)


        def _check(self):
            pass

        @property
        def has_next(self):
            """If true, then we have more bytes to read."""
            if hasattr(self, '_m_has_next'):
                return self._m_has_next

            self._m_has_next = ((self.b & 128) != 0)
            return getattr(self, '_m_has_next', None)

        def _invalidate_has_next(self):
            del self._m_has_next
        @property
        def value(self):
            """The 7-bit (base128) numeric value chunk of this group."""
            if hasattr(self, '_m_value'):
                return self._m_value

            self._m_value = (self.b & 127)
            return getattr(self, '_m_value', None)

        def _invalidate_value(self):
            del self._m_value

    @property
    def last(self):
        if hasattr(self, '_m_last'):
            return self._m_last

        self._m_last = (len(self.groups) - 1)
        return getattr(self, '_m_last', None)

    def _invalidate_last(self):
        del self._m_last
    @property
    def value(self):
        """Resulting value as normal integer."""
        if hasattr(self, '_m_value'):
            return self._m_value

        self._m_value = (((((((self.groups[self.last].value + ((self.groups[(self.last - 1)].value << 7) if (self.last >= 1) else 0)) + ((self.groups[(self.last - 2)].value << 14) if (self.last >= 2) else 0)) + ((self.groups[(self.last - 3)].value << 21) if (self.last >= 3) else 0)) + ((self.groups[(self.last - 4)].value << 28) if (self.last >= 4) else 0)) + ((self.groups[(self.last - 5)].value << 35) if (self.last >= 5) else 0)) + ((self.groups[(self.last - 6)].value << 42) if (self.last >= 6) else 0)) + ((self.groups[(self.last - 7)].value << 49) if (self.last >= 7) else 0))
        return getattr(self, '_m_value', None)

    def _invalidate_value(self):
        del self._m_value

