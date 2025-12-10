import pytest
from unittest.mock import patch, MagicMock

from src.casino import Casino, CasinoBets
from src.player import Player
from src.goose import Goose, HonkGoose, RichGoose, GooseCollection
from src.chip import ChipCollection


@pytest.fixture
def casino():
    chips = ChipCollection()
    casino = Casino(chips, seed=42)
    player = Player("TestPlayer", 100)
    goose = HonkGoose("TestGoose", 5)
    casino.add_player(player)
    casino.add_goose(goose)
    return casino


def test_casino_init_with_seed(casino):
    assert casino is not None


def test_casino_make_random_bet(casino):
    with patch('casino.random.choice') as mock_choice, patch('casino.random.randint') as mock_randint:
        mock_choice.side_effect = [casino.players[0], 'красное']
        mock_randint.return_value = 25
        casino.make_random_bet()
        assert "TestPlayer" in casino.bets
        assert casino.players[0].balance == 75


def test_casino_spin_wheel_zero(casino):
    with patch('casino.random.randint') as mock_randint:
        mock_randint.return_value = 0
        casino.bets.place_bet("TestPlayer", "зеро", 10)
        casino.players[0].balance -= 10
        casino.spin_wheel()
        assert casino.players[0].balance == 110


def test_casino_spin_wheel_win(casino):
    casino.bets.place_bet("TestPlayer", "зеро", 10)
    casino.players[0].balance -= 10
    with patch('casino.random.randint', return_value=0):
        casino.spin_wheel()
    assert casino.players[0].balance == 110


def test_casino_perform_step_with_players(casino):
    casino.players.append(Player("TestPlayer", 100))
    casino.geese.append(HonkGoose("TestGoose", 5))
    casino.bets.place_bet("TestPlayer", "красное", 10)
    casino.players[0].balance -= 10
    casino.perform_step()


def test_casino_add_player(casino):
    initial_len = len(casino.players)
    new_player = Player("NewPlayer", 50)
    casino.add_player(new_player)
    assert len(casino.players) == initial_len + 1
    assert new_player in casino.players


def test_casino_add_goose(casino):
    initial_len = len(casino.geese)
    new_goose = RichGoose("NewGoose", 3)
    casino.add_goose(new_goose)
    assert len(casino.geese) == initial_len + 1
    assert new_goose in casino.geese


def test_casino_goose_steal(casino):
    casino.players.append(Player("TestPlayer", 100))
    casino.geese.append(HonkGoose("TestGoose", 5))
    initial_balance = casino.players[0].balance
    casino.goose_steal()
    assert casino.players[0].balance < initial_balance


def test_casino_goose_action_honk(casino):
    casino.geese.append(HonkGoose("TestGoose", 5))
    casino.goose_action()


def test_casino_add_random_entity_player(casino):
    with patch('casino.random.random', return_value=0.1), patch('casino.random.choice', return_value="Алекс"), patch('casino.random.randint', return_value=100):
        initial_players = len(casino.players)
        casino.add_random_entity()
        assert len(casino.players) == initial_players + 1


def test_casino_add_random_entity_goose(casino):
    with patch('casino.random.random', return_value=0.9), patch('casino.random.choice', return_value="Гусь-Сигма"), patch('casino.random.randint', return_value=5):
        initial_geese = len(casino.geese)
        casino.add_random_entity()
        assert len(casino.geese) == initial_geese + 1
