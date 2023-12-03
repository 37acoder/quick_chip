from abc import abstractmethod
from datetime import datetime

class Player:
    def __init__(self, name: str, deposit: int = 0) -> None:
        self.name = name
        self.deposit = deposit


class Record:
    def __init__(self, t:datetime = None) -> None:
        self.time = t or datetime.now()

    @abstractmethod
    def content(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{self.time}: {self.content()}"


class TransferRecord(Record):
    def __init__(self, from_player: Player, to_player: Player, amount: int) -> None:
        super().__init__()
        self.from_player = from_player
        self.to_player = to_player
        self.amount = amount

    def content(self) -> str:
        return f"{self.from_player.name} pay {self.to_player.name} {self.amount}, balance {self.from_player.deposit}, {self.to_player.deposit}"


class Game:
    def __init__(self, players: list[Player], dealer: Player = None) -> None:
        self.players = players
        self.dealer = dealer or Player("Dealer")

        self.players_map_by_name = {player.name: player for player in self.all_player_including_dealder}
        self.records = []

    @property
    def all_player_including_dealder(self) -> list[Player]:
        return [self.dealer] + self.players 

    @property
    def player_number(self) -> int:
        return len(self.players)

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def transfer(self, from_player: Player, to_player: Player, amount: int) -> None:
        from_player.deposit -= amount
        to_player.deposit += amount
        self.add_record(TransferRecord(from_player, to_player, amount))

    def add_deposit_all_player(self, amount: int) -> int:
        total = 0
        for player in self.players:
            player.deposit += amount
            amount += total
            self.add_record(TransferRecord(self.dealer, player, amount))
        return total

    def dealer_collect_from_all_player(self, amount: int) -> None:
        for player in self.players:
            self.transfer(player, self.dealer, amount)
