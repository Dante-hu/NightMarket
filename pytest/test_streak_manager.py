# pytest/test_streak_manager.py
# Tests Streak_Manager business logic directly — no Flask server needed.
# Avoids the app.run() port conflict entirely.
# Run with: python3 -m pytest pytest/test_streak_manager.py -v

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from managers.streak_manager import Streak_Manager, words_to_intensity



@pytest.fixture
def manager():
    return Streak_Manager(mode=1)

@pytest.fixture(autouse=True)
def clean_test_users(manager):
    """Wipe test users before each test so tests don't bleed into each other."""
    test_users = [
        "test-new-user", "test-streak-player", "test-broken-player",
        "test-idempotent", "shield-player", "cap-player", "intensity-player"
    ]
    conn = manager.db.get_connection()
    for user in test_users:
        conn.execute("DELETE FROM sessions WHERE user_id = ?", (user,))
        conn.execute("DELETE FROM streaks  WHERE user_id = ?", (user,))
    conn.commit()
    conn.close()
    yield

# words_to_intensity

def test_intensity_zero_words():
    assert words_to_intensity(0) == 0

def test_intensity_level_1():
    assert words_to_intensity(1) == 1
    assert words_to_intensity(5) == 1

def test_intensity_level_2():
    assert words_to_intensity(6) == 2
    assert words_to_intensity(15) == 2

def test_intensity_level_3():
    assert words_to_intensity(16) == 3
    assert words_to_intensity(30) == 3

def test_intensity_level_4():
    assert words_to_intensity(31) == 4
    assert words_to_intensity(49) == 4

def test_intensity_level_5():
    assert words_to_intensity(50) == 5
    assert words_to_intensity(999) == 5

# get_user_stats 

def test_get_stats_unknown_user_returns_zeroes(manager):
    stats = manager.get_user_stats("test-new-user")
    assert stats["current_streak"]    == 0
    assert stats["longest_streak"]    == 0
    assert stats["activity_heatmap"]  == {}
    assert stats["shields_remaining"] == 0
    assert stats["preferred_language"] == "hokkien"

def test_get_stats_returns_correct_keys(manager):
    stats = manager.get_user_stats("test-new-user")
    for key in ["user_id", "current_streak", "longest_streak",
                "last_active_date", "shields_remaining", "activity_heatmap"]:
        assert key in stats

# sync_sessions 

def test_sync_single_session(manager):
    result = manager.sync_sessions("test-streak-player", [
        {"date": "2026-03-16", "wordsLearned": 5, "xpEarned": 20, "activityCount": 1}
    ])
    assert "currentStreak"    in result
    assert "longestStreak"    in result
    assert "shieldsRemaining" in result

def test_sync_consecutive_days_builds_streak(manager):
    result = manager.sync_sessions("test-streak-player", [
        {"date": "2026-03-14", "wordsLearned": 5,  "xpEarned": 20, "activityCount": 1},
        {"date": "2026-03-15", "wordsLearned": 10, "xpEarned": 40, "activityCount": 2},
        {"date": "2026-03-16", "wordsLearned": 20, "xpEarned": 80, "activityCount": 4},
    ])
    assert result["currentStreak"] == 3
    assert result["longestStreak"] == 3

def test_sync_missing_day_breaks_streak(manager):
    result = manager.sync_sessions("test-broken-player", [
        {"date": "2026-03-10", "wordsLearned": 5, "xpEarned": 20, "activityCount": 1},
        {"date": "2026-03-11", "wordsLearned": 5, "xpEarned": 20, "activityCount": 1},
        # gap on 2026-03-12
        {"date": "2026-03-13", "wordsLearned": 5, "xpEarned": 20, "activityCount": 1},
    ])
    assert result["currentStreak"] < 3

def test_sync_duplicate_is_idempotent(manager):
    payload = [{"date": "2026-03-16", "wordsLearned": 8, "xpEarned": 32, "activityCount": 2}]
    r1 = manager.sync_sessions("test-idempotent", payload)
    r2 = manager.sync_sessions("test-idempotent", payload)
    assert r1["currentStreak"] == r2["currentStreak"]
    assert r1["longestStreak"] == r2["longestStreak"]

def test_sync_populates_heatmap(manager):
    manager.sync_sessions("test-streak-player", [
        {"date": "2026-03-14", "wordsLearned": 10, "xpEarned": 40, "activityCount": 2},
        {"date": "2026-03-15", "wordsLearned": 20, "xpEarned": 80, "activityCount": 4},
    ])
    stats = manager.get_user_stats("test-streak-player")
    assert "2026-03-14" in stats["activity_heatmap"]
    assert "2026-03-15" in stats["activity_heatmap"]
    assert stats["activity_heatmap"]["2026-03-14"]["words_learned"] == 10

# intensity levels in heatmap 

def test_intensity_levels_stored_correctly(manager):
    manager.sync_sessions("intensity-player", [
        {"date": "2026-03-11", "wordsLearned": 3,  "xpEarned": 12,  "activityCount": 1},
        {"date": "2026-03-12", "wordsLearned": 10, "xpEarned": 40,  "activityCount": 2},
        {"date": "2026-03-13", "wordsLearned": 20, "xpEarned": 80,  "activityCount": 3},
        {"date": "2026-03-14", "wordsLearned": 35, "xpEarned": 140, "activityCount": 4},
        {"date": "2026-03-15", "wordsLearned": 55, "xpEarned": 220, "activityCount": 5},
    ])
    heatmap = manager.get_user_stats("intensity-player")["activity_heatmap"]
    assert heatmap["2026-03-11"]["intensity"] == 1
    assert heatmap["2026-03-12"]["intensity"] == 2
    assert heatmap["2026-03-13"]["intensity"] == 3
    assert heatmap["2026-03-14"]["intensity"] == 4
    assert heatmap["2026-03-15"]["intensity"] == 5

# shield

def test_award_shield_increments(manager):
    manager.sync_sessions("shield-player", [
        {"date": "2026-03-16", "wordsLearned": 5, "xpEarned": 20, "activityCount": 1}
    ])
    result = manager.award_shield("shield-player")
    assert result["shieldsRemaining"] == 1

def test_award_shield_caps_at_3(manager):
    manager.sync_sessions("cap-player", [
        {"date": "2026-03-16", "wordsLearned": 5, "xpEarned": 20, "activityCount": 1}
    ])
    for _ in range(5):
        manager.award_shield("cap-player")
    stats = manager.get_user_stats("cap-player")
    assert stats["shields_remaining"] <= 3