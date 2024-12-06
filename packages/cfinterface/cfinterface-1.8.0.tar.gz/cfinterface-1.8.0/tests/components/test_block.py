from typing import IO

import pytest

from cfinterface.components.block import Block
from cfinterface.components.literalfield import LiteralField
from tests.mocks.mock_open import mock_open

from unittest.mock import MagicMock, patch


class DummyBlock(Block):
    BEGIN_PATTERN = "beg"
    END_PATTERN = "end"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        else:
            return o.data == self.data

    def read(self, file: IO) -> bool:
        self.data = file.readline().strip()
        return True

    def write(self, file: IO) -> bool:
        file.write(self.data)
        return True


class DummyBinaryBlock(Block):
    BEGIN_PATTERN = b"0"
    END_PATTERN = b"1"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self._field = LiteralField(5)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        else:
            return o.data == self.data

    def read(self, file: IO) -> bool:
        self._field.read(file.read(self._field.size))
        self.data = self._field.value
        return True

    def write(self, file: IO) -> bool:
        self._field.value = self.data
        file.write(DummyBinaryBlock.BEGIN_PATTERN)
        file.write(self._field.write(b""))
        file.write(DummyBinaryBlock.END_PATTERN)
        return True


def test_single_block_properties():
    b1 = Block()
    assert b1.is_first
    assert b1.is_last


def test_block_simple_chain_properties():
    # Build a simple block chain
    b1 = Block()
    b2 = Block()
    b3 = Block()
    # Sets relationships
    b1.next = b2
    b2.previous = b1
    b2.next = b3
    b3.previous = b2
    # Asserts properties
    assert b1.is_first
    assert b3.is_last
    assert not b1.is_last
    assert not b2.is_first
    assert not b2.is_last
    assert not b3.is_first
    assert b1.empty
    assert b2.empty
    assert b3.empty


def test_block_equal_error():
    b1 = Block()
    b2 = Block()
    with pytest.raises(NotImplementedError):
        b1 == b2


def test_block_read_error():
    b = Block()
    with pytest.raises(NotImplementedError):
        m: MagicMock = mock_open(read_data="")
        with patch("builtins.open", m):
            with open("", "r") as fp:
                b.read_block(fp)


def test_block_write_error():
    b = Block()
    with pytest.raises(NotImplementedError):
        m: MagicMock = mock_open(read_data="")
        with patch("builtins.open", m):
            with open("", "r") as fp:
                b.write_block(fp)


def test_dummy_block_equal():
    b1 = DummyBlock()
    b2 = DummyBlock()
    assert b1 == b2


def test_dummy_block_read():
    data = "Hello, world!"
    filedata = (
        "\n".join([DummyBlock.BEGIN_PATTERN, data, DummyBlock.END_PATTERN])
        + "\n"
    )
    m: MagicMock = mock_open(read_data=filedata)
    with patch("builtins.open", m):
        with open("", "r") as fp:
            b = DummyBlock()
            assert DummyBlock.begins(fp.readline())
            b.read_block(fp)
            assert b.data == data
            assert DummyBlock.ends(fp.readline())


def test_dummy_block_write():
    data = "Hello, world!"
    filedata = ""
    m = mock_open(read_data=filedata)
    with patch("builtins.open", m):
        with open("", "w") as fp:
            b = DummyBlock()
            b.data = data
            b.write_block(fp)
    m().write.assert_called_once_with(data)


def test_dummy_binary_block_read():
    data = "hello"
    filedata = b"0hello1"
    m: MagicMock = mock_open(read_data=filedata)
    with patch("builtins.open", m):
        with open("", "rb") as fp:
            b = DummyBinaryBlock()
            assert DummyBinaryBlock.begins(fp.read(1), storage="BINARY")
            b.read_block(fp)
            assert b.data == data
            assert DummyBinaryBlock.ends(fp.read(1), storage="BINARY")


def test_dummy_binary_block_write():
    data = "hello"
    filedata = ""
    m = mock_open(read_data=filedata)
    with patch("builtins.open", m):
        with open("", "wb") as fp:
            b = DummyBinaryBlock()
            b.data = data
            b.write_block(fp)
    m().write.assert_any_call(b"hello")
