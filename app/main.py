from typing import List, Dict
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import Player, PlayerUpdateRequest, Game
from app.controller import AppController


class MyApp(FastAPI):
    def __init__(self):
        super().__init__()
        self.controller = AppController()


app = MyApp()


@app.post("/player")
async def create_player(player: Player) -> bool:
    print(player)
    return app.controller.create_player(player)

@app.put("/player")
async def update_player(player_update: PlayerUpdateRequest) -> bool:
    try:
        print(f"Updating player: {player_update}")
        success = app.controller.update_player(player_update)
        if not success:
            raise HTTPException(status_code=404, detail="Player not found")
        return success
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player")
async def read_players(player_name: str) -> List[Player]:
    return app.controller.get_player_by_name(player_name)

@app.delete("/player")
async def delete_player(player: Player) -> bool:
    return app.controller.delete_player(player)

@app.get("/players")
async def read_players() -> List[Player]:
    return app.controller.get_all_players()

@app.get("/games")
def read_games() -> List[Game]:
    return app.controller.get_games()

@app.post("/game")
def create_game(game: Game):
    app.controller.create_game(game)

@app.put("/game")
def update_game(game: Game):
    app.controller.update_game(game)

@app.delete("/game")
def delete_game(game: Game):
    app.controller.delete_game(game)

@app.post("/games/{game_id}/sort-groups")
def sort_groups(game_id: str) -> Dict[str, List[Player]]:
    return app.controller.sort_groups(game_id)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Adjust this based on your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)