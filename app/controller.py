from typing import List, Dict
import random
from app.database import DbConnection
from app.models import Player, PlayerUpdateRequest, Game
from collections import defaultdict


class AppController:
    """
    The controller class for managing players and games in the soccer management app.
    """

    def __init__(self):
        """
        Initializes the AppController class.
        """
        self.db = DbConnection()
    
    def create_player(self, player: Player) -> bool:
        """
        Creates a new player and saves it to the database.

        Args:
            player (Player): The player object to be created.

        Returns:
            bool: True if the player is created successfully, False otherwise.
        """
        try:
            player_dict = player.model_dump()
            player_dict["_id"] = player.id
            self.db.players_db.insert_one(player_dict)
            return True
        except Exception as e:
            print(e)
            return False
    
    def get_player_by_id(self, id: str) -> Player:
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
        return [Player(**player) for player in players]

    def delete_player(self, player: Player) -> bool:
        """
        Deletes a player from the database.

        Args:
            player (Player): The player object to be deleted.

        Returns:
            bool: True if the player is deleted successfully, False otherwise.
        """
        query = {"_id": player.id}
        self.db.players_db.delete_one(query)
        return True
    
    def update_player(self, player_update: PlayerUpdateRequest) -> bool:
        """
        Updates a player in the database.

        Args:
            player_update (PlayerUpdateRequest): The player update request object.

        Returns:
            bool: True if the player is updated successfully, False otherwise.

        Raises:
            Exception: If the player is not found or failed to update.
        """
        old_player = player_update.old
        new_player = player_update.new
        existing_player = self.db.players_db.find_one({"_id": old_player.id})
        if existing_player:
            print(f"Player found: {existing_player}")
            new_player_dict = new_player.model_dump()
            new_player_dict["_id"] = new_player.id
            update_result = self.db.players_db.update_one(
                {"_id": old_player.id},
                {"$set": new_player_dict}
            )
            if update_result.modified_count == 1:
                return True
            else:
                raise Exception("Failed to update player.")
        else:
            return False
    
    def create_game(self, game: Game):
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
        game_dict["_id"] = game.id
        result = self.db.games_db.insert_one(game_dict)
        if result.inserted_id:
            return {"id": str(result.inserted_id)}
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
            db_game.pop("_id")
            players = [Player(**player) for player in db_game.get("players")]
            game = Game(
                date=db_game.get("date"),
                time=db_game.get("time"),
                players=players,
                location=db_game.get("location")
            )
            games.append(game)
        return games

    def update_game(self, game: Game):
        """
        Updates a game in the database.

        Args:
            game (Game): The game object to be updated.

        Returns:
            dict: A dictionary containing a message indicating the success of the update.

        Raises:
            Exception: If the game is not found.
        """
        game_dict = game.model_dump()
        # Update the game in the MongoDB collection
        result = self.db.games_db.update_one({"_id": game.id}, {"$set": game_dict})
        if result.matched_count:
            return {"message": "Game updated successfully"}
        else:
            raise Exception("Game not found")

    def delete_game(self, game: Game):
        """
        Deletes a game from the database.

        Args:
            game (Game): The game object to be deleted.

        Returns:
            dict: A dictionary containing a message indicating the success of the deletion.

        Raises:
            Exception: If the game is not found.
        """
        result = self.db.games_db.delete_one({"_id": game.id})
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
        print("Groups:")
        print("Group A:")
        print(",".join([player.name for player in group_a]))
        print("Group B:")
        print(",".join([player.name for player in group_b]))
        print("Group C:")
        print(",".join([player.name for player in group_c]))
        return {
            "group_a": group_a,
            "group_b": group_b,
            "group_c": group_c
        }