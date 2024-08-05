import os
from pymongo import MongoClient
from pymongo.collection import Collection

# MongoDB connection URI
USER_NAME = os.environ.get("MONGODB_USER")
PASSWORD = os.environ.get("MONGODB_PASSWORD")
MONGODB_URL = f"mongodb+srv://{USER_NAME}:{PASSWORD}@soccermanagementcluster.exqi9dy.mongodb.net/?retryWrites=true&w=majority&appName=SoccerManagementCluster"
SOCCER_MANAGEMENT_DB = "soccer_management"
PLAYERS_DB = "players"
GAMES_DB = "games"


class DbConnection:
    """
    A class representing a connection to the soccer management database.
    """

    def __init__(self):
        """
        Initializes a new instance of the DbConnection class.

        This method establishes a connection to the MongoDB database using the provided connection URI.
        It also initializes the client and database objects for further use.
        """
        self.client = MongoClient(MONGODB_URL)
        self.db = self.client[SOCCER_MANAGEMENT_DB]
    
    @property
    def players_db(self) -> Collection:
        """
        Gets the players database.

        Returns:
            The players database object.
        """
        return self.db[PLAYERS_DB]

    @property
    def games_db(self) -> Collection:
        """
        Gets the games database.

        Returns:
            The games database object.
        """
        return self.db[GAMES_DB]

