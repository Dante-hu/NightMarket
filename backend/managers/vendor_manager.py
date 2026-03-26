from database.hok_db import Hok_DB

class Vendor_Manager(Hok_DB):
    def __init__(self, mode):
        super().__init__(mode)
        self.db = self.connect()

    def get_vendor_profile(self, vendor_id):
        vendor = self.get_vendor(vendor_id)[0]
        dialogue_node_id = vendor[1]
        vendor_name = vendor[3]
        item_data = self.get_items(vendor_id)
        items = []
        for item in item_data:
            items.append({
                "item_id": item[1],
                "item_name": item[2],
                "description": item[3],
                "item_value": item[4]
            })

        return {
            "vendor_id": vendor_id,
            "dialogue_node_id": dialogue_node_id,
            "vendor_name": vendor_name,
            "items": items,
        }
        
    def get_vendor(self, vendor_id):
        command = "SELECT * FROM vendors WHERE vendor_id='%s'" % vendor_id
        return self.db.get_data(command)

    def get_items(self, vendor_id):
        command = "SELECT * FROM items WHERE vendor_id='%s'" % vendor_id
        return self.db.get_data(command)

    def get_all_vendors(self):
        command = "SELECT * FROM vendors"
        return self.db.get_data(command)

    def create_vendor(self, vendor_id, node_id, npc_id, vendor_name):
        self.db.insert("vendors", [{"vendor_id": vendor_id, "node_id": node_id, "npc_id": npc_id, "vendor_name": vendor_name}])
        return {"vendor_id": vendor_id, "vendor_name": vendor_name}

    def update_vendor(self, vendor_id, vendor_name):
        self.db.update("vendors", {"vendor_name": vendor_name}, "vendor_id = ?", (vendor_id,))
        return {"vendor_id": vendor_id, "vendor_name": vendor_name}

    def delete_vendor(self, vendor_id):
        items = self.get_items(vendor_id)
        if items:
            return {"error": "Cannot delete vendor with items"}, False
        self.db.delete("vendors", "vendor_id = ?", (vendor_id,))
        return {"message": "Vendor deleted"}, True

    def create_item(self, vendor_id, item_id, item_name, item_description, item_value):
        self.db.insert("items", [{"vendor_id": vendor_id, "item_id": item_id, "item_name": item_name, "item_description": item_description, "item_value": item_value}])
        return {"item_id": item_id, "item_name": item_name}

    def update_item(self, item_id, item_name, item_description, item_value):
        self.db.update("items", {"item_name": item_name, "item_description": item_description, "item_value": item_value}, "item_id = ?", (item_id,))
        return {"item_id": item_id}

    def delete_item(self, item_id):
        self.db.delete("items", "item_id = ?", (item_id,))
        return {"message": "Item deleted"}, True