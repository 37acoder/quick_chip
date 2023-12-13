from abc import abstractmethod
from dataclasses import dataclass
import datetime
from models.core import User, Game, UserGameInfo


class Player:
    def __init__(self, user: User, user_game_info: UserGameInfo) -> None:
        self.user_model = user
        self.user_game_info_model = user_game_info

    @property
    def name(self) -> str:
        return self.user_model.username

    @property
    def deposit(self):
        return self.user_game_info_model.balance

    @staticmethod
    def get_related_game_by_user_id(user_id: int):
        # user_id related game in recent 1 day
        return (
            Game.select()
            .join(UserGameInfo, on=(Game._id == UserGameInfo.game_id))
            .where(
                UserGameInfo.user_id == user_id
                and (Game.created_at + datetime.timedelta(days=1))
                > datetime.datetime.now()
            )
        )


class GameBoard:
    def __init__(self, game_id: int) -> None:
        self.game_model: Game = Game.get_by_id(game_id)
        user_game_infos = self.game_model.ger_user_game_infos()
        user_game_info_id_map = {info.user_id: info for info in user_game_infos}
        user_ids = [info.user_id for info in user_game_infos]
        users = User.get_user_by_ids(user_ids)
        users_id_map = {user._id: user for user in users}
        self.user_id_map = users_id_map
        self.players = [
            Player(users_id_map[info.user_id], info)
            for info in user_game_info_id_map.values()
        ]
        self.players_map_by_name = {player.name: player for player in self.players}
        self.player_info_map_by_name = {
            player.name: player.user_game_info_model for player in self.players
        }
        self.owner = User.get_by_id(self.game_model.owner_id)
        self.records = []
        self.game_records = self.game_model.get_all_records()
        self.god = Player(User.get_user_by_username("god"), UserGameInfo())

    @property
    def player_number(self) -> int:
        return len(self.players)

    def transfer(self, from_player: Player, to_player: Player, amount: int) -> None:
        self.game_model.balance_transfer(
            from_player.user_model._id, to_player.user_model._id, amount
        )

    def balance_modify(self, user_id: int, amount: int) -> int:
        return self.game_model.balance_modify(user_id, amount).balance

    @staticmethod
    def start_new_game(
        owner_id: int, game_name: str, token=None, default_balance=0
    ) -> Game:
        if Game.get_game_by_name(game_name) is not None:
            raise Exception(f"Game {game_name} already exist")
        game = Game.create_game(
            game_name, owner_id, token, default_balance=default_balance
        )
        return game

    @staticmethod
    def join_game(
        player_id: int,
        game_name: str,
        token="",
    ) -> Game:
        game = Game.get_game_by_name(game_name)
        if game is None:
            raise Exception(f"Game {game_name} not exist")
        if game.token != token:
            raise Exception(f"Game {game_name} token not match")
        game.user_join_game(player_id)
        return game

    def get_game_record(self):
        return self.game_model.get_all_records()
