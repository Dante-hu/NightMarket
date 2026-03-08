"""
Tests for GET /api/v1/vendors/<vendor_id>

Real IDs from hok_test_data.db:
  - v_001 => "A-Ging's Bubble Tea", items: i_001, i_002, i_003
  - v_002 => test_vendor_name_002
  - v_003 => test_vendor_name_003
"""


class TestVendorProfile:

    def test_valid_vendor_returns_200(self, client):
        res = client.get("/api/v1/vendors/v_001")
        assert res.status_code == 200

    def test_response_has_success_status(self, client):
        res = client.get("/api/v1/vendors/v_001")
        data = res.get_json()
        assert data["status"] == "success"

    def test_response_has_data_key(self, client):
        res = client.get("/api/v1/vendors/v_001")
        data = res.get_json()
        assert "data" in data

    def test_response_has_meta_key(self, client):
        res = client.get("/api/v1/vendors/v_001")
        data = res.get_json()
        assert "meta" in data

    def test_vendor_id_is_correct(self, client):
        res = client.get("/api/v1/vendors/v_001")
        data = res.get_json()["data"]
        assert data["vendor_id"] == "v_001"

    def test_vendor_name_is_correct(self, client):
        res = client.get("/api/v1/vendors/v_001")
        data = res.get_json()["data"]
        assert data["vendor_name"] == "A-Ging's Bubble Tea"

    def test_vendor_has_dialogue_node_id(self, client):
        res = client.get("/api/v1/vendors/v_001")
        data = res.get_json()["data"]
        assert "dialogue_node_id" in data
        assert data["dialogue_node_id"] is not None

    def test_vendor_has_items_list(self, client):
        res = client.get("/api/v1/vendors/v_001")
        data = res.get_json()["data"]
        assert isinstance(data["items"], list)
        assert len(data["items"]) > 0

    def test_item_has_required_fields(self, client):
        res = client.get("/api/v1/vendors/v_001")
        items = res.get_json()["data"]["items"]
        for item in items:
            assert "item_id" in item
            assert "item_name" in item
            assert "description" in item
            assert "item_value" in item

    def test_item_value_is_numeric(self, client):
        res = client.get("/api/v1/vendors/v_001")
        items = res.get_json()["data"]["items"]
        for item in items:
            assert isinstance(item["item_value"], (int, float))

    def test_second_vendor_returns_200(self, client):
        res = client.get("/api/v1/vendors/v_002")
        assert res.status_code == 200

    def test_second_vendor_name_is_correct(self, client):
        res = client.get("/api/v1/vendors/v_002")
        data = res.get_json()["data"]
        assert data["vendor_name"] == "test_vendor_name_002"