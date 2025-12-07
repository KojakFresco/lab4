import logging
import random


class Goose:
    def __init__(self, name: str, honk_volume: int = 1):
        self.name = name
        self.honk_volume = honk_volume

class RichGoose(Goose):
    def spend(self):
        return random.randint(1, 100)

class HonkGoose(Goose):
    def __call__(self):
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

    def append(self, goose: Goose) -> None:
        self._geese.append(goose)