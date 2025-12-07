class Player:
    def __init__(self, name: str, balance: float):
        self.name = name
        self.balance = balance

    def __repr__(self):
        return f"Player(name={self.name}, balance={self.balance})"

    def update_balance(self, amount: float) -> None:
        self.balance += amount


class PlayerCollection:
    def __init__(self):
        self._players = []

    def __getitem__(self, index):
        if isinstance(index, str):
            return self.get_player_by_name(index)
        return self._players[index]

    def __setitem__(self, index, value):
        self._players[index] = value

    def __delitem__(self, index):
        del self._players[index]

    def __len__(self):
        return len(self._players)

    def append(self, player: Player) -> None:
        self._players.append(player)

    def get_player_by_name(self, name: str) -> Player | None:
        for player in self._players:
            if player.name == name:
                return player
        return None