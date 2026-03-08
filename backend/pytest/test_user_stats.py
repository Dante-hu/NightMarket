"""
Tests for GET /api/v1/user/<user_id>/stats
"""


class TestUserStats:

    def test_known_user_returns_200(self, client):
        res = client.get("/api/v1/user/u123/stats")
        assert res.status_code == 200

    def test_known_user_returns_correct_id(self, client):
        res = client.get("/api/v1/user/u123/stats")
        data = res.get_json()
        assert data["user_id"] == "u123"

    def test_known_user_has_streak(self, client):
        res = client.get("/api/v1/user/u123/stats")
        data = res.get_json()
        assert data["current_streak"] == 5

    def test_known_user_has_activity_heatmap(self, client):
        res = client.get("/api/v1/user/u123/stats")
        data = res.get_json()
        assert isinstance(data["activity_heatmap"], dict)
        assert len(data["activity_heatmap"]) > 0

    def test_known_user_has_preferred_language(self, client):
        res = client.get("/api/v1/user/u123/stats")
        data = res.get_json()
        assert data["preferred_language"] == "hokkien"

    def test_unknown_user_returns_200(self, client):
        res = client.get("/api/v1/user/unknown_user/stats")
        assert res.status_code == 200

    def test_unknown_user_returns_default_streak_zero(self, client):
        res = client.get("/api/v1/user/unknown_user/stats")
        data = res.get_json()
        assert data["current_streak"] == 0

    def test_unknown_user_returns_empty_heatmap(self, client):
        res = client.get("/api/v1/user/unknown_user/stats")
        data = res.get_json()
        assert data["activity_heatmap"] == {}

    def test_unknown_user_last_active_date_is_none(self, client):
        res = client.get("/api/v1/user/unknown_user/stats")
        data = res.get_json()
        assert data["last_active_date"] is None

    def test_unknown_user_id_is_echoed_back(self, client):
        res = client.get("/api/v1/user/new_player_99/stats")
        data = res.get_json()
        assert data["user_id"] == "new_player_99"