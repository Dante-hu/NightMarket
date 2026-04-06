from .sql_db import SQL_DB
import os

class Hok_DB:
    def __init__(self, mode=1):
        self.mode = mode
        self.db_name = None
        self.base_dir = None
        self.db = None
            
    def connect(self):
        self.db_name = self.get_name(self.mode)
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

        if not os.path.isfile(self.base_dir + self.db_name + ".db"): 
            raise Exception("Database file not found.")
            
        print("Connecting file: " + self.base_dir + self.db_name + ".db")
        return SQL_DB(path=self.base_dir, db_name=self.db_name)
    
    def get_name(self, mode):
        match mode:
            case 0:
                return "hok_data"
            case 1:
                return "hok_test_data"
            case 2:
                return "hok_lesson_data"
            case _:
                raise Exception("Error, mode selected is invalid.") 

    # temp function used for creating initial db, should not be used at all in prod
    def create_tables(self):
        self.db.create_table("dialogue_nodes", "node_id TEXT, parent_node_id TEXT, npc_id TEXT")
        self.db.create_table("npcs", "npc_id TEXT, npc_name TEXT")

        self.db.create_table("dialogues", "node_id TEXT, dialogue_id TEXT, dialogue TEXT, translation_HAN TEXT, translation_POJ TEXT, audio_clip TEXT, npc_id TEXT")
        #self.db.create_table("words", "dialogue_id TEXT, word_id TEXT, word TEXT, translation TEXT, conTEXT TEXT, audio_clip TEXT")

        self.db.create_table("options", "node_id TEXT, option_id TEXT, option_TEXT TEXT, next_node_id TEXT, feedback_type TEXT")
        self.db.create_table("events", "option_id TEXT, event_id TEXT, event_type TEXT, metadata TEXT")

        self.db.create_table("vendors", "vendor_id TEXT, node_id TEXT, npc_id TEXT, vendor_name TEXT")
        self.db.create_table("items", "vendor_id TEXT, item_id TEXT, item_name TEXT, item_description TEXT, item_value INTEGER")
        
        #minigame api
        self.db.create_table("challenges", 
            "challenge_id TEXT, title TEXT, type TEXT, difficulty TEXT")
        
        self.db.create_table("challenge_requirements",
            "challenge_id TEXT, target_item_id TEXT, exact_price INTEGER, required_toppings TEXT")
        
        self.db.create_table("user_challenges",
            "user_id TEXT, challenge_id TEXT, status TEXT, accepted_at TEXT, completed_at TEXT")
        
        self.db.create_table("inventory",
            "user_id TEXT, item_id TEXT, challenge_id TEXT, acquired_at TEXT")

    def insert(self, table_name, data):
        self.db.insert(table_name, data)