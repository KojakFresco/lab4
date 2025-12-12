import pytest
from src.player import Player, PsychoPlayer, PlayerCollection


def test_player_init():
    player = Player("Test", 100)
    assert player.name == "Test"
    assert player.balance == 100


def test_player_repr():
    player = Player("Test", 100)
    assert repr(player) == "Player(name=Test, balance=100)"


def test_player_update_balance():
    player = Player("Test", 100)
    player.update_balance(50)
    assert player.balance == 150


def test_psycho_player_init():
    psycho = PsychoPlayer("Test", 100)
    assert psycho.name == "Test"
    assert psycho.balance == 100
    assert psycho.psycho == 0.0


def test_psycho_player_update_psycho_win():
    psycho = PsychoPlayer("Test", 100)
    psycho.psycho = 0.2
    psycho.update_psycho(50)
    assert psycho.psycho == 0.0


def test_psycho_player_update_psycho_lose():
    psycho = PsychoPlayer("Test", 100)
    psycho.update_psycho(-50)
    assert psycho.psycho > 0.0


def test_player_collection_init():
    pc = PlayerCollection()
    assert len(pc) == 0


def test_player_eq():
    player1 = Player("Test", 100)
    player2 = Player("Test", 100)
    player3 = Player("Test", 200)
    assert player1 == player2
    assert player1 != player3


@pytest.fixture
def player_collection():
    collection = PlayerCollection()
    player1 = Player("Alice", 100)
    player2 = Player("Bob", 200)
    collection.append(player1)
    collection.append(player2)
    return collection


def test_player_collection_append(player_collection):
    assert len(player_collection) == 2
    assert Player("Alice", 100) in player_collection
    assert Player("Bob", 200) in player_collection


def test_player_collection_getitem_by_index(player_collection):
    assert player_collection[0].name == "Alice"
    assert player_collection[1].name == "Bob"


def test_player_collection_getitem_by_name(player_collection):
    assert player_collection["Alice"].name == "Alice"
    assert player_collection["Bob"].name == "Bob"


def test_player_collection_getitem_slice(player_collection):
    sliced = player_collection[0:2]
    assert len(sliced) == 2
    assert sliced[0].name == "Alice"


def test_player_collection_contains(player_collection):
    assert Player("Alice", 100) in player_collection
    assert Player("Charlie", 50) not in player_collection


def test_player_collection_get_player_by_name(player_collection):
    assert player_collection.get_player_by_name("Alice").name == "Alice"
    assert player_collection.get_player_by_name("Charlie") is None
