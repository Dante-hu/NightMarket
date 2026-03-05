from database.sql_db import SQL_DB
import os

class Hok_DB:
    def __init__(self, mode):
        self.mode = mode
        self.db_name = self.get_name(self.mode)
        self.db = self.connect()        

    def get_name(self, mode):
        match mode:
            case 0:
                return "hok_data"
            case 1:
                return "hok_test_data"
            case _:
                raise Exception("Error, mode selected is invalid.") 
            
    def connect(self):
        if not os.path.isfile("./database/" + self.db_name + ".db"): 
            raise Exception("Database file not found.")
            
        print("Connecting file: ./database/" + self.db_name + ".db")
        return SQL_DB(path="./database/", db_name=self.db_name)


    def create_tables(self):
        self.db.create_table("dialogue_nodes", "node_id TEXT, parent_node_id TEXT, npc_id TEXT")
        self.db.create_table("npcs", "npc_id TEXT, npc_name TEXT")

        self.db.create_table("dialogues", "node_id TEXT, dialogue_id TEXT, dialogue TEXT, translation TEXT, audio_clip TEXT, npc_id TEXT")
        self.db.create_table("words", "dialogue_id TEXT, word_id TEXT, word TEXT, translation TEXT, conTEXT TEXT, audio_clip TEXT")

        self.db.create_table("options", "node_id TEXT, option_id TEXT, option_TEXT TEXT, next_node_id TEXT, feedback_type TEXT")
        self.db.create_table("events", "option_id TEXT, event_id TEXT, event_type TEXT, metadata TEXT")

        self.db.create_table("vendors", "vendor_id TEXT, node_id TEXT, npc_id TEXT, vendor_name TEXT")
        self.db.create_table("items", "vendor_id TEXT, item_id TEXT, item_name TEXT, item_description TEXT, item_value INTEGER")

