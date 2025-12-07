import pytest

from src.player import Player, PlayerCollection
from src.chip import Chip, ChipCollection
from src.goose import Goose, HonkGoose, RichGoose, GooseCollection
from src.casino import CasinoBets


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


def test_chip_add():
    chip1 = Chip("red", 10)
    chip2 = Chip("blue", 20)
    result = chip1 + chip2
    assert result.value == 30
    assert isinstance(result, Chip)


def test_chip_init():
    chip = Chip("red", 10)
    assert chip.color == "red"
    assert chip.value == 10


def test_chip_repr():
    chip = Chip("blue", 20)
    assert repr(chip) == "Chip(value=20)"


def test_chip_eq():
    chip1 = Chip("green", 15)
    chip2 = Chip("green", 15)
    chip3 = Chip("yellow", 15)
    assert chip1 == chip2
    assert chip1 != chip3


def test_chip_hash():
    chip = Chip("purple", 25)
    assert isinstance(hash(chip), int)


@pytest.fixture
def chip_collection():
    collection = ChipCollection()
    chip1 = Chip("red", 5)
    chip2 = Chip("blue", 10)
    collection.append(chip1)
    collection.append(chip2)
    return collection


def test_chip_collection_append_and_len(chip_collection):
    assert len(chip_collection) == 2


def test_chip_collection_getitem(chip_collection):
    assert chip_collection[0].value == 5
    assert chip_collection[1].value == 10


def test_chip_collection_contains(chip_collection):
    assert Chip("red", 5) in chip_collection
    assert Chip("yellow", 20) not in chip_collection


def test_goose_creation():
    goose = Goose("TestGoose", 5)
    assert goose.name == "TestGoose"
    assert goose.honk_volume == 5


def test_honk_goose():
    goose = HonkGoose("HonkGoose", 3)
    assert isinstance(goose, Goose)


def test_rich_goose_spend():
    goose = RichGoose("RichGoose", 1)
    money = goose.spend()
    assert isinstance(money, int)
    assert money >= 1


@pytest.fixture
def casino_bets():
    return CasinoBets()


def test_casino_bets_place_bet(casino_bets):
    casino_bets.place_bet("Alice", "красное", 50)
    assert "Alice" in casino_bets
    assert casino_bets["Alice"]["type"] == "красное"
    assert casino_bets["Alice"]["amount"] == 50


def test_casino_bets_place_bet_twice_fails(casino_bets):
    casino_bets.place_bet("Alice", "красное", 50)
    casino_bets.place_bet("Alice", "чёрное", 30)  # Должен игнорировать
    assert casino_bets["Alice"]["type"] == "красное"  # Не изменилось


def test_player_init():
    player = Player("Alice", 100)
    assert player.name == "Alice"
    assert player.balance == 100


def test_player_repr():
    player = Player("Bob", 200)
    assert repr(player) == "Player(name=Bob, balance=200)"


def test_player_eq():
    player1 = Player("Alice", 100)
    player2 = Player("Alice", 100)
    player3 = Player("Bob", 100)
    assert player1 == player2
    assert player1 != player3


def test_honk_goose_init():
    goose = HonkGoose("HonkGoose", 3)
    assert goose.name == "HonkGoose"
    assert goose.honk_volume == 3


def test_rich_goose_init():
    goose = RichGoose("RichGoose", 1)
    assert goose.name == "RichGoose"
    assert goose.honk_volume == 1
