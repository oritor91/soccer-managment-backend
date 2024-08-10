from typing import List, Dict
import random
from app.database import DbConnection
from pymongo.results import UpdateResult
from app.models import Player, PlayerBase, Game, GameBase
from collections import defaultdict
from bson import ObjectId


class AppController:
    """
    The controller class for managing players and games in the soccer management app.
    """

    def __init__(self):
        """
        Initializes the AppController class.
        """
        self.db = DbConnection()
    
    def create_player(self, player: PlayerBase) -> bool:
        """
        Creates a new player and saves it to the database.

        Args:
            player (Player): The player object to be created.

        Returns:
            bool: True if the player is created successfully, False otherwise.
        """
        try:
            player_dict = player.model_dump()
            res = self.db.players_db.insert_one(player_dict)
            return True
        except Exception as e:
            print(e)
            return False
    
    def get_player_by_id(self, id: ObjectId) -> Player:
        """
        Retrieves a player from the database based on the player's ID.

        Args:
            id (str): The ID of the player.

        Returns:
            Player: The player object.
        """
        query = {"_id": id}
        player = self.db.players_db.find_one(query)
        return Player(**player)
    
    def get_player_by_name(self, name: str) -> List[Player]:
        """
        Retrieves players from the database based on the player's name.

        Args:
            name (str): The name of the player.

        Returns:
            List[Player]: A list of player objects.
        """
        query = {"name": name}
        players = self.db.players_db.find(query)
        return [Player(**player) for player in players]
    
    def get_all_players(self) -> List[Player]:
        """
        Retrieves all players from the database.

        Returns:
            List[Player]: A list of player objects.
        """
        players = self.db.players_db.find()
        res = [Player(**player) for player in players]
        return res

    def delete_player(self, player_id: str) -> bool:
        """
        Deletes a player from the database.

        Args:
            player (Player): The player object to be deleted.

        Returns:
            bool: True if the player is deleted successfully, False otherwise.
        """
        query = {"_id": ObjectId(player_id)}
        self.db.players_db.delete_one(query)
        return True
    
    def update_player(self, player_id: str, player: PlayerBase) -> bool:
        """
        Updates a player in the database.

        Args:
            player (Player): The player object to be updated.

        Returns:
            bool: True if the player is updated successfully, False otherwise.

        Raises:
            Exception: If the player is not found or failed to update.
        """
        query = {"_id": ObjectId(player_id)}
        player_dict = player.model_dump()
        result: UpdateResult = self.db.players_db.update_one(query, {"$set": player_dict})
        if result.modified_count > 0:
            return True
        else:
            raise Exception(f"Player not found -> {result.raw_result}")
    
    def create_game(self, game: GameBase) -> Game:
        """
        Creates a new game and saves it to the database.

        Args:
            game (Game): The game object to be created.

        Returns:
            dict: A dictionary containing the ID of the inserted game.

        Raises:
            Exception: If the game creation failed.
        """
        # Insert the game into the MongoDB collection
        game_dict = game.model_dump()
        result = self.db.games_db.insert_one(game_dict)
        if result.inserted_id:
            return Game(**game_dict)
        else:
            raise Exception("Game creation failed")

    def get_games(self) -> List[Game]:
        """
        Retrieves all games from the database.

        Returns:
            List[Game]: A list of game objects.
        """
        # Fetch all games from the MongoDB collection
        games_cursor = self.db.games_db.find()
        games = []
        for db_game in games_cursor:
            db_game: dict
            game = Game(**db_game)
            games.append(game)
        return games

    def update_game(self, game_id: str, game: Game):
        """
        Updates a game in the database.

        Args:
            game (Game): The game object to be updated.

        Returns:
            dict: A dictionary containing a message indicating the success of the update.

        Raises:
            Exception: If the game is not found.
        """
        print(game_id)
        query = {"_id": ObjectId(game_id)}
        game_dict = game.model_dump()
        print(game_dict)
        result: UpdateResult = self.db.games_db.update_one(query, {"$set": game_dict})
        if result.modified_count > 0:
            return True
        else:
            raise Exception("Game not found")

    def delete_game(self, game_id: str):
        """
        Deletes a game from the database.

        Args:
            game (Game): The game object to be deleted.

        Returns:
            dict: A dictionary containing a message indicating the success of the deletion.

        Raises:
            Exception: If the game is not found.
        """
        result = self.db.games_db.delete_one({"_id": ObjectId(game_id)})
        if result.deleted_count:
            return {"message": "Game deleted successfully"}
        else:
            raise Exception("Game not found")
    
    def sort_groups(self, game_id: str) -> Dict:
        """
        Sorts players into groups based on skill level and position.

        Args:
            game_id (str): The ID of the game.

        Returns:
            dict: A dictionary containing three groups of players.

        Raises:
            Exception: If the game is not found.
        """
        game_dict: dict = self.db.games_db.find_one({"_id": game_id})
        if not game_dict:
            raise Exception("Game not found")
        game_dict.pop("_id")
        game = Game(**game_dict)
        players = game.players
        # Example: Sort players based on skill level and divide into two groups
        return self.sort_players_into_groups(players)
        
    @staticmethod
    def sort_players_into_groups(players: List[Player]) -> Dict:
        """
        Sorts players into groups based on skill level and position.

        Args:
            players (List[Player]): A list of player objects.

        Returns:
            dict: A dictionary containing three groups of players.
        """
        # Step 1: Sort players by skill level in descending order
        random.shuffle(players)
        sorted_players = sorted(players, key=lambda x: x.skill_level, reverse=True)
        
        # Step 2: Group players by position
        position_groups = defaultdict(list)
        for player in sorted_players:
            position_groups[player.position].append(player)

        # Step 3: Distribute players into three groups
        group_a = []
        group_b = []
        group_c = []

        # Alternate adding players from each position group to the groups
        group_selector = 0  # This will cycle through 0, 1, 2 for group A, B, C
        for position, players in position_groups.items():
            for player in players:
                if group_selector == 0:
                    group_a.append(player)
                elif group_selector == 1:
                    group_b.append(player)
                else:
                    group_c.append(player)
                group_selector = (group_selector + 1) % 3
        # Print the groups for deubgging purposes
        average_a = sum([player.skill_level for player in group_a]) / len(group_a)
        print(f"Average skill level a: {average_a}")
        average_b = sum([player.skill_level for player in group_b]) / len(group_b)
        print(f"Average skill level b: {average_b}")
        average_c = sum([player.skill_level for player in group_c]) / len(group_c)
        print(f"Average skill level c: {average_c}")
        return {
            "group_a": group_a,
            "group_b": group_b,
            "group_c": group_c
        }
    
    def save_sorted_groups(self, game_id: str, sorted_groups: Dict):
        """
        Saves the sorted groups for a game.

        Args:
            game_id (str): The ID of the game.
            sorted_groups (Dict): A dictionary containing the sorted groups.

        Returns:
            dict: A dictionary containing a message indicating the success of the operation.

        Raises:
            Exception: If the game is not found.
        """
        game_dict: dict = self.db.games_db.find_one({"_id": game_id})
        if not game_dict:
            raise Exception("Game not found")
        game_dict.pop("_id")
        game = Game(**game_dict)
        game.sorted_groups = sorted_groups["sortedGroups"]
        game_dict = game.model_dump()
        result = self.db.games_db.update_one({"_id": game_id}, {"$set": game_dict})
        if result.modified_count:
            return {"message": "Sorted groups saved successfully"}
        else:
            raise Exception("Failed to save sorted groups")
