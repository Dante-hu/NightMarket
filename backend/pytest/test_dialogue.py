"""
Tests for:
  GET /api/v1/dialogue/<node_id>
  GET /api/v1/dialogue/root-nodes/<npc_id>

Real IDs from hok_test_data.db:
  - node n_001 => dialogue d_001, npc_001, options: o_001, o_002
  - node n_002 => dialogue d_002, npc_001
  - npc_001 => root node n_001
"""


class TestGetDialogueNode:

    def test_valid_node_returns_200(self, client):
        res = client.get("/api/v1/dialogue/n_001")
        assert res.status_code == 200

    def test_response_has_success_status(self, client):
        res = client.get("/api/v1/dialogue/n_001")
        data = res.get_json()
        assert data["status"] == "success"

    def test_response_has_data_and_meta(self, client):
        res = client.get("/api/v1/dialogue/n_001")
        data = res.get_json()
        assert "data" in data
        assert "meta" in data

    def test_dialogue_node_id_is_correct(self, client):
        res = client.get("/api/v1/dialogue/n_001")
        data = res.get_json()["data"]
        assert data["dialogue_node"] == "n_001"

    def test_dialogue_has_required_fields(self, client):
        res = client.get("/api/v1/dialogue/n_001")
        dialogue = res.get_json()["data"]["dialogue"]
        assert "dialogue_id" in dialogue
        assert "text" in dialogue
        assert "translation" in dialogue
        assert "audio" in dialogue
        assert "npc_id" in dialogue
        assert "key_words" in dialogue

    def test_dialogue_text_is_correct(self, client):
        res = client.get("/api/v1/dialogue/n_001")
        dialogue = res.get_json()["data"]["dialogue"]
        assert dialogue["text"] == "Hello, how are you today?"

    def test_dialogue_npc_id_is_correct(self, client):
        res = client.get("/api/v1/dialogue/n_001")
        dialogue = res.get_json()["data"]["dialogue"]
        assert dialogue["npc_id"] == "npc_001"

    def test_dialogue_has_options(self, client):
        res = client.get("/api/v1/dialogue/n_001")
        options = res.get_json()["data"]["options"]
        assert isinstance(options, list)
        assert len(options) > 0

    def test_option_has_required_fields(self, client):
        res = client.get("/api/v1/dialogue/n_001")
        options = res.get_json()["data"]["options"]
        for option in options:
            assert "option_id" in option
            assert "text" in option
            assert "next_node" in option
            assert "feedback_type" in option

    def test_options_have_correct_feedback_type(self, client):
        res = client.get("/api/v1/dialogue/n_001")
        options = res.get_json()["data"]["options"]
        for option in options:
            assert option["feedback_type"] == "positive"

    def test_keywords_are_list(self, client):
        res = client.get("/api/v1/dialogue/n_001")
        keywords = res.get_json()["data"]["dialogue"]["key_words"]
        assert isinstance(keywords, list)

    def test_keyword_has_required_fields(self, client):
        res = client.get("/api/v1/dialogue/n_001")
        keywords = res.get_json()["data"]["dialogue"]["key_words"]
        for kw in keywords:
            assert "word_id" in kw
            assert "word" in kw
            assert "translation" in kw
            assert "context" in kw
            assert "audio" in kw

    def test_next_nodes_is_list(self, client):
        res = client.get("/api/v1/dialogue/n_001")
        next_nodes = res.get_json()["data"]["next_nodes"]
        assert isinstance(next_nodes, list)

    def test_second_node_returns_200(self, client):
        res = client.get("/api/v1/dialogue/n_002")
        assert res.status_code == 200

    def test_second_node_text_is_correct(self, client):
        res = client.get("/api/v1/dialogue/n_002")
        dialogue = res.get_json()["data"]["dialogue"]
        assert dialogue["text"] == "Thats nice to hear."


class TestGetDialogueRootNodes:

    def test_valid_npc_returns_200(self, client):
        res = client.get("/api/v1/dialogue/root-nodes/npc_001")
        assert res.status_code == 200

    def test_response_has_success_status(self, client):
        res = client.get("/api/v1/dialogue/root-nodes/npc_001")
        data = res.get_json()
        assert data["status"] == "success"

    def test_response_has_data_and_meta(self, client):
        res = client.get("/api/v1/dialogue/root-nodes/npc_001")
        data = res.get_json()
        assert "data" in data
        assert "meta" in data

    def test_npc_id_is_echoed_back(self, client):
        res = client.get("/api/v1/dialogue/root-nodes/npc_001")
        data = res.get_json()["data"]
        assert data["npc_id"] == "npc_001"

    def test_root_node_ids_is_list(self, client):
        res = client.get("/api/v1/dialogue/root-nodes/npc_001")
        data = res.get_json()["data"]
        assert isinstance(data["root_node_ids"], list)

    def test_root_node_ids_not_empty(self, client):
        res = client.get("/api/v1/dialogue/root-nodes/npc_001")
        data = res.get_json()["data"]
        assert len(data["root_node_ids"]) > 0