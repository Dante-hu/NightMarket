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
                "audio": key_word[5],
                "english_word": key_word[6] if len(key_word) > 6 else ""
                
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