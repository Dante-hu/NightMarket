from database.hok_db import Hok_DB

class Vendor_Manager(Hok_DB):
    def __init__(self, mode):
        super().__init__(mode)

    def get_vendor_profile(self, vendor_id):
        vendor = self.get_vendor(vendor_id)[0]
        dialogue_node_id = vendor[1]
        vendor_name = vendor[3]
        item_data = self.get_items()
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