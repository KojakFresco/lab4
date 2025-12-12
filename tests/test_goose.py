from src.goose import Goose, HonkGoose, GooseCollection


def test_goose_init():
    goose = Goose("Test", 5)
    assert goose.name == "Test"
    assert goose.honk_volume == 5


def test_honk_goose_call():
    goose = HonkGoose("Test", 5)
    volume = goose()
    assert volume == 5


def test_goose_collection_init():
    gc = GooseCollection()
    assert len(gc) == 0


def test_goose_collection_append():
    gc = GooseCollection()
    goose = HonkGoose("Test", 5)
    gc.append(goose)
    assert len(gc) == 1
    assert gc[0] == goose


def test_goose_collection_getitem():
    gc = GooseCollection()
    goose = HonkGoose("Test", 5)
    gc.append(goose)
    assert gc[0] == goose


def test_goose_collection_setitem():
    gc = GooseCollection()
    goose1 = HonkGoose("Test1", 5)
    goose2 = HonkGoose("Test2", 6)
    gc.append(goose1)
    gc[0] = goose2
    assert gc[0] == goose2


def test_goose_collection_delitem():
    gc = GooseCollection()
    goose = HonkGoose("Test", 5)
    gc.append(goose)
    del gc[0]
    assert len(gc) == 0


def test_goose_collection_len():
    gc = GooseCollection()
    gc.append(HonkGoose("Test", 5))
    assert len(gc) == 1


def test_goose_collection_repr():
    gc = GooseCollection()
    goose = HonkGoose("Test", 5)
    gc.append(goose)
    assert "GooseCollection" in repr(gc)


def test_goose_collection_iter():
    gc = GooseCollection()
    goose = HonkGoose("Test", 5)
    gc.append(goose)
    for g in gc:
        assert g == goose
