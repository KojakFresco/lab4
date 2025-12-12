import pytest
from src.chip import Chip, ChipCollection


def test_chip_init():
    chip = Chip("red", 10)
    assert chip.value == 10


def test_chip_add():
    chip1 = Chip("red", 10)
    chip2 = Chip("blue", 20)
    result = chip1 + chip2
    assert result.value == 30


@pytest.fixture
def chip_collection():
    collection = ChipCollection()
    chip1 = Chip("red", 5)
    chip2 = Chip("blue", 10)
    collection.append(chip1)
    collection.append(chip2)
    return collection


def test_chip_collection_init():
    cc = ChipCollection()
    assert len(cc) == 0


def test_chip_collection_append():
    cc = ChipCollection()
    chip = Chip("red", 10)
    cc.append(chip)
    assert len(cc) == 1
    assert cc[0] == chip


def test_chip_collection_append_and_len(chip_collection):
    assert len(chip_collection) == 2


def test_chip_collection_getitem(chip_collection):
    assert chip_collection[0].value == 5
    assert chip_collection[1].value == 10


def test_chip_collection_contains(chip_collection):
    assert Chip("red", 5) in chip_collection
    assert Chip("green", 20) not in chip_collection


def test_chip_collection_setitem():
    cc = ChipCollection()
    chip1 = Chip("red", 10)
    chip2 = Chip("blue", 20)
    cc.append(chip1)
    cc[0] = chip2
    assert cc[0] == chip2


def test_chip_collection_delitem():
    cc = ChipCollection()
    chip = Chip("red", 10)
    cc.append(chip)
    del cc[0]
    assert len(cc) == 0


def test_chip_collection_len():
    cc = ChipCollection()
    cc.append(Chip("red", 10))
    assert len(cc) == 1


def test_chip_collection_repr():
    cc = ChipCollection()
    chip = Chip("red", 10)
    cc.append(chip)
    assert "ChipCollection" in repr(cc)


def test_chip_collection_iter():
    cc = ChipCollection()
    chip = Chip("red", 10)
    cc.append(chip)
    for c in cc:
        assert c == chip
