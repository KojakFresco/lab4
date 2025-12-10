import logging
import random
import time
from collections import UserDict
from colorama import init, Fore

from player import PlayerCollection, Player
from goose import GooseCollection, Goose, HonkGoose, RichGoose
from chip import ChipCollection

init(autoreset=True)

logger = logging.getLogger()


class Casino:
    def __init__(self, chips: ChipCollection, seed: int | None = None):
        self.players = PlayerCollection()
        self.geese = GooseCollection()
        self.bets = CasinoBets()
        self.chips = chips

        self.player_names = ["Алекс", "Борис", "Виктор", "Григорий", "Дмитрий"]
        self.goose_names = ["Сигма", "Крутой", "Проказник", "Воришка", "Шутник"]

        self.events = {
            "player_bet": self.make_random_bet,
            "spin_wheel": self.spin_wheel,
            "goose_steal": self.goose_steal,
            "new_entity": self.add_random_entity,
            "goose_action": self.goose_action
        }
        self.event_weights = {
            "player_bet": 0.0,
            "spin_wheel": 0.0,
            "goose_steal": 0.0,
            "new_entity": 1.0,
            "goose_action": 0.0
        }
        if seed is not None:
            random.seed(seed)

    def add_player(self, player: Player):
        """
        Добавляет нового игрока в казино.

        :param player: Объект игрока, который будет добавлен.
        """
        self.players.append(player)

    def add_goose(self, goose: Goose):
        """
        Добавляет нового гуся в казино.

        :param goose: Объект гуся, который будет добавлен.
        """
        self.geese.append(goose)

    def perform_step(self) -> None:
        """
        Выполняет один шаг симуляции, выбирая случайное событие на основе весов.

        Событие может быть ставкой игрока, вращением колеса, кражей гуся, добавлением новой сущности
        или действием гуся. Вес событий корректируется динамически.
        """
        if len(self.players):
            weight_bets = ((len(self.bets)) / len(self.players)) ** 0.5
            self.set_events_weight({"player_bet": 1 - weight_bets,
                                    "spin_wheel": weight_bets})

        if len(self.geese) and len(self.players):
            weight_goose = (sum(p.balance for p in self.players) / 300.0 / len(self.players)) ** 0.5
            self.set_events_weight({"goose_steal": weight_goose,
                                    "goose_action": weight_goose})

        weight_entity = ((10 - len(self.players) - len(self.geese)) / 10.0) ** 2 * 2
        self.event_weights["new_entity"] = weight_entity

        weights = [self.event_weights[k] for k in self.events.keys()]
        event = random.choices(list(self.events.keys()), weights=weights)[0]
        self.events[event]()
        time.sleep(2)

    def make_random_bet(self):
        """
        Устанавливает случайную ставку для случайного игрока.

        Ставка выбирается случайным образом из доступных игроков, которые ещё не сделали ставку.
        """
        available_players = [p for p in self.players if p.name not in self.bets]
        player = random.choice(available_players)
        bet_type = random.choices(['красное', 'чёрное', 'зеро'], weights=[0.47, 0.48, 0.05])[0]
        if player.balance < 1: amount = player.balance
        else: amount = random.randint(player.balance // 4 + 1, player.balance)

        self.bets.place_bet(player.name, bet_type, amount)
        player.balance -= amount  # Снимаем ставку сразу

        logger.info(
            Fore.BLUE + "🎰 Игрок %s сделал ставку: %d на %s. Баланс после ставки: %d",
            player.name, amount, bet_type, player.balance
        )

    def spin_wheel(self):
        """
        Генерирует случайное значение от 0 до 36, имитируя вращение колеса казино.

        Определяет выигрышный цвет (красное, чёрное или зеро) и обновляет баланс игроков
        в зависимости от их ставок.
        """
        logger.info(Fore.LIGHTYELLOW_EX + "🎡 Колёсико вращается...")
        time.sleep(1.0)

        number = random.randint(0, 36)
        red_numbers = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
        if number == 0:
            winning_color = 'зеро'
        elif number in red_numbers:
            winning_color = 'красное'
        else:
            winning_color = 'чёрное'
        logger.info(Fore.LIGHTYELLOW_EX + "🎲 Выпало: %d (%s)", number, winning_color)

        for player_name, bet_info in self.bets.items():
            bet_type = bet_info['type']
            amount = bet_info['amount']
            player = self.players[player_name]
            if player is None:
                continue

            if bet_type == winning_color:
                player.balance += amount * 2
                result = "ВЫИГРАЛ"
            else:
                result = "ПРОИГРАЛ"
            color = Fore.GREEN if bet_type == winning_color else Fore.RED
            logger.info(
                color + "💰 Игрок %s поставил %d на %s и %s. Новый баланс: %d",
                player.name, amount, bet_type, result, player.balance
            )

        self.bets.clear_bets()

    def goose_steal(self):
        """
        Случайный гусь крадёт деньги у случайного игрока.
        """
        if len(self.geese) == 0 or len(self.players) == 0:
            return

        goose = random.choice(self.geese)
        player = random.choice([p for p in self.players if p.balance > 0])
        if player.balance // 2 > 1: steal_amount = random.randint(1, player.balance // 2)
        else: steal_amount = 1

        player.balance -= steal_amount
        logger.info(
            Fore.MAGENTA + "🦢 Гусь %s украл у игрока %s %d грязных бумажек! Новый баланс игрока: %d",
            goose.name, player.name, steal_amount, player.balance
        )

    def goose_action(self):
        """
        Случайный гусь выполняет своё действие.

        Если гусь является HonkGoose, он издаёт громкий крик. Если это RichGoose, он раздаёт
        деньги всем игрокам.
        """
        goose = random.choice(self.geese)
        if isinstance(goose, HonkGoose):
            logger.info(Fore.MAGENTA + "🦢 Гусь %s жёстко орёт!", goose.name)
            goose()
        if isinstance(goose, RichGoose):
            money = goose.spend()
            for player in self.players:
                player.balance += money
            logger.info(Fore.MAGENTA + "🦢 Гусь %s раздаёт челяди деньги! Все игроки получают по %d", goose.name, money)

    def add_random_entity(self):
        """
        Добавляет случайного игрока или гуся в казино.

        Используется формула для определения вероятности добавления игрока или гуся.
        Если добавляется гусь, его тип выбирается с учётом текущего баланса типов гусей.
        """
        prob_player = (len(self.geese) + 1) / (len(self.players) + len(self.geese) + 2)
        if (random.random() < prob_player and len(self.player_names) > 0) or len(self.goose_names) == 0:
            balances = [50, 100, 150, 200, 300, 500]
            weights = [0.3, 0.25, 0.15, 0.15, 0.1, 0.05]
            balance = random.choices(balances, weights=weights)[0]
            name = random.choice(self.player_names)
            new_player = Player(
                name=name,
                balance=balance
            )
            self.player_names.remove(name)
            self.add_player(new_player)
            logger.info(Fore.CYAN + "➕ В казик пришёл новый игрок: %s с валютой в количестве %d", new_player.name, new_player.balance)
        else:
            name = random.choice(self.goose_names)
            goose_classes = [HonkGoose, RichGoose]

            count_honk = sum(1 for g in self.geese if isinstance(g, HonkGoose))
            count_rich = sum(1 for g in self.geese if isinstance(g, RichGoose))

            weights = [1 / (count_honk + 1), 1 / (count_rich + 1)]
            goose_class = random.choices(goose_classes, weights=weights)[0]
            new_goose = goose_class(
                name=name,
                honk_volume=random.randint(1, 10)
            )
            self.goose_names.remove(name)
            self.add_goose(new_goose)
            logger.info(Fore.CYAN + "➕ В казик залетел новый гусь по имени %s", new_goose.name)

    def set_events_weight(self, weights: dict[str, float]):
        """
        Устанавливает веса для событий симуляции.

        :param weights: Словарь, где ключ — название события, а значение — его вес.
        """
        for event, weight in weights.items():
            self.event_weights[event] = weight

        # other_total = sum(v for k, v in self.event_weights.items() if k != event_name)
        # if other_total == 0:
        #     for k in self.event_weights:
        #         if k != event_name:
        #             self.event_weights[k] = (1 - weight) / (len(self.event_weights) - 1)
        # else:
        #     scale = (1 - weight) / other_total
        #     for k in self.event_weights:
        #         if k != event_name:
        #             self.event_weights[k] *= scale

        logger.debug("New events weights: %s", self.event_weights)


class CasinoBets(UserDict):
    """
    Словарная коллекция для хранения ставок игроков (player_name -> {'type': bet_type, 'amount': amount}).
    Логирует изменения ставок при установке значений.
    """

    def place_bet(self, player_name: str, bet_type: str, amount: int):
        """Устанавливает ставку игрока: тип ('чётное' или 'нечётное') и размер."""
        if player_name in self:
            return
        self[player_name] = {'type': bet_type, 'amount': amount}

    def clear_bets(self):
        """Очищает все ставки."""
        self.data.clear()
        logger.debug("All bets have been cleared.")
