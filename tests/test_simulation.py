from unittest.mock import patch, MagicMock, ANY

from src.simulation import run_simulation


def test_run_simulation_calls_casino():
    with patch('src.simulation.Casino') as mock_casino_class:
        mock_casino = MagicMock()
        mock_casino_class.return_value = mock_casino
        run_simulation(steps=3, seed=42)

        assert mock_casino.perform_step.call_count == 3

        args, kwargs = mock_casino_class.call_args
        assert args[1] == 42
