"""
SQLite → Supabase PostgreSQL Migration Script

Run from your backend root folder AFTER setting your Supabase URL:
    export DATABASE_URL="postgresql://postgres:[password]@db.xxxx.supabase.co:5432/postgres"
    python migrate_to_supabase.py

Or on Windows:
    $env:DATABASE_URL="postgresql://postgres:[password]@db.xxxx.supabase.co:5432/postgres"
    python migrate_to_supabase.py
"""

import sqlite3
import os
import sys

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("ERROR: psycopg2 not installed. Run: pip install psycopg2-binary")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────
SQLITE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "database", "hok_lesson_data.db"
)

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable not set.")
    print("Set it with your Supabase connection string first.")
    sys.exit(1)


# ── Table definitions ─────────────────────────────────────────────────────────
TABLES = {
    "npcs": """
        CREATE TABLE IF NOT EXISTS npcs (
            npc_id TEXT PRIMARY KEY,
            npc_name TEXT
        )
    """,
    "dialogue_nodes": """
        CREATE TABLE IF NOT EXISTS dialogue_nodes (
            node_id TEXT PRIMARY KEY,
            parent_node_id TEXT,
            npc_id TEXT
        )
    """,
    "dialogues": """
        CREATE TABLE IF NOT EXISTS dialogues (
            node_id TEXT,
            dialogue_id TEXT,
            dialogue TEXT,
            translation_HAN TEXT,
            translation_POJ TEXT,
            audio_clip TEXT,
            npc_id TEXT
        )
    """,
    "words": """
        CREATE TABLE IF NOT EXISTS words (
            dialogue_id TEXT,
            word_id TEXT,
            word TEXT,
            translation TEXT,
            context TEXT,
            audio_clip TEXT,
            english_word TEXT DEFAULT ''
        )
    """,
    "options": """
        CREATE TABLE IF NOT EXISTS options (
            node_id TEXT,
            option_id TEXT,
            option_text TEXT,
            next_node_id TEXT,
            feedback_type TEXT
        )
    """,
    "events": """
        CREATE TABLE IF NOT EXISTS events (
            option_id TEXT,
            event_id TEXT,
            event_type TEXT,
            metadata TEXT
        )
    """,
    "vendors": """
        CREATE TABLE IF NOT EXISTS vendors (
            vendor_id TEXT PRIMARY KEY,
            node_id TEXT,
            npc_id TEXT,
            vendor_name TEXT
        )
    """,
    "items": """
        CREATE TABLE IF NOT EXISTS items (
            vendor_id TEXT,
            item_id TEXT,
            item_name TEXT,
            item_description TEXT,
            item_value NUMERIC
        )
    """,
    "challenges": """
        CREATE TABLE IF NOT EXISTS challenges (
            challenge_id TEXT PRIMARY KEY,
            title TEXT,
            type TEXT
        )
    """,
    "challenge_requirements": """
        CREATE TABLE IF NOT EXISTS challenge_requirements (
            challenge_id TEXT,
            target_item_id TEXT,
            target_vendor_id TEXT,
            exact_price NUMERIC,
            required_items TEXT
        )
    """,
    "user_challenges": """
        CREATE TABLE IF NOT EXISTS user_challenges (
            user_id TEXT,
            challenge_id TEXT,
            status TEXT,
            accepted_at TEXT,
            completed_at TEXT
        )
    """,
    "inventory": """
        CREATE TABLE IF NOT EXISTS inventory (
            user_id TEXT,
            item_id TEXT,
            challenge_id TEXT,
            acquired_at TEXT
        )
    """,
}


def get_sqlite_conn():
    if not os.path.isfile(SQLITE_PATH):
        print(f"ERROR: SQLite database not found at {SQLITE_PATH}")
        sys.exit(1)
    return sqlite3.connect(SQLITE_PATH)


def get_pg_conn():
    return psycopg2.connect(DATABASE_URL, sslmode='require')


def create_tables(pg_cursor):
    print("\nStep 1 — Creating tables in PostgreSQL...")
    for table_name, ddl in TABLES.items():
        try:
            pg_cursor.execute(ddl)
            print(f"  ✅ {table_name}")
        except Exception as e:
            print(f"  ❌ {table_name}: {e}")


def migrate_table(sqlite_conn, pg_cursor, table_name):
    sqlite_cursor = sqlite_conn.cursor()

    # Check if table exists in SQLite
    exists = sqlite_cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    ).fetchone()

    if not exists:
        print(f"  ⚠️  {table_name:30s} → not found in SQLite, skipping")
        return 0

    # Get all rows from SQLite
    rows = sqlite_cursor.execute(f"SELECT * FROM \"{table_name}\"").fetchall()

    if not rows:
        print(f"  ⚠️  {table_name:30s} → empty, skipping")
        return 0

    # Get column names
    col_info = sqlite_cursor.execute(
        f"PRAGMA table_info(\"{table_name}\")").fetchall()
    columns = [col[1].lower() for col in col_info]

    # Build INSERT query
    placeholders = ', '.join(['%s'] * len(columns))
    col_names = ', '.join([f'"{c}"' for c in columns])
    query = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"

    inserted = 0
    errors = 0
    for row in rows:
        try:
            pg_cursor.execute(query, row)
            inserted += 1
        except Exception as e:
            pg_cursor.connection.rollback()
            errors += 1
            if errors <= 3:  # only show first 3 errors
                print(f"    ⚠️  Row error in {table_name}: {e}")

    print(f"  ✅ {table_name:30s} → {inserted} rows inserted, {errors} errors")
    return inserted


def verify(pg_cursor):
    print("\nStep 3 — Verification...")
    for table_name in TABLES.keys():
        try:
            pg_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = pg_cursor.fetchone()[0]
            status = "✅" if count > 0 else "⚠️  EMPTY"
            print(f"  {status}  {table_name:30s} → {count} rows")
        except Exception as e:
            print(f"  ❌  {table_name:30s} → {e}")


def migrate():
    print("=" * 60)
    print("  SQLite → Supabase PostgreSQL Migration")
    print("=" * 60)
    print(f"\n  Source: {SQLITE_PATH}")
    print(f"  Target: Supabase PostgreSQL\n")

    sqlite_conn = get_sqlite_conn()
    pg_conn = get_pg_conn()
    pg_cursor = pg_conn.cursor()

    # Step 1 — Create tables
    create_tables(pg_cursor)
    pg_conn.commit()

    # Step 2 — Migrate all tables
    print("\nStep 2 — Migrating data...")
    total = 0
    for table_name in TABLES.keys():
        inserted = migrate_table(sqlite_conn, pg_cursor, table_name)
        pg_conn.commit()   #commit after each table
        total += inserted

    pg_conn.commit()

    # Step 3 — Verify
    verify(pg_cursor)

    sqlite_conn.close()
    pg_cursor.close()
    pg_conn.close()

    print(f"\n{'='*60}")
    print(f"  Migration complete! {total} total rows migrated.")
    print(f"{'='*60}")


if __name__ == "__main__":
    migrate()