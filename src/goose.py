import logging
import random


class Goose:
    def __init__(self, name: str, honk_volume: int = 1):
        self.name = name
        self.honk_volume = honk_volume

    def __repr__(self):
        return f"Goose(name={self.name}, honk_volume={self.honk_volume})"

class RichGoose(Goose):
    def spend(self):
        """
        Генерирует случайную сумму денег, которую гусь может потратить.

        :return: Случайное целое число от 1 до 100.
        """
        return random.randint(1, 100)

class HonkGoose(Goose):
    def __call__(self):
        """
        Вызывает гуся, который издаёт звук "Га!" с громкостью, равной его параметру honk_volume.

        :return: Громкость крика гуся.
        """
        logging.getLogger(__name__).info("Га! " * int(self.honk_volume))
        return self.honk_volume

class GooseCollection:
    def __init__(self):
        self._geese = []

    def __getitem__(self, index):
        return self._geese[index]

    def __setitem__(self, index, value):
        self._geese[index] = value

    def __delitem__(self, index):
        del self._geese[index]

    def __len__(self):
        return len(self._geese)

    def __repr__(self):
        return f"GooseCollection({self._geese})"

    def append(self, goose: Goose) -> None:
        self._geese.append(goose)

    def clear(self) -> None:
        self._geese.clear()