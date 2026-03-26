from database.hok_db import Hok_DB

class Dialogue_Manager(Hok_DB):
    def __init__(self, mode):
        super().__init__(mode)
        self.db = self.connect()

    def get_dialogue_node(self, node_id):
        dialogue = self.get_dialogue(node_id)[0]
        next_nodes = self.get_next_nodes(node_id)
        next_nodes_data = [item[0] for item in next_nodes]

        key_words = self.get_key_words(dialogue[1])
        key_words_data = []
        for key_word in key_words:
            key_words_data.append({
                "word_id": key_word[1],
                "word": key_word[2],
                "translation": key_word[3],
                "context": key_word[4],
                "audio": key_word[5]
            })

        options = self.get_node_options(node_id)
        options_data = []
        for option in options:
            events = self.get_option_events(option[1])
            events_data = []
            for evt in events:
                events_data.append({
                    "event_id": evt[1],
                    "event_type": evt[2],
                    "metadata": evt[3]
                })
            options_data.append({
                "option_id": option[1],
                "text": option[2],
                "next_node": option[3],
                "feedback_type": option[4],
                "events": events_data
            })

        return {
            "dialogue_node": node_id,
            "dialogue": {
                "dialogue_id": dialogue[1],
                "text": dialogue[2],
                "translation": dialogue[3],
                "audio": dialogue[4],
                "npc_id": dialogue[5],
                "key_words": key_words_data
            },
            "options": options_data,
            "next_nodes": next_nodes_data
        }
    
    def get_dialogue_root_nodes(self, npc_id):
        root_nodes = self.get_root_nodes(npc_id)[0]
        root_node_ids = []
        for root_node in root_nodes:
            root_node_ids.append(root_node)

        return {
            "npc_id": npc_id,
            "root_node_ids": root_node_ids
        }

    def get_root_nodes(self, npc_id):
        command = "SELECT node_id FROM dialogue_nodes " \
            "WHERE parent_node_id='%s' AND npc_id='%s'" % ("n_000", npc_id)
        return self.db.get_data(command)

    def get_node_options(self, node_id):
        command = "SELECT * FROM options WHERE node_id='%s'" % node_id
        return self.db.get_data(command)
    
    def get_option_events(self, option_id):
        command = "SELECT * FROM events WHERE option_id='%s'" % option_id
        return self.db.get_data(command)

    def get_next_nodes(self, parent_node_id):
        command = "SELECT * FROM dialogue_nodes WHERE parent_node_id='%s'" % parent_node_id
        return self.db.get_data(command)

    def get_dialogue(self, node_id):
        command = "SELECT * FROM dialogues WHERE node_id='%s'" % node_id
        return self.db.get_data(command)

    def get_key_words(self, dialogue_id):
        command = "SELECT * FROM words WHERE dialogue_id='%s'" % dialogue_id
        return self.db.get_data(command)

    def get_all_npcs(self):
        command = "SELECT * FROM npcs"
        return self.db.get_data(command)

    def create_npc(self, npc_id, npc_name):
        self.db.insert("npcs", [{"npc_id": npc_id, "npc_name": npc_name}])
        return {"npc_id": npc_id, "npc_name": npc_name}

    def update_npc(self, npc_id, npc_name):
        self.db.update("npcs", {"npc_name": npc_name}, "npc_id = ?", (npc_id,))
        return {"npc_id": npc_id, "npc_name": npc_name}

    def delete_npc(self, npc_id):
        nodes = self.get_nodes_for_npc(npc_id)
        if nodes:
            return {"error": "Cannot delete NPC with existing dialogue nodes"}, False
        self.db.delete("npcs", "npc_id = ?", (npc_id,))
        return {"message": "NPC deleted"}, True

    def get_nodes_for_npc(self, npc_id):
        command = "SELECT * FROM dialogue_nodes WHERE npc_id='%s'" % npc_id
        return self.db.get_data(command)

    def create_node(self, node_id, parent_node_id, npc_id):
        self.db.insert("dialogue_nodes", [{"node_id": node_id, "parent_node_id": parent_node_id, "npc_id": npc_id}])
        return {"node_id": node_id, "parent_node_id": parent_node_id, "npc_id": npc_id}

    def update_node(self, node_id, parent_node_id):
        self.db.update("dialogue_nodes", {"parent_node_id": parent_node_id}, "node_id = ?", (node_id,))
        return {"node_id": node_id, "parent_node_id": parent_node_id}

    def delete_node(self, node_id):
        children = self.db.get_data("SELECT node_id FROM dialogue_nodes WHERE parent_node_id = '%s'" % node_id)
        if children:
            return {"error": "Cannot delete node with child nodes"}, False
        self.db.delete("dialogue_nodes", "node_id = ?", (node_id,))
        self.db.delete("dialogues", "node_id = ?", (node_id,))
        self.db.delete("options", "node_id = ?", (node_id,))
        return {"message": "Node deleted"}, True

    def get_dialogue_for_node(self, node_id):
        return self.get_dialogue(node_id)

    def create_dialogue(self, node_id, dialogue_id, dialogue_text, translation, npc_id):
        self.db.insert("dialogues", [{"node_id": node_id, "dialogue_id": dialogue_id, "dialogue": dialogue_text, "translation": translation, "audio_clip": "", "npc_id": npc_id}])
        return {"node_id": node_id, "dialogue_id": dialogue_id, "dialogue": dialogue_text}

    def update_dialogue(self, node_id, dialogue_text, translation):
        self.db.update("dialogues", {"dialogue": dialogue_text, "translation": translation}, "node_id = ?", (node_id,))
        return {"node_id": node_id, "dialogue": dialogue_text}

    def get_options_for_node(self, node_id):
        return self.get_node_options(node_id)

    def create_option(self, node_id, option_id, option_text, next_node_id, feedback_type):
        self.db.insert("options", [{"node_id": node_id, "option_id": option_id, "option_text": option_text, "next_node_id": next_node_id, "feedback_type": feedback_type}])
        return {"node_id": node_id, "option_id": option_id, "option_text": option_text}

    def update_option(self, option_id, option_text, next_node_id, feedback_type):
        self.db.update("options", {"option_text": option_text, "next_node_id": next_node_id, "feedback_type": feedback_type}, "option_id = ?", (option_id,))
        return {"option_id": option_id}

    def delete_option(self, option_id):
        self.db.delete("options", "option_id = ?", (option_id,))
        self.db.delete("events", "option_id = ?", (option_id,))
        return {"message": "Option deleted"}, True