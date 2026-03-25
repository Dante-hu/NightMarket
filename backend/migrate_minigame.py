"""
Migration script — adds minigame tables and test data to existing hok_test_data.db.
Run this from your backend root folder:

    python migrate_minigame.py

Safe to run multiple times — uses INSERT OR IGNORE and CREATE TABLE IF NOT EXISTS
so it will never overwrite or duplicate existing data.
"""

import sqlite3
import json
import os

# ── Config ────────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "hok_test_data.db")

def migrate():
    if not os.path.isfile(DB_PATH):
        print(f"ERROR: Database not found at {DB_PATH}")
        print("Make sure you're running this script from your backend root folder.")
        return

    print(f"Connecting to: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ── Step 1: Create new tables ─────────────────────────────────────────────
    print("\nCreating minigame tables...")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS challenges (
            challenge_id TEXT PRIMARY KEY,
            title TEXT,
            type TEXT
        )
    """)
    print("  ✅ challenges")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS challenge_requirements (
            challenge_id TEXT,
            target_item_id TEXT,
            target_vendor_id TEXT,
            exact_price REAL,
            required_items TEXT
        )
    """)
    print("  ✅ challenge_requirements")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_challenges (
            user_id TEXT,
            challenge_id TEXT,
            status TEXT,
            accepted_at TEXT,
            completed_at TEXT
        )
    """)
    print("  ✅ user_challenges")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            user_id TEXT,
            item_id TEXT,
            challenge_id TEXT,
            acquired_at TEXT
        )
    """)
    print("  ✅ inventory")

    # ── Step 2: Seed challenge data ───────────────────────────────────────────
    print("\nSeeding challenge data...")

    challenges = [
        ("ch_001", "Boba Quest",           "ORDER_SPECIFIC_ITEM"),
        ("ch_002", "Mango Madness",         "ORDER_SPECIFIC_ITEM"),
        ("ch_003", "A-Ging's Special",      "BUY_FROM_SPECIFIC_VENDOR"),
        ("ch_004", "Bubble Tea Collector",  "COLLECT_MULTIPLE_ITEMS"),
        ("ch_005", "The Full Menu",         "COLLECT_MULTIPLE_ITEMS"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO challenges VALUES (?,?,?)", challenges)
    print(f"  ✅ Inserted {cursor.rowcount} challenges (skipped duplicates)")

    # ── Step 3: Seed challenge requirements ──────────────────────────────────
    # Uses existing item IDs and vendor IDs from your db:
    #   i_001 = Taro bubble tea     ($5.99, vendor v_001)
    #   i_002 = Milk bubble tea     ($5.99, vendor v_001)
    #   i_003 = Mango bubble tea    ($5.99, vendor v_001)
    #   v_001 = A-Ging's Bubble Tea
    requirements = [
        # ch_001: order taro bubble tea for $5.99
        ("ch_001", "i_001", None,    5.99, None),

        # ch_002: order mango bubble tea for $5.99
        ("ch_002", "i_003", None,    5.99, None),

        # ch_003: buy anything from A-Ging's Bubble Tea (v_001)
        ("ch_003", None,    "v_001", None, None),

        # ch_004: collect taro AND milk bubble tea
        ("ch_004", None,    None,    None, json.dumps(["i_001", "i_002"])),

        # ch_005: collect all three bubble teas
        ("ch_005", None,    None,    None, json.dumps(["i_001", "i_002", "i_003"])),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO challenge_requirements VALUES (?,?,?,?,?)", requirements)
    print(f"  ✅ Inserted challenge requirements")

    conn.commit()

    # ── Step 4: Verify everything looks correct ───────────────────────────────
    print("\nVerifying migration...")

    print("\n  challenges table:")
    for row in cursor.execute("SELECT * FROM challenges"):
        print(f"    {row}")

    print("\n  challenge_requirements table:")
    for row in cursor.execute("SELECT * FROM challenge_requirements"):
        print(f"    {row}")

    print("\n  user_challenges table (should be empty):")
    rows = cursor.execute("SELECT * FROM user_challenges").fetchall()
    print(f"    {len(rows)} rows (empty is correct)")

    print("\n  inventory table (should be empty):")
    rows = cursor.execute("SELECT * FROM inventory").fetchall()
    print(f"    {len(rows)} rows (empty is correct)")

    print("\n  Existing tables still intact:")
    for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        print(f"    {row[0]}")

    conn.close()
    print("\n✅ Migration complete! Your existing data was not modified.")

if __name__ == "__main__":
    migrate()