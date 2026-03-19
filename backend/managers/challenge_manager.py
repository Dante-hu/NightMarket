import json
from datetime import datetime, timezone
from database.hok_db import Hok_DB

class Challenge_Manager(Hok_DB):
    def __init__(self, mode):
        super().__init__(mode)
        self.db = self.connect()

    #Challenge Fetching

    def get_all_challenges(self):
        """Returns lightweight list of all challenges for the selection screen."""
        command = "SELECT challenge_id, title, type FROM challenges"
        rows = self.db.get_data(command)
        return [
            {
                "challenge_id": row[0],
                "title": row[1],
                "type": row[2]
            }
            for row in rows
        ]

    def get_challenge(self, challenge_id):
        """Returns full details + requirements for a specific challenge."""
        command = "SELECT * FROM challenges WHERE challenge_id='%s'" % challenge_id
        rows = self.db.get_data(command)
        if not rows:
            return None

        challenge = rows[0]
        requirements = self._get_requirements(challenge_id)

        return {
            "challenge_id": challenge[0],
            "title": challenge[1],
            "type": challenge[2],
            "requirements": requirements
        }

    def _get_requirements(self, challenge_id):
        """Internal helper to fetch and format requirements for a challenge."""
        command = "SELECT * FROM challenge_requirements WHERE challenge_id='%s'" % challenge_id
        rows = self.db.get_data(command)
        if not rows:
            return {}

        req = rows[0]
        challenge_type = self._get_challenge_type(challenge_id)

        if challenge_type == "ORDER_SPECIFIC_ITEM":
            return {
                "target_item_id": req[1],
                "exact_price": req[3]
            }
        elif challenge_type == "BUY_FROM_SPECIFIC_VENDOR":
            return {
                "target_vendor_id": req[2]
            }
        elif challenge_type == "COLLECT_MULTIPLE_ITEMS":
            return {
                "required_items": json.loads(req[4]) if req[4] else []
            }
        return {}

    def _get_challenge_type(self, challenge_id):
        """Internal helper to get challenge type."""
        command = "SELECT type FROM challenges WHERE challenge_id='%s'" % challenge_id
        rows = self.db.get_data(command)
        return rows[0][0] if rows else None

    # ── User Challenge Actions ────────────────────────────────────────

    def accept_challenge(self, user_id, challenge_id):
        """Accepts a challenge for a user. Only one active challenge allowed at a time."""

        # Check if challenge exists
        if not self.get_challenge(challenge_id):
            return None, "Challenge not found"

        # Check if user already has an active challenge
        existing = self.get_active_challenge(user_id)
        if existing:
            return None, "User already has an active challenge: %s" % existing["challenge_id"]

        # Insert into user_challenges
        now = datetime.now(timezone.utc).isoformat()
        self.db.insert("user_challenges", [{
            "user_id": user_id,
            "challenge_id": challenge_id,
            "status": "active",
            "accepted_at": now,
            "completed_at": ""
        }])

        return {
            "user_id": user_id,
            "challenge_id": challenge_id,
            "status": "active",
            "accepted_at": now
        }, None

    def get_active_challenge(self, user_id):
        """Returns the user's currently active challenge or None."""
        command = "SELECT * FROM user_challenges WHERE user_id='%s' AND status='active'" % user_id
        rows = self.db.get_data(command)
        if not rows:
            return None
        row = rows[0]
        return {
            "user_id": row[0],
            "challenge_id": row[1],
            "status": row[2],
            "accepted_at": row[3],
            "completed_at": row[4]
        }

    # ── Inventory ─────────────────────────────────────────────────────

    def add_to_inventory(self, user_id, item_id, challenge_id):
        """Adds an item to the user's inventory for a given challenge."""
        now = datetime.now(timezone.utc).isoformat()

        # Check for duplicate — don't add the same item twice for same challenge
        command = "SELECT * FROM inventory WHERE user_id='%s' AND item_id='%s' AND challenge_id='%s'" % (
            user_id, item_id, challenge_id)
        existing = self.db.get_data(command)
        if existing:
            return None, "Item already in inventory for this challenge"

        self.db.insert("inventory", [{
            "user_id": user_id,
            "item_id": item_id,
            "challenge_id": challenge_id,
            "acquired_at": now
        }])

        return {
            "user_id": user_id,
            "item_id": item_id,
            "challenge_id": challenge_id,
            "acquired_at": now
        }, None

    def get_user_inventory(self, user_id):
        """Returns all inventory items for a user along with their active challenge."""
        active = self.get_active_challenge(user_id)

        command = "SELECT * FROM inventory WHERE user_id='%s'" % user_id
        rows = self.db.get_data(command)
        items = [
            {
                "item_id": row[1],
                "challenge_id": row[2],
                "acquired_at": row[3]
            }
            for row in rows
        ]

        return {
            "user_id": user_id,
            "active_challenge_id": active["challenge_id"] if active else None,
            "inventory": items
        }

    # ── Challenge Verification ────────────────────────────────────────

    def verify_challenge(self, user_id, challenge_id, final_order):
        """
        Verifies whether the user has successfully completed the challenge.
        Returns (is_success, reason)
        """
        challenge = self.get_challenge(challenge_id)
        if not challenge:
            return False, "Challenge not found"

        # Check user has this challenge active
        active = self.get_active_challenge(user_id)
        if not active or active["challenge_id"] != challenge_id:
            return False, "Challenge is not active for this user"

        requirements = challenge["requirements"]
        challenge_type = challenge["type"]
        is_success = False
        reason = None

        if challenge_type == "ORDER_SPECIFIC_ITEM":
            item_match = final_order.get("item_id") == requirements.get("target_item_id")
            price_match = final_order.get("total_paid") == requirements.get("exact_price")

            if not item_match:
                reason = "Wrong item ordered"
            elif not price_match:
                reason = "Incorrect price paid"
            else:
                is_success = True

        elif challenge_type == "BUY_FROM_SPECIFIC_VENDOR":
            vendor_match = final_order.get("vendor_id") == requirements.get("target_vendor_id")
            if not vendor_match:
                reason = "Must buy from the correct vendor"
            else:
                is_success = True

        elif challenge_type == "COLLECT_MULTIPLE_ITEMS":
            required = set(requirements.get("required_items", []))

            # Check inventory for collected items
            command = "SELECT item_id FROM inventory WHERE user_id='%s' AND challenge_id='%s'" % (
                user_id, challenge_id)
            collected = set(row[0] for row in self.db.get_data(command))

            missing = required - collected
            if missing:
                reason = "Missing items: %s" % list(missing)
            else:
                is_success = True

        # If successful, mark challenge as completed
        if is_success:
            self._complete_challenge(user_id, challenge_id)

        return is_success, reason

    def _complete_challenge(self, user_id, challenge_id):
        """Marks a challenge as completed in user_challenges."""
        now = datetime.now(timezone.utc).isoformat()
        command = "UPDATE user_challenges SET status='completed', completed_at='%s' " \
                  "WHERE user_id='%s' AND challenge_id='%s'" % (now, user_id, challenge_id)
        conn = self.db.get_connection()
        conn.execute(command)
        conn.commit()
        conn.close()