import logging
import random
import time
from collections import UserDict

from player import PlayerCollection, Player
from goose import GooseCollection, Goose, HonkGoose, RichGoose
from chip import ChipCollection

logger = logging.getLogger()


class Casino:
    def __init__(self, chips: ChipCollection, seed: int | None = None):
        self.players = PlayerCollection()
        self.geese = GooseCollection()
        self.bets = CasinoBets()
        self.chips = chips

        self.player_names = ["Алекс", "Борис", "Виктор", "Григорий", "Дмитрий"]
        self.goose_names = ["Гусь-Сигма", "Гусь-Свэг", "Гусь-Проказник", "Гусь-Воришка", "Гусь-Шутник"]

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
        self.players.append(player)

    def add_goose(self, goose: Goose):
        self.geese.append(goose)

    def perform_step(self) -> None:
        """
        Выполняет один шаг симуляции: генерирует случайное значение,
        обновляет балансы игроков (пример: вычитает ставку или добавляет выигрыш)
        и логирует результат.
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
        time.sleep(1.5)

    def make_random_bet(self):
        """Устанавливает случайную ставку для случайного игрока."""
        available_players = [p for p in self.players if p.name not in self.bets]
        player = random.choice(available_players)
        bet_type = random.choices(['красное', 'чёрное', 'зеро'], weights=[0.49, 0.48, 0.03])[0]
        amount = random.randint(int(player.balance / 4), int(player.balance))

        self.bets.place_bet(player.name, bet_type, amount)
        player.balance -= amount  # Снимаем ставку сразу

        logger.info(
            "\033[94m🎰 Игрок %s сделал ставку: %d на %s. Баланс после ставки: %d\033[0m",
            player.name, amount, bet_type, player.balance
        )

    def spin_wheel(self):
        """Генерирует случайное значение от 0 до 36, имитируя вращение колеса казино."""
        logger.info("\033[93m🎡 Колёсико вращается...\033[0m")
        time.sleep(1.0)

        number = random.randint(0, 36)
        red_numbers = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
        if number == 0:
            winning_color = 'зеро'
        elif number in red_numbers:
            winning_color = 'красное'
        else:
            winning_color = 'чёрное'
        logger.info("\033[93m🎲 Выпало: %d (%s)\033[0m", number, winning_color)

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
            color = "\033[92m" if bet_type == winning_color else "\033[91m"
            logger.info(
                f"{color}💰 Игрок %s поставил %d на %s и %s. Новый баланс: %d\033[0m",
                player.name, amount, bet_type, result, player.balance
            )

        self.bets.clear_bets()

    def goose_steal(self):
        """Случайный гусь крадёт деньги у случайного игрока."""
        if len(self.geese) == 0 or len(self.players) == 0:
            return

        goose = random.choice(self.geese)
        player = random.choice(self.players)
        steal_amount = random.randint(1, player.balance // 2)

        player.balance -= steal_amount
        logger.info(
            "\033[95m🦢 Гусь %s украл у игрока %s %d грязных бумажек! Новый баланс игрока: %d\033[0m",
            goose.name, player.name, steal_amount, player.balance
        )

    def goose_action(self):
        """Случайный гусь выполняет своё действие."""
        goose = random.choice(self.geese)
        if isinstance(goose, HonkGoose):
            logger.info("\033[95m🦢 Гусь %s жёстко орёт!\033[0m", goose.name)
            goose()
        if isinstance(goose, RichGoose):
            money = goose.spend()
            for player in self.players:
                player.balance += money
            logger.info("\033[95m🦢 Гусь %s раздаёт челяди деньги! Все игроки получают по %d\033[0m", goose.name, money)

    def add_random_entity(self):
        """Добавляет случайного игрока или гуся в казино, используя формулу для баланса."""
        prob_player = (len(self.geese) + 1) / (len(self.players) + len(self.geese) + 2)
        if random.random() < prob_player:
            balances = [50, 100, 150, 200, 300, 500]
            weights = [0.3, 0.25, 0.15, 0.15, 0.1, 0.05]
            balance = random.choices(balances, weights=weights)[0]
            name = random.choice(self.player_names)
            new_player = Player(
                name=name,
                balance=balance
            )
            del name
            self.add_player(new_player)
            logger.info("\033[96m➕  В казик пришёл новый игрок: %s с валютой в количестве %d\033[0m", new_player.name, new_player.balance)
        else:
            name = random.choice(self.goose_names)
            goose_classes = [HonkGoose, RichGoose]

            count_honk = sum(1 for g in self.geese if isinstance(g, HonkGoose))
            count_rich = sum(1 for g in self.geese if isinstance(g, RichGoose))

            weights = [1 / (count_honk + 1), 1 / (count_rich + 1)]
            GooseClass = random.choices(goose_classes, weights=weights)[0]
            new_goose = GooseClass(
                name=name,
                honk_volume=random.randint(1, 10)
            )
            del name
            self.add_goose(new_goose)
            logger.info("\033[96m➕  В казик залетел новый гусь по имени %s\033[0m", new_goose.name)

    def set_events_weight(self, weights: dict[str, float]):
        """
        Устанавливает вес для события.
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
        self[player_name] = {'type': bet_type, 'amount': amount}

    def clear_bets(self):
        """Очищает все ставки."""
        self.data.clear()
        logger.debug("All bets have been cleared.")
