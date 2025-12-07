import logging.config
from config import LOGGING_CONFIG
from casino import Casino
from chip import ChipCollection, Chip

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def run_simulation(steps: int = 20, seed: int | None = None):
    """
    Функция для запуска симуляции с заданным количеством шагов и необязательным сидом для генератора случайных чисел.

    :param steps: Количество шагов симуляции (по умолчанию 20)
    :param seed: Сид для генератора случайных чисел (по умолчанию None)
    :return: Данная функция ничего не возвращает
    """

    chips = ChipCollection()
    chips.append(Chip("Белый", 1))
    chips.append(Chip("Красный", 5))
    chips.append(Chip("Зелёный", 25))
    chips.append(Chip("Чёрный", 100))

    casino = Casino(chips, seed)
    for step in range(steps):
        casino.perform_step()