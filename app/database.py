from pymongo import MongoClient

# MongoDB connection URI

MONGODB_URL = "mongodb+srv://orito:uWQ3nJgt0U1lqbUW@soccermanagementcluster.exqi9dy.mongodb.net/?retryWrites=true&w=majority&appName=SoccerManagementCluster"
SOCCER_MANAGEMENT_DB = "soccer_management"
PLAYERS_DB = "players"
GAMES_DB = "games"


class DbConnection:
    def __init__(self):
        self.client = MongoClient(MONGODB_URL)
        print(self.client.list_database_names())
        self.db = self.client[SOCCER_MANAGEMENT_DB]
    
    @property
    def players_db(self):
        return self.db[PLAYERS_DB]

    @property
    def games_db(self):
        return self.db[GAMES_DB]

