"""
Tests for minigame / challenge endpoints:
  GET  /api/v1/challenges
  GET  /api/v1/challenges/<challenge_id>
  POST /api/v1/challenges/accept
  POST /api/v1/challenges/inventory
  GET  /api/v1/user/<user_id>/inventory
  POST /api/v1/challenges/verify

Real test data:
  ch_001 → ORDER_SPECIFIC_ITEM   (item: i_001, price: 5.99)
  ch_002 → ORDER_SPECIFIC_ITEM   (item: i_003, price: 5.99)
  ch_003 → BUY_FROM_SPECIFIC_VENDOR (vendor: v_001)
  ch_004 → COLLECT_MULTIPLE_ITEMS  (items: i_001, i_002)
  ch_005 → COLLECT_MULTIPLE_ITEMS  (items: i_001, i_002, i_003)
"""


class TestGetChallenges:

    def test_returns_200(self, client):
        res = client.get("/api/v1/challenges")
        assert res.status_code == 200

    def test_response_has_success_status(self, client):
        res = client.get("/api/v1/challenges")
        assert res.get_json()["status"] == "success"

    def test_response_has_data_and_meta(self, client):
        data = res = client.get("/api/v1/challenges").get_json()
        assert "data" in data
        assert "meta" in data

    def test_returns_list_of_challenges(self, client):
        data = client.get("/api/v1/challenges").get_json()["data"]
        assert isinstance(data, list)
        assert len(data) == 5

    def test_challenge_has_required_fields(self, client):
        data = client.get("/api/v1/challenges").get_json()["data"]
        for challenge in data:
            assert "challenge_id" in challenge
            assert "title" in challenge
            assert "type" in challenge

    def test_challenge_does_not_expose_requirements(self, client):
        """List endpoint should be lightweight — no requirements data."""
        data = client.get("/api/v1/challenges").get_json()["data"]
        for challenge in data:
            assert "requirements" not in challenge

    def test_challenge_types_are_valid(self, client):
        valid_types = {"ORDER_SPECIFIC_ITEM", "BUY_FROM_SPECIFIC_VENDOR", "COLLECT_MULTIPLE_ITEMS"}
        data = client.get("/api/v1/challenges").get_json()["data"]
        for challenge in data:
            assert challenge["type"] in valid_types


class TestGetChallenge:

    def test_valid_challenge_returns_200(self, client):
        res = client.get("/api/v1/challenges/ch_001")
        assert res.status_code == 200

    def test_response_has_success_status(self, client):
        res = client.get("/api/v1/challenges/ch_001")
        assert res.get_json()["status"] == "success"

    def test_challenge_has_requirements(self, client):
        data = client.get("/api/v1/challenges/ch_001").get_json()["data"]
        assert "requirements" in data

    def test_order_specific_item_requirements(self, client):
        data = client.get("/api/v1/challenges/ch_001").get_json()["data"]
        assert data["type"] == "ORDER_SPECIFIC_ITEM"
        assert "target_item_id" in data["requirements"]
        assert "exact_price" in data["requirements"]
        assert data["requirements"]["target_item_id"] == "i_001"
        assert data["requirements"]["exact_price"] == 5.99

    def test_buy_from_vendor_requirements(self, client):
        data = client.get("/api/v1/challenges/ch_003").get_json()["data"]
        assert data["type"] == "BUY_FROM_SPECIFIC_VENDOR"
        assert "target_vendor_id" in data["requirements"]
        assert data["requirements"]["target_vendor_id"] == "v_001"

    def test_collect_multiple_items_requirements(self, client):
        data = client.get("/api/v1/challenges/ch_004").get_json()["data"]
        assert data["type"] == "COLLECT_MULTIPLE_ITEMS"
        assert "required_items" in data["requirements"]
        assert isinstance(data["requirements"]["required_items"], list)
        assert "i_001" in data["requirements"]["required_items"]
        assert "i_002" in data["requirements"]["required_items"]

    def test_invalid_challenge_returns_404(self, client):
        res = client.get("/api/v1/challenges/ch_999")
        assert res.status_code == 404

    def test_invalid_challenge_returns_error_status(self, client):
        res = client.get("/api/v1/challenges/ch_999")
        assert res.get_json()["status"] == "error"


class TestAcceptChallenge:

    def test_returns_200(self, client):
        res = client.post("/api/v1/challenges/accept", json={
            "user_id": "u_accept_test",
            "challenge_id": "ch_001"
        })
        assert res.status_code == 200

    def test_response_has_success_status(self, client):
        res = client.post("/api/v1/challenges/accept", json={
            "user_id": "u_accept_test2",
            "challenge_id": "ch_001"
        })
        assert res.get_json()["status"] == "success"

    def test_response_has_correct_data(self, client):
        res = client.post("/api/v1/challenges/accept", json={
            "user_id": "u_accept_test3",
            "challenge_id": "ch_002"
        })
        data = res.get_json()["data"]
        assert data["user_id"] == "u_accept_test3"
        assert data["challenge_id"] == "ch_002"
        assert data["status"] == "active"
        assert "accepted_at" in data

    def test_cannot_accept_two_challenges(self, client):
        """User should not be able to accept a second challenge while one is active."""
        client.post("/api/v1/challenges/accept", json={
            "user_id": "u_double_accept",
            "challenge_id": "ch_001"
        })
        res = client.post("/api/v1/challenges/accept", json={
            "user_id": "u_double_accept",
            "challenge_id": "ch_002"
        })
        assert res.status_code == 400

    def test_missing_user_id_returns_400(self, client):
        res = client.post("/api/v1/challenges/accept", json={
            "challenge_id": "ch_001"
        })
        assert res.status_code == 400

    def test_missing_challenge_id_returns_400(self, client):
        res = client.post("/api/v1/challenges/accept", json={
            "user_id": "u_accept_test4"
        })
        assert res.status_code == 400

    def test_invalid_challenge_returns_400(self, client):
        res = client.post("/api/v1/challenges/accept", json={
            "user_id": "u_accept_test5",
            "challenge_id": "ch_999"
        })
        assert res.status_code == 400


class TestAddToInventory:

    def test_returns_200(self, client):
        # Accept challenge first
        client.post("/api/v1/challenges/accept", json={
            "user_id": "u_inv_test",
            "challenge_id": "ch_001"
        })
        res = client.post("/api/v1/challenges/inventory", json={
            "user_id": "u_inv_test",
            "item_id": "i_001",
            "challenge_id": "ch_001"
        })
        assert res.status_code == 200

    def test_response_has_success_status(self, client):
        client.post("/api/v1/challenges/accept", json={
            "user_id": "u_inv_test2",
            "challenge_id": "ch_001"
        })
        res = client.post("/api/v1/challenges/inventory", json={
            "user_id": "u_inv_test2",
            "item_id": "i_001",
            "challenge_id": "ch_001"
        })
        assert res.get_json()["status"] == "success"

    def test_response_has_correct_data(self, client):
        client.post("/api/v1/challenges/accept", json={
            "user_id": "u_inv_test3",
            "challenge_id": "ch_001"
        })
        res = client.post("/api/v1/challenges/inventory", json={
            "user_id": "u_inv_test3",
            "item_id": "i_001",
            "challenge_id": "ch_001"
        })
        data = res.get_json()["data"]
        assert data["user_id"] == "u_inv_test3"
        assert data["item_id"] == "i_001"
        assert data["challenge_id"] == "ch_001"
        assert "acquired_at" in data

    def test_duplicate_item_returns_400(self, client):
        """Same item cannot be added twice for the same challenge."""
        client.post("/api/v1/challenges/accept", json={
            "user_id": "u_inv_dup",
            "challenge_id": "ch_001"
        })
        client.post("/api/v1/challenges/inventory", json={
            "user_id": "u_inv_dup",
            "item_id": "i_001",
            "challenge_id": "ch_001"
        })
        res = client.post("/api/v1/challenges/inventory", json={
            "user_id": "u_inv_dup",
            "item_id": "i_001",
            "challenge_id": "ch_001"
        })
        assert res.status_code == 400

    def test_missing_fields_returns_400(self, client):
        res = client.post("/api/v1/challenges/inventory", json={
            "user_id": "u_inv_test4"
        })
        assert res.status_code == 400


class TestGetUserInventory:

    def test_returns_200(self, client):
        res = client.get("/api/v1/user/u123/inventory")
        assert res.status_code == 200

    def test_response_has_success_status(self, client):
        res = client.get("/api/v1/user/u123/inventory")
        assert res.get_json()["status"] == "success"

    def test_response_has_required_fields(self, client):
        data = client.get("/api/v1/user/u123/inventory").get_json()["data"]
        assert "user_id" in data
        assert "active_challenge_id" in data
        assert "inventory" in data

    def test_inventory_is_list(self, client):
        data = client.get("/api/v1/user/u123/inventory").get_json()["data"]
        assert isinstance(data["inventory"], list)

    def test_user_with_items_in_inventory(self, client):
        """Set up a user with items and verify they appear in inventory."""
        client.post("/api/v1/challenges/accept", json={
            "user_id": "u_inv_fetch",
            "challenge_id": "ch_004"
        })
        client.post("/api/v1/challenges/inventory", json={
            "user_id": "u_inv_fetch",
            "item_id": "i_001",
            "challenge_id": "ch_004"
        })
        data = client.get("/api/v1/user/u_inv_fetch/inventory").get_json()["data"]
        assert data["active_challenge_id"] == "ch_004"
        assert len(data["inventory"]) == 1
        assert data["inventory"][0]["item_id"] == "i_001"


class TestVerifyChallenge:

    def test_order_specific_item_success(self, client):
        """ch_001 requires i_001 at 5.99."""
        client.post("/api/v1/challenges/accept", json={
            "user_id": "u_verify_001",
            "challenge_id": "ch_001"
        })
        res = client.post("/api/v1/challenges/verify", json={
            "user_id": "u_verify_001",
            "challenge_id": "ch_001",
            "final_order": {
                "item_id": "i_001",
                "total_paid": 5.99
            }
        })
        data = res.get_json()["data"]
        assert res.status_code == 200
        assert data["is_success"] == True
        assert data["reason"] is None

    def test_order_specific_item_wrong_item(self, client):
        client.post("/api/v1/challenges/accept", json={
            "user_id": "u_verify_002",
            "challenge_id": "ch_001"
        })
        res = client.post("/api/v1/challenges/verify", json={
            "user_id": "u_verify_002",
            "challenge_id": "ch_001",
            "final_order": {
                "item_id": "i_002",  # wrong item
                "total_paid": 5.99
            }
        })
        data = res.get_json()["data"]
        assert data["is_success"] == False
        assert data["reason"] == "Wrong item ordered"

    def test_buy_from_vendor_success(self, client):
        """ch_003 requires buying from v_001."""
        client.post("/api/v1/challenges/accept", json={
            "user_id": "u_verify_004",
            "challenge_id": "ch_003"
        })
        res = client.post("/api/v1/challenges/verify", json={
            "user_id": "u_verify_004",
            "challenge_id": "ch_003",
            "final_order": {
                "vendor_id": "v_001"
            }
        })
        data = res.get_json()["data"]
        assert data["is_success"] == True

    def test_buy_from_vendor_wrong_vendor(self, client):
        client.post("/api/v1/challenges/accept", json={
            "user_id": "u_verify_005",
            "challenge_id": "ch_003"
        })
        res = client.post("/api/v1/challenges/verify", json={
            "user_id": "u_verify_005",
            "challenge_id": "ch_003",
            "final_order": {
                "vendor_id": "v_002"  # wrong vendor
            }
        })
        data = res.get_json()["data"]
        assert data["is_success"] == False
        assert data["reason"] == "Must buy from the correct vendor"

    def test_collect_multiple_items_success(self, client):
        """ch_004 requires i_001 and i_002."""
        client.post("/api/v1/challenges/accept", json={
            "user_id": "u_verify_006",
            "challenge_id": "ch_004"
        })
        client.post("/api/v1/challenges/inventory", json={
            "user_id": "u_verify_006",
            "item_id": "i_001",
            "challenge_id": "ch_004"
        })
        client.post("/api/v1/challenges/inventory", json={
            "user_id": "u_verify_006",
            "item_id": "i_002",
            "challenge_id": "ch_004"
        })
        res = client.post("/api/v1/challenges/verify", json={
            "user_id": "u_verify_006",
            "challenge_id": "ch_004",
            "final_order": {}
        })
        data = res.get_json()["data"]
        assert data["is_success"] == True
        assert data["reason"] is None

    def test_collect_multiple_items_missing_item(self, client):
        """Verify fails if not all required items are collected."""
        client.post("/api/v1/challenges/accept", json={
            "user_id": "u_verify_007",
            "challenge_id": "ch_004"
        })
        # Only add one of the two required items
        client.post("/api/v1/challenges/inventory", json={
            "user_id": "u_verify_007",
            "item_id": "i_001",
            "challenge_id": "ch_004"
        })
        res = client.post("/api/v1/challenges/verify", json={
            "user_id": "u_verify_007",
            "challenge_id": "ch_004",
            "final_order": {}
        })
        data = res.get_json()["data"]
        assert data["is_success"] == False
        assert "Missing items" in data["reason"]

    def test_verify_without_active_challenge_fails(self, client):
        """Cannot verify a challenge that hasn't been accepted."""
        res = client.post("/api/v1/challenges/verify", json={
            "user_id": "u_no_challenge",
            "challenge_id": "ch_001",
            "final_order": {"item_id": "i_001", "total_paid": 5.99}
        })
        data = res.get_json()["data"]
        assert data["is_success"] == False

    def test_missing_fields_returns_400(self, client):
        res = client.post("/api/v1/challenges/verify", json={
            "user_id": "u_verify_008"
        })
        assert res.status_code == 400

    def test_response_always_has_challenge_id(self, client):
        client.post("/api/v1/challenges/accept", json={
            "user_id": "u_verify_009",
            "challenge_id": "ch_001"
        })
        res = client.post("/api/v1/challenges/verify", json={
            "user_id": "u_verify_009",
            "challenge_id": "ch_001",
            "final_order": {"item_id": "i_001", "total_paid": 5.99}
        })
        data = res.get_json()["data"]
        assert data["challenge_id"] == "ch_001"