import pytest
from app.controller import AppController
from app.models import Player, PlayerBase, Game, GameBase


def test_create_player():
    controller = AppController()
    player = PlayerBase(name="John Doe", phone_number="1234567890", position="ST", skill_level=5)
    succeeded, res = controller.create_player(player)
    my_player = Player(name="John Doe", phone_number="1234567890", position="CM", skill_level=1, _id=res.inserted_id) 
    controller.update_player(str(my_player.id), my_player)


def test_create_game():
    controller = AppController()
    game = GameBase(date="2022-12-25", time="12:00", location="Field 1")
    controller.create_game(game)


def test_update_game():
    controller = AppController()
    game = GameBase(date="2022-12-25", time="12:00", location="Field 1")
    create_game = controller.create_game(game)
    game = GameBase(date="2022-12-25", time="12:00", location="Field 2")
    controller.update_game(create_game.id, game)