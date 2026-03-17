
from database.hok_db import Hok_DB
from datetime import date

THRESHOLDS = [0, 1, 6, 16, 31, 50]  # mirror unity client

def words_to_intensity(words: int) -> int:
    level = 0
    for i, t in enumerate(THRESHOLDS):
        if words >= t:
            level = i
    return level


class Streak_Manager:
    def __init__(self, mode=1):
        self.mode = mode
        hok_db = Hok_DB(mode)
        self.db = hok_db.connect()
        self._ensure_tables()

    # table setup

    def _ensure_tables(self):
        """Creates streak and session tables if they don't exist.
        Matches the create_table pattern used in Hok_DB.create_tables().
        """
        self.db.create_table(
            "streaks",
            "user_id TEXT PRIMARY KEY, "
            "current_streak INTEGER NOT NULL DEFAULT 0, "
            "longest_streak INTEGER NOT NULL DEFAULT 0, "
            "last_session_date TEXT, "
            "shields_remaining INTEGER NOT NULL DEFAULT 0"
        )
        self.db.create_table(
            "sessions",
            "user_id TEXT NOT NULL, "
            "session_date TEXT NOT NULL, "
            "words_learned INTEGER NOT NULL DEFAULT 0, "
            "xp_earned INTEGER NOT NULL DEFAULT 0, "
            "activity_count INTEGER NOT NULL DEFAULT 0, "
            "intensity INTEGER NOT NULL DEFAULT 0, "
            "UNIQUE(user_id, session_date)"
        )

    # call app from the app_factory file

    def get_user_stats(self, user_id: str) -> dict:
        """Returns streak state + heatmap for a user.
        Replaces the MOCK_USER_STATS block in app_factory.py.
        """
        streak = self._get_streak_row(user_id)
        heatmap = self._get_heatmap(user_id, weeks=52)

        return {
            "user_id":          user_id,
            "current_streak":   streak["current_streak"],
            "longest_streak":   streak["longest_streak"],
            "last_active_date": streak["last_session_date"],
            "shields_remaining": streak["shields_remaining"],
            "activity_heatmap": heatmap,
            "preferred_language": "hokkien"
        }

    def sync_sessions(self, user_id: str, entries: list) -> dict:
        """Upserts a batch of session entries from the Unity client.
        Called from POST /api/v1/user/<user_id>/sync

        Args:
            user_id: Player identifier
            entries: List of dicts with keys:
                     date, wordsLearned, xpEarned, activityCount

        Returns:
            { currentStreak, longestStreak, shieldsRemaining }
        """
        self._ensure_user(user_id)

        latest_date = None
        for entry in entries:
            entry_date     = entry.get("date", "")
            words_learned  = int(entry.get("wordsLearned",  0))
            xp_earned      = int(entry.get("xpEarned",      0))
            activity_count = int(entry.get("activityCount", 1))
            intensity      = words_to_intensity(words_learned)

            if not entry_date:
                continue

            self._upsert_session(
                user_id, entry_date, words_learned,
                xp_earned, activity_count, intensity
            )

            if latest_date is None or entry_date > latest_date:
                latest_date = entry_date

        # from fll user history calculate streak
        streak = self._recalculate_streak(user_id)
        self._save_streak(user_id, streak["current_streak"],
                          streak["longest_streak"], latest_date)

        row = self._get_streak_row(user_id)
        return {
            "currentStreak":    row["current_streak"],
            "longestStreak":    row["longest_streak"],
            "shieldsRemaining": row["shields_remaining"]
        }

    def award_shield(self, user_id: str) -> dict:
        """Increments shields_remaining (max 3) for a user."""
        self._ensure_user(user_id)
        row = self._get_streak_row(user_id)
        new_shields = min(row["shields_remaining"] + 1, 3)

        self.db.get_connection().execute(
            "UPDATE streaks SET shields_remaining = ? WHERE user_id = ?",
            (new_shields, user_id)
        )
        self.db.get_connection().commit()

        return {"shieldsRemaining": new_shields}

    # helper fncs

    def _ensure_user(self, user_id: str):
        """Creates streak row for user if it doesn't exist."""
        existing = self.db.get_data(
            f"SELECT user_id FROM streaks WHERE user_id = '{user_id}'"
        )
        if not existing:
            self.db.insert("streaks", [{"user_id": user_id}])

    def _get_streak_row(self, user_id: str) -> dict:
        rows = self.db.get_data(
            f"SELECT user_id, current_streak, longest_streak, "
            f"last_session_date, shields_remaining "
            f"FROM streaks WHERE user_id = '{user_id}'"
        )
        if not rows:
            return {
                "current_streak": 0, "longest_streak": 0,
                "last_session_date": None, "shields_remaining": 0
            }
        r = rows[0]
        return {
            "current_streak":   r[1],
            "longest_streak":   r[2],
            "last_session_date": r[3],
            "shields_remaining": r[4]
        }

    def _get_heatmap(self, user_id: str, weeks: int = 52) -> dict:
        """Returns heatmap as { "YYYY-MM-DD": activity_count } dict
        matching the shape the Unity HeatmapUI expects.
        """
        rows = self.db.get_data(
            f"SELECT session_date, words_learned, xp_earned, "
            f"activity_count, intensity "
            f"FROM sessions WHERE user_id = '{user_id}' "
            f"AND session_date >= date('now', '-{weeks * 7} days') "
            f"ORDER BY session_date ASC"
        )
        return {
            r[0]: {
                "words_learned":  r[1],
                "xp_earned":      r[2],
                "activity_count": r[3],
                "intensity":      r[4]
            }
            for r in rows
        }

    def _upsert_session(self, user_id, session_date, words_learned,
                        xp_earned, activity_count, intensity):
        """INSERT or UPDATE a session row, keeping the highest values seen."""
        conn = self.db.get_connection()
        conn.execute("""
            INSERT INTO sessions
                (user_id, session_date, words_learned, xp_earned, activity_count, intensity)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, session_date) DO UPDATE SET
                words_learned  = MAX(words_learned,  excluded.words_learned),
                xp_earned      = MAX(xp_earned,      excluded.xp_earned),
                activity_count = MAX(activity_count, excluded.activity_count),
                intensity      = MAX(intensity,       excluded.intensity)
        """, (user_id, session_date, words_learned, xp_earned, activity_count, intensity))
        conn.commit()
        conn.close()

    def _recalculate_streak(self, user_id: str) -> dict:
        """Recalculates current + longest streak from full session history.
        Same algorithm as the Python streak_routes.py version.
        """
        rows = self.db.get_data(
            f"SELECT session_date FROM sessions "
            f"WHERE user_id = '{user_id}' "
            f"ORDER BY session_date DESC"
        )
        if not rows:
            return {"current_streak": 0, "longest_streak": 0}

        from datetime import date as dt
        dates = [dt.fromisoformat(r[0]) for r in rows]
        today = dt.today()

        days_since_last = (today - dates[0]).days

        # Current streak
        if days_since_last > 1:
            current_streak = 0
        else:
            current_streak = 1
            for i in range(1, len(dates)):
                if (dates[i - 1] - dates[i]).days == 1:
                    current_streak += 1
                else:
                    break

        # Longest streak
        longest_streak = current_streak
        temp = 1
        for i in range(1, len(dates)):
            if (dates[i - 1] - dates[i]).days == 1:
                temp += 1
                longest_streak = max(longest_streak, temp)
            else:
                temp = 1

        return {
            "current_streak": current_streak,
            "longest_streak": max(longest_streak, current_streak)
        }

    def _save_streak(self, user_id, current_streak, longest_streak, latest_date):
        conn = self.db.get_connection()
        conn.execute("""
            UPDATE streaks SET
                current_streak    = ?,
                longest_streak    = MAX(longest_streak, ?),
                last_session_date = CASE
                    WHEN last_session_date IS NULL OR ? > last_session_date
                    THEN ? ELSE last_session_date END
            WHERE user_id = ?
        """, (current_streak, longest_streak,
              latest_date, latest_date, user_id))
        conn.commit()
        conn.close()