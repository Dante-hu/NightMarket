"""
Lesson 1 Population Script — ORDERING SNACKS
Adds Lesson 1 content to hok_lesson_data.db.

Run from your backend root folder:
    python populate_lesson_1.py

IMPORTANT: Run populate_lesson_0.py first before this script.

Lesson 1 Overview:
    - Player independently interacts with multiple vendors
    - No more guided tutorial style
    - Learning objectives:
        * Greet vendors (老板好)
        * Ask what food is (请问这是什么？)
        * Ask how food is sold (怎么卖？)
        * Order a quantity (我要一个 / 我要三个)

Vendors (4 stalls, all follow same structure):
    1. 白糖粿 Fried Sweet Rice Cake (Beh Teung Guai)
    2. 红豆饼 Red Bean Pancake (kóng-á-kér)
    3. 地瓜球 Sweet Potato Balls
    [optional 4th stall for variety]

Dialogue structure per vendor (same pattern for all):
    [1] Player greets vendor
        老板好！
    [2] Player asks what it is
        请问这是什么？
    [3] Vendor explains + price
        这是白糖粿。五块一个或十二块三个。
    [4] Player asks how it is sold
        怎么卖？
    [5] Vendor gives price options
        五块一个或十二块三个。
    [6] Player orders
        Option A: 我要一个 ($5)
        Option B: 我要三个 ($12)
    [7] Vendor completes sale
        好的，来！

Mini challenge at end:
    Buy 2 different snacks with no English guidance
"""

import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "database",
    "hok_lesson_data.db"
)

def check_db():
    """Make sure the db exists before running."""
    if not os.path.isfile(DB_PATH):
        print("ERROR: hok_lesson_data.db not found.")
        print("Please run populate_lesson_0.py first.")
        return False
    return True


def populate_npcs(cursor):
    npcs = [
        ("npc_beh_teung_guai",  "Fried Sweet Rice Cake Vendor"),
        ("npc_red_bean_pancake", "Red Bean Pancake Vendor"),
        ("npc_sweet_potato",    "Sweet Potato Ball Vendor"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO npcs VALUES (?,?)", npcs)
    print(f"   Inserted {len(npcs)} NPCs")


def populate_vendors(cursor):
    vendors = [
        ("v_beh_teung_guai",  "n_l1_v1_greet", "npc_beh_teung_guai",  "白糖粿 Stall"),
        ("v_red_bean_pancake", "n_l1_v2_greet", "npc_red_bean_pancake","红豆饼 Stall"),
        ("v_sweet_potato",    "n_l1_v3_greet", "npc_sweet_potato",    "地瓜球 Stall"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO vendors VALUES (?,?,?,?)", vendors)
    print(f"   Inserted {len(vendors)} vendors")


def populate_items(cursor):
    items = [
        # 白糖粿 — $5 for 1, $12 for 3
        ("v_beh_teung_guai", "i_beh_teung_guai_1",
         "白糖粿 (Fried Sweet Rice Cake)",
         "A chewy fried sweet rice cake coated in sugar. "
         "A classic Taiwanese street snack with a crispy outside.",
         5),

        # 红豆饼 — $5 for 1, $12 for 3
        ("v_red_bean_pancake", "i_red_bean_pancake_1",
         "红豆饼 (Red Bean Pancake)",
         "A fluffy pancake filled with sweet red bean paste. "
         "Also known as 管仔粿 (kóng-á-kér) in Hokkien.",
         5),

        # 地瓜球 — $5 for 1 bag, $12 for 3 bags
        ("v_sweet_potato", "i_sweet_potato_1",
         "地瓜球 (Sweet Potato Balls)",
         "Crispy golden balls made from sweet potato and tapioca. "
         "Light and hollow inside, chewy on the outside.",
         5),
    ]
    cursor.executemany("INSERT OR IGNORE INTO items VALUES (?,?,?,?,?)", items)
    print(f"   Inserted {len(items)} items")


def populate_dialogue_nodes(cursor):
    """
    All three vendors follow the exact same node structure.
    Prefix: n_l1_v1 = lesson 1, vendor 1 (白糖粿)
            n_l1_v2 = lesson 1, vendor 2 (红豆饼)
            n_l1_v3 = lesson 1, vendor 3 (地瓜球)

    Per vendor:
        _greet    → player greets vendor
        _whatis   → player asks what it is
        _explain  → vendor explains dish
        _howsold  → player asks how it is sold
        _price    → vendor gives price options
        _order    → player orders (branches: 1 or 3)
        _complete → vendor completes sale
    """
    nodes = [
        # ── Vendor 1: 白糖粿 ──────────────────────────────────────────
        ("n_l1_v1_greet",    "n_000",          "npc_beh_teung_guai"),
        ("n_l1_v1_whatis",   "n_l1_v1_greet",  "npc_beh_teung_guai"),
        ("n_l1_v1_explain",  "n_l1_v1_whatis", "npc_beh_teung_guai"),
        ("n_l1_v1_howsold",  "n_l1_v1_explain","npc_beh_teung_guai"),
        ("n_l1_v1_price",    "n_l1_v1_howsold","npc_beh_teung_guai"),
        ("n_l1_v1_complete", "n_l1_v1_price",  "npc_beh_teung_guai"),

        # ── Vendor 2: 红豆饼 ──────────────────────────────────────────
        ("n_l1_v2_greet",    "n_000",          "npc_red_bean_pancake"),
        ("n_l1_v2_whatis",   "n_l1_v2_greet",  "npc_red_bean_pancake"),
        ("n_l1_v2_explain",  "n_l1_v2_whatis", "npc_red_bean_pancake"),
        ("n_l1_v2_howsold",  "n_l1_v2_explain","npc_red_bean_pancake"),
        ("n_l1_v2_price",    "n_l1_v2_howsold","npc_red_bean_pancake"),
        ("n_l1_v2_complete", "n_l1_v2_price",  "npc_red_bean_pancake"),

        # ── Vendor 3: 地瓜球 ──────────────────────────────────────────
        ("n_l1_v3_greet",    "n_000",          "npc_sweet_potato"),
        ("n_l1_v3_whatis",   "n_l1_v3_greet",  "npc_sweet_potato"),
        ("n_l1_v3_explain",  "n_l1_v3_whatis", "npc_sweet_potato"),
        ("n_l1_v3_howsold",  "n_l1_v3_explain","npc_sweet_potato"),
        ("n_l1_v3_price",    "n_l1_v3_howsold","npc_sweet_potato"),
        ("n_l1_v3_complete", "n_l1_v3_price",  "npc_sweet_potato"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO dialogue_nodes VALUES (?,?,?)", nodes)
    print(f"   Inserted {len(nodes)} dialogue nodes")


def populate_dialogues(cursor):
    """
    dialogue   = English text
    translation = Hokkien/Chinese text
    """
    dialogues = [
        # ── Vendor 1: 白糖粿 (Fried Sweet Rice Cake) ─────────────────

        ("n_l1_v1_greet", "d_l1_v1_001",
         "Hello!",
         "老板好！",
         "", "npc_beh_teung_guai"),

        ("n_l1_v1_whatis", "d_l1_v1_002",
         "Excuse me, what is this?",
         "请问这是什么？",
         "", "npc_beh_teung_guai"),

        ("n_l1_v1_explain", "d_l1_v1_003",
         "This is fried sweet rice cake!",
         "这是白糖粿！",
         "", "npc_beh_teung_guai"),

        ("n_l1_v1_howsold", "d_l1_v1_004",
         "How do you sell this?",
         "怎么卖？",
         "", "npc_beh_teung_guai"),

        ("n_l1_v1_price", "d_l1_v1_005",
         "$5 for one or $12 for three.",
         "五块一个或十二块三个。",
         "", "npc_beh_teung_guai"),

        ("n_l1_v1_complete", "d_l1_v1_006",
         "Here you go! Enjoy!",
         "来，请慢用！",
         "", "npc_beh_teung_guai"),

        # ── Vendor 2: 红豆饼 (Red Bean Pancake) ──────────────────────

        ("n_l1_v2_greet", "d_l1_v2_001",
         "Hello!",
         "老板好！",
         "", "npc_red_bean_pancake"),

        ("n_l1_v2_whatis", "d_l1_v2_002",
         "Excuse me, what is this?",
         "请问这是什么？",
         "", "npc_red_bean_pancake"),

        ("n_l1_v2_explain", "d_l1_v2_003",
         "This is red bean pancake!",
         "这是红豆饼！",
         "", "npc_red_bean_pancake"),

        ("n_l1_v2_howsold", "d_l1_v2_004",
         "How do you sell this?",
         "怎么卖？",
         "", "npc_red_bean_pancake"),

        ("n_l1_v2_price", "d_l1_v2_005",
         "$5 for one or $12 for three.",
         "五块一个或十二块三个。",
         "", "npc_red_bean_pancake"),

        ("n_l1_v2_complete", "d_l1_v2_006",
         "Here you go! Enjoy!",
         "来，请慢用！",
         "", "npc_red_bean_pancake"),

        # ── Vendor 3: 地瓜球 (Sweet Potato Balls) ────────────────────

        ("n_l1_v3_greet", "d_l1_v3_001",
         "Hello!",
         "老板好！",
         "", "npc_sweet_potato"),

        ("n_l1_v3_whatis", "d_l1_v3_002",
         "Excuse me, what is this?",
         "请问这是什么？",
         "", "npc_sweet_potato"),

        ("n_l1_v3_explain", "d_l1_v3_003",
         "This is sweet potato balls!",
         "这是地瓜球！",
         "", "npc_sweet_potato"),

        ("n_l1_v3_howsold", "d_l1_v3_004",
         "How do you sell this?",
         "怎么卖？",
         "", "npc_sweet_potato"),

        ("n_l1_v3_price", "d_l1_v3_005",
         "$5 for one or $12 for three.",
         "五块一个或十二块三个。",
         "", "npc_sweet_potato"),

        ("n_l1_v3_complete", "d_l1_v3_006",
         "Here you go! Enjoy!",
         "来，请慢用！",
         "", "npc_sweet_potato"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO dialogues VALUES (?,?,?,?,?,?)", dialogues)
    print(f"   Inserted {len(dialogues)} dialogue lines")


def populate_words(cursor):
    """
    New vocab introduced in Lesson 1.
    Reuses some from Lesson 0 (老板好, 请问这是什么) but also
    introduces new keywords: 怎么卖, 我要一个, 我要三个, dish names.
    """
    words = [
        # ── Vendor 1 keywords ─────────────────────────────────────────

        # d_l1_v1_001 — 老板好！(already taught in L0, reinforce here)
        ("d_l1_v1_001", "w_l1_001",
         "老板好", "Hello vendor / Hello boss (lāu-pán hó)",
         "Standard greeting when approaching a vendor at the night market",
         ""),

        # d_l1_v1_002 — 请问这是什么？
        ("d_l1_v1_002", "w_l1_002",
         "请问这是什么", "Excuse me, what is this?",
         "Key phrase for asking about an unfamiliar dish",
         ""),

        # d_l1_v1_003 — 这是白糖粿
        ("d_l1_v1_003", "w_l1_003",
         "白糖粿", "Fried Sweet Rice Cake (Beh Teung Guai)",
         "A chewy Taiwanese street snack made from glutinous rice flour",
         ""),

        # d_l1_v1_004 — 怎么卖？(NEW in Lesson 1)
        ("d_l1_v1_004", "w_l1_004",
         "怎么卖", "How do you sell this? / How much is it sold for?",
         "Used to ask about pricing and quantity at a vendor stall",
         ""),

        # d_l1_v1_005 — 五块一个或十二块三个
        ("d_l1_v1_005", "w_l1_005",
         "五块", "$5 / Five dollars (gō͘ kho)",
         "Common price unit at night market stalls",
         ""),
        ("d_l1_v1_005", "w_l1_006",
         "十二块", "$12 / Twelve dollars",
         "Combo price — usually cheaper per unit than buying individually",
         ""),

        # ── Vendor 2 keywords ─────────────────────────────────────────

        # d_l1_v2_003 — 这是红豆饼
        ("d_l1_v2_003", "w_l1_007",
         "红豆饼", "Red Bean Pancake (kóng-á-kér)",
         "A popular Taiwanese pancake filled with sweet red bean paste",
         ""),

        # d_l1_v2_004 — 怎么卖？(reinforce)
        ("d_l1_v2_004", "w_l1_008",
         "怎么卖", "How do you sell this?",
         "Used to ask about pricing at a vendor stall",
         ""),

        # ── Vendor 3 keywords ─────────────────────────────────────────

        # d_l1_v3_003 — 这是地瓜球
        ("d_l1_v3_003", "w_l1_009",
         "地瓜球", "Sweet Potato Balls",
         "Crispy golden balls made from sweet potato and tapioca starch",
         ""),

        # d_l1_v3_004 — 怎么卖？(reinforce again)
        ("d_l1_v3_004", "w_l1_010",
         "怎么卖", "How do you sell this?",
         "Used to ask about pricing at a vendor stall",
         ""),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO words VALUES (?,?,?,?,?,?)", words)
    print(f"   Inserted {len(words)} keyword vocabulary entries")


def populate_options(cursor):
    """
    Each vendor has the same branching structure:
    After vendor gives price → player picks quantity (1 or 3)
    """
    options = []

    for v in ["v1", "v2", "v3"]:
        # After vendor explains dish — player asks how it's sold
        options.append((
            f"n_l1_{v}_explain", f"o_l1_{v}_001",
            "How do you sell this? / 怎么卖？",
            f"n_l1_{v}_howsold", "positive"
        ))

        # After vendor gives price — player orders 1
        options.append((
            f"n_l1_{v}_price", f"o_l1_{v}_002",
            "I'll take one. / 我要一个。",
            f"n_l1_{v}_complete", "positive"
        ))

        # After vendor gives price — player orders 3
        options.append((
            f"n_l1_{v}_price", f"o_l1_{v}_003",
            "I'll take three. / 我要三个。",
            f"n_l1_{v}_complete", "positive"
        ))

    cursor.executemany(
        "INSERT OR IGNORE INTO options VALUES (?,?,?,?,?)", options)
    print(f"   Inserted {len(options)} dialogue options")


def populate_events(cursor):
    """
    ADD_TO_INVENTORY fires when player orders from each vendor.
    """
    events = [
        # Vendor 1 — 白糖粿
        ("o_l1_v1_002", "e_l1_001",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_beh_teung_guai_1", "quantity": 1}'),
        ("o_l1_v1_003", "e_l1_002",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_beh_teung_guai_1", "quantity": 3}'),

        # Vendor 2 — 红豆饼
        ("o_l1_v2_002", "e_l1_003",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_red_bean_pancake_1", "quantity": 1}'),
        ("o_l1_v2_003", "e_l1_004",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_red_bean_pancake_1", "quantity": 3}'),

        # Vendor 3 — 地瓜球
        ("o_l1_v3_002", "e_l1_005",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_sweet_potato_1", "quantity": 1}'),
        ("o_l1_v3_003", "e_l1_006",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_sweet_potato_1", "quantity": 3}'),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO events VALUES (?,?,?,?)", events)
    print(f"   Inserted {len(events)} events")


def verify(cursor):
    print("\n── Verification ─────────────────────────────────────────────")
    tables = ["npcs", "vendors", "items", "dialogue_nodes",
              "dialogues", "words", "options", "events"]
    for table in tables:
        count = cursor.execute(
            f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table:20s} → {count} total rows")

    print("\n── Lesson 1 Dialogue Flow Sample (Vendor 1) ─────────────────")
    rows = cursor.execute("""
        SELECT node_id, dialogue, translation
        FROM dialogues
        WHERE node_id LIKE 'n_l1_v1%'
        ORDER BY dialogue_id
    """).fetchall()
    for row in rows:
        print(f"\n  [{row[0]}]")
        print(f"  EN: {row[1]}")
        print(f"  HK: {row[2]}")

        opts = cursor.execute(
            "SELECT option_TEXT, next_node_id FROM options WHERE node_id=?",
            (row[0],)).fetchall()
        for opt in opts:
            print(f"  → Option: {opt[0]} | next: {opt[1]}")


def populate():
    if not check_db():
        return

    print(f"Connecting to: {DB_PATH}\n")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Step 1 — Populating NPCs...")
    populate_npcs(cursor)

    print("\nStep 2 — Populating vendors...")
    populate_vendors(cursor)

    print("\nStep 3 — Populating items...")
    populate_items(cursor)

    print("\nStep 4 — Populating dialogue nodes...")
    populate_dialogue_nodes(cursor)

    print("\nStep 5 — Populating dialogues...")
    populate_dialogues(cursor)

    print("\nStep 6 — Populating vocabulary keywords...")
    populate_words(cursor)

    print("\nStep 7 — Populating player options...")
    populate_options(cursor)

    print("\nStep 8 — Populating events...")
    populate_events(cursor)

    conn.commit()

    print("\nStep 9 — Verifying data...")
    verify(cursor)

    conn.close()
    print("\n Lesson 1 population complete!")
    print(f"   Database: {DB_PATH}")


if __name__ == "__main__":
    populate()