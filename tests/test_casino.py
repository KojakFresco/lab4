import pytest
from unittest.mock import patch, MagicMock

from src.casino import Casino, CasinoBets
from src.player import Player, PlayerCollection, PsychoPlayer
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


@pytest.fixture
def empty_casino():
    chips = ChipCollection()
    return Casino(chips, seed=42)


@pytest.fixture
def casino_bets():
    return CasinoBets()


def test_casino_init_with_seed(casino):
    assert casino is not None


def test_casino_make_random_bet(casino):
    with patch('src.casino.random.choice') as mock_choice, patch('src.casino.random.randint') as mock_randint:
        mock_choice.side_effect = [casino.players[0], 'красное']
        mock_randint.return_value = 25
        casino.make_random_bet()
        assert "TestPlayer" in casino.bets
        assert casino.players[0].balance == 75


@pytest.mark.parametrize("randint_value,expected_balance", [
    (0, 110),  # Win zero
    (2, 90),   # Lose black
])
def test_casino_spin_wheel(casino, randint_value, expected_balance):
    casino.bets.place_bet("TestPlayer", "зеро" if randint_value == 0 else "красное", 10)
    casino.players[0].balance -= 10
    with patch('src.casino.random.randint', return_value=randint_value):
        casino.spin_wheel()
    assert casino.players[0].balance == expected_balance


def test_casino_perform_step_with_players(empty_casino):
    empty_casino.players.append(Player("TestPlayer", 100))
    empty_casino.geese.append(HonkGoose("TestGoose", 5))
    with patch('src.casino.time.sleep'), patch('src.casino.random.choices', return_value=['player_bet']):
        empty_casino.perform_step()


def test_casino_evualuate_weights_no_players(empty_casino):
    empty_casino.evualuate_weights()


def test_casino_make_random_bet_low_balance(empty_casino):
    player = Player("TestPlayer", 0)
    empty_casino.add_player(player)
    with patch('src.casino.random.choice', return_value=player), patch('src.casino.random.choices', return_value=['красное']):
        empty_casino.make_random_bet()
        assert player.balance == 0


def test_casino_spin_wheel_player_none(empty_casino):
    empty_casino.bets.place_bet("NonExistent", "зеро", 10)
    with patch('src.casino.random.randint', return_value=0):
        empty_casino.spin_wheel()  # Should skip the None player


def test_casino_goose_steal(casino):
    initial_balance = casino.players[0].balance
    casino.goose_steal()
    assert casino.players[0].balance < initial_balance


def test_casino_goose_steal_no_entities(empty_casino):
    empty_casino.goose_steal()  # Should return early


@pytest.mark.parametrize("goose_type", [HonkGoose, RichGoose])
def test_casino_goose_action(empty_casino, goose_type):
    if goose_type == HonkGoose:
        goose = HonkGoose("TestGoose", 5)
    else:
        goose = RichGoose("TestGoose", 5)
    empty_casino.geese.append(goose)
    empty_casino.players.append(Player("TestPlayer", 100))
    with patch('src.casino.random.choice', return_value=goose):
        empty_casino.goose_action()  # Should not raise error


def test_casino_add_player(casino):
    initial_len = len(casino.players)
    new_player = Player("NewPlayer", 50)
    casino.add_player(new_player)
    assert len(casino.players) == initial_len + 1


def test_casino_add_goose(casino):
    initial_len = len(casino.geese)
    new_goose = RichGoose("NewGoose", 3)
    casino.add_goose(new_goose)
    assert len(casino.geese) == initial_len + 1


@pytest.mark.parametrize("random_value,name,entity_type", [
    (0.1, "Александр", "player"),
    (0.9, "Сигма", "goose"),
])
def test_casino_add_random_entity(empty_casino, random_value, name, entity_type):
    if entity_type == "player":
        choices_side_effect = [[100], [Player]]  # First for balances, second for player_classes
    else:
        choices_side_effect = [[HonkGoose]]  # For goose_classes
    with patch('src.casino.random.random', return_value=random_value), patch('src.casino.random.choice', return_value=name), patch('src.casino.random.choices', side_effect=choices_side_effect):
        initial_count = len(empty_casino.players) if entity_type == "player" else len(empty_casino.geese)
        empty_casino.add_random_entity()
        new_count = len(empty_casino.players) if entity_type == "player" else len(empty_casino.geese)
        assert new_count == initial_count + 1


@pytest.mark.parametrize("random_value,expected_players", [
    (0.3, 1),  # Suicide, len becomes 1
    (0.5, 1),  # Kill other, len becomes 1
])
def test_casino_kill_player(empty_casino, random_value, expected_players):
    psycho = PsychoPlayer("Psycho", 100)
    other = Player("Other", 50)
    empty_casino.add_player(psycho)
    empty_casino.add_player(other)
    with patch('src.casino.random.random', return_value=random_value), patch('src.casino.random.choice', return_value=other):
        empty_casino.kill_player(psycho)
        assert len(empty_casino.players) == expected_players


def test_casino_set_events_weight_debug(empty_casino):
    with patch('src.casino.logger') as mock_logger:
        empty_casino.set_events_weight({"player_bet": 0.5})
        mock_logger.debug.assert_called()


def test_casino_bets_place_bet(casino_bets):
    casino_bets.place_bet("Alice", "красное", 50)
    assert "Alice" in casino_bets
    assert casino_bets["Alice"]["type"] == "красное"
    assert casino_bets["Alice"]["amount"] == 50


def test_casino_bets_place_bet_twice_fails(casino_bets):
    casino_bets.place_bet("Alice", "красное", 50)
    casino_bets.place_bet("Alice", "чёрное", 30)  # Should ignore
    assert casino_bets["Alice"]["type"] == "красное"
