"""
Database Inspection Script
Prints a readable summary of hok_lesson_data.db

Run from your backend root folder:

    # Show full summary (row counts only)
    python inspect_lesson_db.py

    # Filter by lesson
    python inspect_lesson_db.py --lesson 0
    python inspect_lesson_db.py --lesson 1

    # Filter by vendor
    python inspect_lesson_db.py --vendor v_pineapple
    python inspect_lesson_db.py --vendor v_beh_teung_guai

    # Filter by both
    python inspect_lesson_db.py --lesson 1 --vendor v_beh_teung_guai
"""

import sqlite3
import os
import sys
import json

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "database",
    "hok_lesson_data.db"
)

# ── Argument parsing ──────────────────────────────────────────────────────────
def parse_args():
    args = sys.argv[1:]
    lesson = None
    vendor = None

    if "--lesson" in args:
        idx = args.index("--lesson")
        if idx + 1 < len(args):
            lesson = args[idx + 1]

    if "--vendor" in args:
        idx = args.index("--vendor")
        if idx + 1 < len(args):
            vendor = args[idx + 1]

    return lesson, vendor


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_lesson_prefix(lesson):
    """Converts lesson number to node prefix e.g. '0' -> 'n_l0_'"""
    return f"n_l{lesson}_"


def print_header(title):
    print("\n" + "=" * 65)
    print(f" {title}")
    print("=" * 65)


def print_section(title):
    print(f"\n── {title} {'─' * (60 - len(title))}")


# ── Summary ───────────────────────────────────────────────────────────────────
def show_summary(cursor):
    print_section("Table Row Counts")
    tables = ["npcs", "vendors", "items", "dialogue_nodes",
              "dialogues", "words", "options", "events"]
    for table in tables:
        count = cursor.execute(
            f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        status = "✅" if count > 0 else "⚠️  EMPTY"
        print(f"  {status}  {table:20s} → {count} rows")


# ── NPCs ──────────────────────────────────────────────────────────────────────
def show_npcs(cursor, lesson=None, vendor_id=None):
    print_section("NPCs")

    if vendor_id:
        rows = cursor.execute("""
            SELECT n.npc_id, n.npc_name, v.vendor_id, v.vendor_name
            FROM npcs n
            JOIN vendors v ON v.npc_id = n.npc_id
            WHERE v.vendor_id = ?
        """, (vendor_id,)).fetchall()
    elif lesson is not None:
        prefix = get_lesson_prefix(lesson)
        rows = cursor.execute("""
            SELECT DISTINCT n.npc_id, n.npc_name, v.vendor_id, v.vendor_name
            FROM npcs n
            JOIN vendors v ON v.npc_id = n.npc_id
            WHERE v.node_id LIKE ?
        """, (f"{prefix}%",)).fetchall()
    else:
        rows = cursor.execute("""
            SELECT n.npc_id, n.npc_name, v.vendor_id, v.vendor_name
            FROM npcs n
            LEFT JOIN vendors v ON v.npc_id = n.npc_id
        """).fetchall()

    if not rows:
        print("  No NPCs found for this filter.")
        return

    for row in rows:
        print(f"  {row[0]:30s} | {row[1]:30s} | vendor: {row[2]}")


# ── Vendors ───────────────────────────────────────────────────────────────────
def show_vendors(cursor, lesson=None, vendor_id=None):
    print_section("Vendors & Items")

    if vendor_id:
        rows = cursor.execute(
            "SELECT * FROM vendors WHERE vendor_id = ?",
            (vendor_id,)).fetchall()
    elif lesson is not None:
        prefix = get_lesson_prefix(lesson)
        rows = cursor.execute(
            "SELECT * FROM vendors WHERE node_id LIKE ?",
            (f"{prefix}%",)).fetchall()
    else:
        rows = cursor.execute("SELECT * FROM vendors").fetchall()

    if not rows:
        print("  No vendors found for this filter.")
        return

    for v in rows:
        print(f"\n  🏪 {v[3]} ({v[0]})")
        print(f"     NPC        : {v[2]}")
        print(f"     Entry node : {v[1]}")

        items = cursor.execute(
            "SELECT * FROM items WHERE vendor_id = ?",
            (v[0],)).fetchall()
        if items:
            print(f"     Items:")
            for item in items:
                print(f"       - [{item[1]}] {item[2]} | ${item[4]}")
                print(f"         {item[3]}")
        else:
            print(f"     Items: none (non-vendor NPC)")


# ── Dialogue Flow ─────────────────────────────────────────────────────────────
def show_dialogue_flow(cursor, lesson=None, vendor_id=None):
    print_section("Dialogue Flow")

    if vendor_id:
        vendors = cursor.execute(
            "SELECT vendor_id, vendor_name, npc_id, node_id FROM vendors WHERE vendor_id = ?",
            (vendor_id,)).fetchall()
    elif lesson is not None:
        prefix = get_lesson_prefix(lesson)
        vendors = cursor.execute(
            "SELECT vendor_id, vendor_name, npc_id, node_id FROM vendors WHERE node_id LIKE ?",
            (f"{prefix}%",)).fetchall()
    else:
        vendors = cursor.execute(
            "SELECT vendor_id, vendor_name, npc_id, node_id FROM vendors").fetchall()

    if not vendors:
        print("  No vendors found for this filter.")
        return

    for vendor in vendors:
        v_id, v_name, npc_id, entry_node = vendor
        print(f"\n  ┌─ {v_name} ({v_id})")
        print(f"  │  NPC: {npc_id} | Entry: {entry_node}")

        nodes = cursor.execute("""
            SELECT node_id, parent_node_id
            FROM dialogue_nodes
            WHERE npc_id = ?
            ORDER BY node_id
        """, (npc_id,)).fetchall()

        for node in nodes:
            node_id, parent_id = node

            dialogue = cursor.execute("""
                SELECT dialogue_id, dialogue, translation_HAN
                FROM dialogues WHERE node_id = ?
            """, (node_id,)).fetchone()

            print(f"  │")
            print(f"  ├── Node    : {node_id}")
            print(f"  │   Parent  : {parent_id}")

            if dialogue:
                print(f"  │   ID      : {dialogue[0]}")
                print(f"  │   EN      : {dialogue[1]}")
                print(f"  │   HK      : {dialogue[2]}")

                keywords = cursor.execute("""
                    SELECT word, translation, conTEXT
                    FROM words WHERE dialogue_id = ?
                """, (dialogue[0],)).fetchall()
                if keywords:
                    print(f"  │   Keywords:")
                    for kw in keywords:
                        print(f"  │     🔑 {kw[0]:25s} = {kw[1]}")
                        if kw[2]:
                            print(f"  │        📝 {kw[2]}")
            else:
                print(f"  │   ⚠️  NO DIALOGUE FOUND")

            options = cursor.execute("""
                SELECT option_id, option_TEXT, next_node_id, feedback_type
                FROM options WHERE node_id = ?
            """, (node_id,)).fetchall()
            if options:
                print(f"  │   Options:")
                for opt in options:
                    print(f"  │     → {opt[1]}")
                    print(f"  │       next: {opt[2]} | {opt[3]}")

                    events = cursor.execute("""
                        SELECT event_type, metadata
                        FROM events WHERE option_id = ?
                    """, (opt[0],)).fetchall()
                    for evt in events:
                        try:
                            meta = json.loads(evt[1])
                        except:
                            meta = evt[1]
                        print(f"  │       ⚡ {evt[0]}: {meta}")

        print(f"  └─ End of {v_name}")


# ── Main ──────────────────────────────────────────────────────────────────────
def inspect():
    if not os.path.isfile(DB_PATH):
        print(f"ERROR: Database not found at {DB_PATH}")
        print("Make sure you're running from your backend root folder.")
        return

    lesson, vendor_id = parse_args()

    title = "DATABASE INSPECTION — hok_lesson_data.db"
    if lesson is not None:
        title += f" | Lesson {lesson}"
    if vendor_id:
        title += f" | Vendor: {vendor_id}"

    print_header(title)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    show_summary(cursor)
    show_npcs(cursor, lesson, vendor_id)
    show_vendors(cursor, lesson, vendor_id)
    show_dialogue_flow(cursor, lesson, vendor_id)

    conn.close()
    print("\n" + "=" * 65)
    print(" Inspection complete!")
    print("=" * 65)


if __name__ == "__main__":
    inspect()