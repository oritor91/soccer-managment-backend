from typing import List, Dict
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import Player, Game, PlayerBase, GameBase
from app.controller import AppController


class MyApp(FastAPI):
    """
    Custom FastAPI application class.
    """

    def __init__(self):
        super().__init__()
        self.controller = AppController()


app = MyApp()


@app.post("/player")
async def create_player(player: PlayerBase) -> bool:
    """
    Create a new player.

    Args:
        player (Player): The player object to create.

    Returns:
        bool: True if the player is created successfully, False otherwise.
    """
    return app.controller.create_player(player)


@app.put("/player/{player_id}")
async def update_player(player_id: str, player: PlayerBase) -> bool:
    """
    Update an existing player.

    Args:
        player_update (PlayerUpdateRequest): The player update request object.

    Returns:
        bool: True if the player is updated successfully, False otherwise.

    Raises:
        HTTPException: If the player is not found.
        HTTPException: If any other error occurs during the update process.
    """
    try:
        success = app.controller.update_player(player_id, player)
        if not success:
            raise HTTPException(status_code=404, detail="Player not found")
        return success
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/player")
async def read_players(player_name: str) -> List[Player]:
    """
    Get a list of players by name.

    Args:
        player_name (str): The name of the player.

    Returns:
        List[Player]: A list of players matching the given name.
    """
    return app.controller.get_player_by_name(player_name)


@app.delete("/player/{player_id}")
async def delete_player(player_id: str) -> bool:
    """
    Delete a player.

    Args:
        player (Player): The player object to delete.

    Returns:
        bool: True if the player is deleted successfully, False otherwise.
    """
    return app.controller.delete_player(player_id)


@app.get("/players")
async def read_all_players() -> List[Player]:
    """
    Get all players.

    Returns:
        List[Player]: A list of all players.
    """
    return app.controller.get_all_players()


@app.get("/games")
def read_games() -> List[Game]:
    """
    Get all games.

    Returns:
        List[Game]: A list of all games.
    """
    return app.controller.get_games()


@app.post("/game")
def create_game(game: GameBase) -> Game:
    """
    Create a new game.

    Args:
        game (Game): The game object to create.
    """
    return app.controller.create_game(game)


@app.put("/game/{game_id}")
def update_game(game_id: str, game: Game):
    """
    Update an existing game.

    Args:
        game (Game): The game object to update.
    """
    app.controller.update_game(game_id, game)


@app.delete("/game/{game_id}")
def delete_game(game_id: str):
    """
    Delete a game.

    Args:
        game (Game): The game object to delete.
    """
    app.controller.delete_game(game_id)


@app.post("/game/{game_id}/sort-groups")
def sort_groups(game_id: str) -> Dict[str, List[Player]]:
    """
    Sort groups for a game.

    Args:
        game_id (str): The ID of the game.

    Returns:
        Dict[str, List[Player]]: A dictionary containing the sorted groups.
    """
    return app.controller.sort_groups(game_id)

@app.put("/game/{game_id}/save-groups")
def save_sorted_groups(game_id: str, sorted_groups: Dict[str, Dict[str, List[Player]]]):
    """
    Sort groups for a game.

    Args:
        game_id (str): The ID of the game.

    Returns:
        Dict[str, List[Player]]: A dictionary containing the sorted groups.
    """
    app.controller.save_sorted_groups(game_id, sorted_groups)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Adjust this based on your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)