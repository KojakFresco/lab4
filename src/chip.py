class Chip:
    def __init__(self, color: str, value: int):
        self.color = color
        self.value = value

    def __repr__(self) -> str:
        return f"Chip(value={self.value})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Chip):
            return self.color == other.color and self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def __add__(self, other):
        if isinstance(other, Chip):
            return Chip(self.color, self.value + other.value)
        return NotImplemented


class ChipCollection:
    def __init__(self, chips: list[Chip] | None = None):
        self._chips = list(chips) if chips else []

    def __getitem__(self, index):
        return self._chips[index]

    def __setitem__(self, index, value: Chip):
        self._chips[index] = value

    def __delitem__(self, index):
        del self._chips[index]

    def __len__(self) -> int:
        return len(self._chips)

    def __iter__(self):
        return iter(self._chips)

    def append(self, chip: Chip) -> None:
        self._chips.append(chip)

    def remove(self, chip: Chip) -> None:
        self._chips.remove(chip)

    def __contains__(self, chip: Chip) -> bool:
        return chip in self._chips

    def __repr__(self) -> str:
        return f"ChipCollection({self._chips})"
