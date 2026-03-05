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
            event = self.get_node_options(option[1])
            options_data.append({
                "option_id": option[1],
                "text": option[2],
                "next_node": option[3],
                "feedback_type": option[4],
                "event": event
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
    
    def get_node_options(self, node_id):
        command = "SELECT * FROM options WHERE node_id='%s'" % node_id
        return self.db.get_data(command)
    
    def get_option_events(self, option_id):
        command = "SELECT * FROM events WHERE node_id='%s'" % option_id
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