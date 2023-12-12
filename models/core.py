from dataclasses import dataclass, asdict
import datetime
import json
from typing import List
import dacite
from peewee import Model, CharField, DateTimeField, IntegerField, TextField, AutoField
from models.db import mysql_db


class ModelException(Exception):
    pass


class User(Model):
    _id = AutoField(primary_key=True, unique=True)
    username = CharField()
    password = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.create_at = datetime.datetime.now()
        return super(User, self).save(*args, **kwargs)

    class Meta:
        database = mysql_db

    def __str__(self) -> str:
        return f"<User {self.username}>"

    def is_out_date(self):
        if self.created_at + datetime.timedelta(days=1) < datetime.datetime.now():
            return True
        return False

    @staticmethod
    def init_user(username, password):
        user = User(username=username, password=password)
        user.save()

    @staticmethod
    def get_user_by_username(username=None):
        return User.get_or_none(username=username)


class UserGameInfo(Model):
    _id = AutoField(primary_key=True, unique=True)
    user_id = IntegerField(null=False)
    game_id = IntegerField(null=False)
    balance = IntegerField(null=False, default=0)
    created_at = DateTimeField(default=datetime.datetime.now)
    modify_at = DateTimeField

    def save(self, *args, **kwargs):
        self.modify_at = datetime.datetime.now()
        return super(UserGameInfo, self).save(*args, **kwargs)

    class Meta:
        database = mysql_db


@dataclass
class GameData:
    Records: List
        
class GameBoard(Model):
    _id = AutoField(primary_key=True, unique=True)
    name = CharField(unique=True, null=False)
    owner_id = IntegerField(null=False)
    token = CharField(null=True)
    game_data = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    modify_at = DateTimeField

    def save(self, *args, **kwargs):
        self.modify_at = datetime.datetime.now()
        return super(GameBoard, self).save(*args, **kwargs)

    @property
    def data(self):
        json_data = json.loads(self.game_data)
        return dacite.from_dict(GameData, json_data)

    class Meta:
        database = mysql_db



    @staticmethod
    def create_game(name, owner_id, token=None):
        game = GameBoard(
            name=name,
            owner_id=owner_id,
            token=token,
            game_data=json.dumps(asdict(GameData(Records=[])))
        )
        game.save()
        return game

    def is_expired(self, now=None):
        if now is None:
            now = datetime.datetime.now()
        if self.created_at + datetime.timedelta(days=1) < now:
            return True
        return False

    def user_join_game(self, user_id: int, balance=0):
        if self.is_expired():
            raise ModelException("game is expired")

        user_game_info = UserGameInfo.get_or_none(user_id=user_id, game_id=self._id)
        if user_game_info is None:
            user_game_info = UserGameInfo(
                user_id=user_id, game_id=self._id, balance=balance
            )
            user_game_info.save()
        return user_game_info

    def balance_trancefer(self, from_user_id: int, to_user_id: int, amount: int):
        with mysql_db.atomic():
            from_user_game_info = UserGameInfo.get_or_none(
                user_id=from_user_id, game_id=self._id
            )
            to_user_game_info = UserGameInfo.get_or_none(
                user_id=to_user_id, game_id=self._id
            )
            if from_user_game_info is None or to_user_game_info is None:
                raise ModelException("user not join game")
            if from_user_game_info.balance < amount:
                raise ModelException("user balance not enough")
            from_user_game_info.balance -= amount
            to_user_game_info.balance += amount
            from_user_game_info.save()
            to_user_game_info.save()
            return from_user_game_info, to_user_game_info


# if tables not exist , create
if not mysql_db.table_exists("user"):
    mysql_db.create_tables([User])
if not mysql_db.table_exists("game"):
    mysql_db.create_tables([GameBoard])
if not mysql_db.table_exists("user_game_info"):
    mysql_db.create_tables([UserGameInfo])
