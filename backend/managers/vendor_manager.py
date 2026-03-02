from database.sql_db import SQL_DB

class Vendor_Manager:
    def __init__(self, mode):
        self.mode = mode
        self.db_name = self.set_name(self.mode)
        self.db = SQL_DB(path="./database/", db_name=self.db_name)

    def set_name(self, mode):
        match mode:
            case 0:
                return "vendor_data"
            case 1:
                return "vendor_test_data"
            case _:
                raise Exception("Error mode selected is invalid") 

    def create_db(self):
        self.db.create_table("vendors", "vendor_id TEXT, dialogue_node_id TEXT vendor TEXT")
        self.db.create_table("items", "vendor_id TEXT, item_id TEXT, name TEXT, description TEXT, value INTEGER")
