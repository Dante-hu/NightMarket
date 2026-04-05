"""
Lesson 0 Population Script — NIGHT MARKET AT FIRST TASTE
Creates hok_lesson_data.db and populates it with Lesson 0 content.

Run from your backend root folder:
    python populate_lesson_0.py

Table structure (matches existing hok_db schema):
    npcs          (npc_id, npc_name)
    dialogue_nodes (node_id, parent_node_id, npc_id)
    dialogues      (node_id, dialogue_id, dialogue[EN], translation[HOK], audio_clip, npc_id)
    words          (dialogue_id, word_id, word[HOK], translation[EN], context, audio_clip)
    options        (node_id, option_id, option_TEXT, next_node_id, feedback_type)
    events         (option_id, event_id, event_type, metadata)
    vendors        (vendor_id, node_id, npc_id, vendor_name)
    items          (vendor_id, item_id, item_name, item_description, item_value)

Lesson 0 Dialogue Flow:
    [1] Arrival narration
    [2] Passerby interaction
        - Excuse me, what is this?
        - Passerby: This is pineapple cake
        - Where did you buy it?
        - Passerby: points to vendor
    [3] First vendor (Pineapple Cake Vendor)
        - Greet vendor
        - Ask what is this
        - Vendor: This is pineapple cake. Would you like to try one?
            - Yes → [4]
            - No  → Vendor urges → [4]
    [4] First purchase
        - How many would you like? (1, 2, 3)
        - Vendor: Here you go!
    [5] Completion narration
"""

import sqlite3
import os

# ── Config 
DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "database",
    "hok_lesson_data.db"
)

def create_tables(cursor):
    """Creates all tables matching the existing hok_db schema."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS npcs (
            npc_id TEXT PRIMARY KEY,
            npc_name TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dialogue_nodes (
            node_id TEXT PRIMARY KEY,
            parent_node_id TEXT,
            npc_id TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dialogues (
            node_id TEXT,
            dialogue_id TEXT,
            dialogue TEXT,
            translation_HAN TEXT,
            translation_POJ TEXT,
            audio_clip TEXT,
            npc_id TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            dialogue_id TEXT,
            word_id TEXT,
            word TEXT,
            translation TEXT,
            conTEXT TEXT,
            audio_clip TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS options (
            node_id TEXT,
            option_id TEXT,
            option_TEXT TEXT,
            next_node_id TEXT,
            feedback_type TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            option_id TEXT,
            event_id TEXT,
            event_type TEXT,
            metadata TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendors (
            vendor_id TEXT PRIMARY KEY,
            node_id TEXT,
            npc_id TEXT,
            vendor_name TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            vendor_id TEXT,
            item_id TEXT,
            item_name TEXT,
            item_description TEXT,
            item_value INTEGER
        )
    """)
    print("   All tables created")


def populate_npcs(cursor):
    """
    Lesson 0 NPCs:
    - Passerby
    - Pineapple Cake Vendor
    - (optional) Mochi Vendor
    """
    npcs = [
        ("npc_passerby",        "Passerby"),
        ("npc_pineapple_vendor","Pineapple Cake Vendor"),
        ("npc_mochi_vendor",    "Mochi Vendor"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO npcs VALUES (?,?)", npcs)
    print(f"   Inserted {len(npcs)} NPCs")


def populate_vendors(cursor):
    """
    Vendors map to NPCs and their entry dialogue node.
    vendor_id, node_id (entry point), npc_id, vendor_name

    Note: Passerby is added as a fake vendor with no items.
    This allows NPC.cs to fetch their profile the same way as
    real vendors without any code changes needed.
    """
    vendors = [
        # Passerby — no items, just a dialogue entry point
        ("v_passerby",  "n_l0_pb_root",  "npc_passerby",         "Passerby"),
        # Real vendors
        ("v_pineapple", "n_l0_v1_greet", "npc_pineapple_vendor", "Pineapple Cake Stall"),
        ("v_mochi",     "n_l0_v2_greet", "npc_mochi_vendor",     "Mochi Stall"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO vendors VALUES (?,?,?,?)", vendors)
    print(f"    Inserted {len(vendors)} vendors")


def populate_items(cursor):
    """
    Items sold at each vendor stall.
    vendor_id, item_id, item_name, item_description, item_value
    """
    items = [
        # Pineapple cake — priced per piece
        ("v_pineapple", "i_pineapple_1",
         "凤梨酥 (Pineapple Cake)",
         "A classic Taiwanese pastry filled with sweet pineapple jam. "
         "Crispy on the outside, soft and tangy on the inside.",
         20),

        # Mochi — priced per piece
        ("v_mochi", "i_mochi_1",
         "麻吉 (Mochi)",
         "Soft and chewy Japanese-style rice cake. "
         "Popular in Taiwan with various sweet fillings.",
         15),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO items VALUES (?,?,?,?,?)", items)
    print(f"    Inserted {len(items)} items")


def populate_dialogue_nodes(cursor):
    """
    Dialogue node tree for Lesson 0.

    n_000 = virtual root (parent of all lesson root nodes)

    Passerby branch:
        n_l0_pb_root     → passerby greeting / what is this?
        n_l0_pb_answer   → passerby answers: this is pineapple cake
        n_l0_pb_where    → player asks: where did you buy it?
        n_l0_pb_point    → passerby points to vendor

    Pineapple Cake Vendor branch:
        n_l0_v1_greet    → player greets vendor
        n_l0_v1_whatis   → vendor explains what it is
        n_l0_v1_tryone   → vendor asks: would you like to try one?
        n_l0_v1_yes      → player says yes → goes to purchase
        n_l0_v1_no       → player says no → vendor urges → goes to purchase
        n_l0_v1_howmany  → vendor asks: how many would you like?
        n_l0_v1_purchase → vendor: here you go! + narration
        n_l0_complete    → lesson complete narration
    """
    nodes = [
        # Passerby branch
        ("n_l0_pb_root",    "n_000",         "npc_passerby"),
        ("n_l0_pb_answer",  "n_l0_pb_root",  "npc_passerby"),
        ("n_l0_pb_where",   "n_l0_pb_answer","npc_passerby"),
        ("n_l0_pb_point",   "n_l0_pb_where", "npc_passerby"),

        # Pineapple Cake Vendor branch
        ("n_l0_v1_greet",   "n_000",             "npc_pineapple_vendor"),
        ("n_l0_v1_whatis",  "n_l0_v1_greet",     "npc_pineapple_vendor"),
        ("n_l0_v1_tryone",  "n_l0_v1_whatis",    "npc_pineapple_vendor"),
        ("n_l0_v1_yes",     "n_l0_v1_tryone",    "npc_pineapple_vendor"),
        ("n_l0_v1_no",      "n_l0_v1_tryone",    "npc_pineapple_vendor"),
        ("n_l0_v1_howmany", "n_l0_v1_yes",       "npc_pineapple_vendor"),
        ("n_l0_v1_purchase","n_l0_v1_howmany",   "npc_pineapple_vendor"),
        ("n_l0_complete",   "n_l0_v1_purchase",  "npc_pineapple_vendor"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO dialogue_nodes VALUES (?,?,?)", nodes)
    print(f"    Inserted {len(nodes)} dialogue nodes")


def populate_dialogues(cursor):
    """
    Dialogue lines for each node.
    node_id, dialogue_id, dialogue[EN], translation[HOK], audio_clip, npc_id

    dialogue   = English text
    translation = Hokkien/Chinese text
    """
    dialogues = [
        # ── Passerby branch ───────────────────────────────────────────────────

        # [2] Player notices passerby eating a snack
        # Player speaks first — asks what it is
        (
            "n_l0_pb_root", "d_l0_pb_001",
            "Excuse me, what is this?",
            "麻烦问一下这个是什么？",
            "", "", "npc_passerby"
        ),

        # Passerby answers
        (
            "n_l0_pb_answer", "d_l0_pb_002",
            "This is pineapple cake.",
            "这是凤梨酥。",
            "", "", "npc_passerby"
        ),

        # Player asks where they bought it
        (
            "n_l0_pb_where", "d_l0_pb_003",
            "Where did you buy it?",
            "请问你在哪里买的？",
            "", "", "npc_passerby"
        ),

        # Passerby points to the vendor
        (
            "n_l0_pb_point", "d_l0_pb_004",
            "Over there at that stall!",
            "就在那边那个摊位！",
            "", "", "npc_passerby"
        ),

        # ── Pineapple Cake Vendor branch ──────────────────────────────────────

        # [3] Player approaches vendor and greets them
        (
            "n_l0_v1_greet", "d_l0_v1_001",
            "Hello!",
            "老板好！",
            "", "", "npc_pineapple_vendor"
        ),

        # Player asks what it is
        (
            "n_l0_v1_whatis", "d_l0_v1_002",
            "Excuse me, what is this?",
            "请问这是什么？",
            "", "", "npc_pineapple_vendor"
        ),

        # Vendor explains
        (
            "n_l0_v1_tryone", "d_l0_v1_003",
            "This is pineapple cake! Would you like to try one?",
            "这是凤梨酥！你要不要试吃看看？",
            "", "", "npc_pineapple_vendor"
        ),

        # Player says yes
        (
            "n_l0_v1_yes", "d_l0_v1_004",
            "Yes please!",
            "好啊！",
            "", "", "npc_pineapple_vendor"
        ),

        # Player says no — vendor urges them
        (
            "n_l0_v1_no", "d_l0_v1_005",
            "You must try it! It is Taiwan's pride!",
            "你一定要试试看！台湾的骄傲！",
            "", "", "npc_pineapple_vendor"
        ),

        # [4] Vendor asks how many
        (
            "n_l0_v1_howmany", "d_l0_v1_006",
            "How many would you like?",
            "你要几个？",
            "", "", "npc_pineapple_vendor"
        ),

        # Vendor gives the item
        (
            "n_l0_v1_purchase", "d_l0_v1_007",
            "Here you go! Enjoy!",
            "来，请慢用！",
            "", "", "npc_pineapple_vendor"
        ),

        # [5] Lesson complete narration (no NPC, narration box)
        (
            "n_l0_complete", "d_l0_complete_001",
            "Lesson 0 Complete! You have successfully bought your first Taiwanese snack! "
            "Unlocked: Lesson 1 – Ordering Street Snacks.",
            "第零课完成！你成功买到了你的第一个台湾小吃！",
            "", "", "npc_pineapple_vendor"
        ),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO dialogues VALUES (?,?,?,?,?,?,?)", dialogues)
    print(f"   Inserted {len(dialogues)} dialogue lines")


def populate_words(cursor):
    """
    Keyword vocabulary for each dialogue.
    dialogue_id, word_id, word[HOK/ZH], translation[EN], context, audio_clip

    These are the highlighted/hoverable keywords shown in the dialogue text.
    """
    words = [
        # d_l0_pb_001 — 麻烦问一下这个是什么？
        ("d_l0_pb_001", "w_l0_001",
         "麻烦问一下", "Excuse me / May I ask",
         "Polite way to get someone's attention before asking a question",
         ""),
        ("d_l0_pb_001", "w_l0_002",
         "这个是什么", "What is this",
         "Used to ask about an unfamiliar object or food",
         ""),

        # d_l0_pb_002 — 这是凤梨酥
        ("d_l0_pb_002", "w_l0_003",
         "凤梨酥", "Pineapple Cake (ông-lâi-soo)",
         "A classic Taiwanese pastry, often given as a gift",
         ""),

        # d_l0_pb_003 — 请问你在哪里买的？
        ("d_l0_pb_003", "w_l0_004",
         "请问", "Excuse me / May I ask",
         "Polite opener used before asking a question",
         ""),
        ("d_l0_pb_003", "w_l0_005",
         "在哪里买", "Where to buy",
         "Used to ask about the location of a purchase",
         ""),

        # d_l0_v1_001 — 老板好！
        ("d_l0_v1_001", "w_l0_006",
         "老板好", "Hello boss / Hello vendor (lāu-pán hó)",
         "Common greeting used when approaching a vendor or shop owner",
         ""),

        # d_l0_v1_002 — 请问这是什么？
        ("d_l0_v1_002", "w_l0_007",
         "请问这是什么", "Excuse me, what is this?",
         "Standard phrase for asking about an unfamiliar dish or item",
         ""),

        # d_l0_v1_003 — 这是凤梨酥！你要不要试吃看看？
        ("d_l0_v1_003", "w_l0_008",
         "试吃", "Try eating / Taste test",
         "Vendors often offer free samples at night market stalls",
         ""),

        # d_l0_v1_004 — 好啊！
        ("d_l0_v1_004", "w_l0_009",
         "好啊", "Yes / Sure / Okay",
         "Casual affirmative response",
         ""),

        # d_l0_v1_005 — 台湾的骄傲
        ("d_l0_v1_005", "w_l0_010",
         "台湾的骄傲", "Taiwan's pride",
         "Expression used to describe something quintessentially Taiwanese",
         ""),

        # d_l0_v1_006 — 你要几个？
        ("d_l0_v1_006", "w_l0_011",
         "你要几个", "How many do you want?",
         "Used by vendors when asking for quantity",
         ""),

        # d_l0_v1_007 — 来，请慢用！
        ("d_l0_v1_007", "w_l0_012",
         "请慢用", "Please enjoy your meal / Bon appétit",
         "Polite phrase used when serving food",
         ""),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO words VALUES (?,?,?,?,?,?)", words)
    print(f"   Inserted {len(words)} keyword vocabulary entries")


def populate_options(cursor):
    """
    Dialogue options (player choices) for branching nodes.
    node_id, option_id, option_TEXT, next_node_id, feedback_type
    """
    options = [
        # After passerby says "This is pineapple cake"
        # Player can ask where they bought it
        (
            "n_l0_pb_answer", "o_l0_pb_001",
            "Where did you buy it? / 请问你在哪里买的？",
            "n_l0_pb_where", "positive"
        ),

        # After vendor asks "Would you like to try one?"
        # Option 1: Yes
        (
            "n_l0_v1_tryone", "o_l0_v1_001",
            "Yes please! / 好啊！",
            "n_l0_v1_howmany", "positive"
        ),
        # Option 2: No (vendor urges, then continues)
        (
            "n_l0_v1_tryone", "o_l0_v1_002",
            "No thank you. / 不用了，谢谢。",
            "n_l0_v1_no", "neutral"
        ),

        # After vendor urges (no path) — only one option: continue
        (
            "n_l0_v1_no", "o_l0_v1_003",
            "Okay, I will try one. / 好，我试一个。",
            "n_l0_v1_howmany", "positive"
        ),

        # After vendor asks how many — player picks quantity
        (
            "n_l0_v1_howmany", "o_l0_v1_004",
            "One please. / 我要一个。",
            "n_l0_v1_purchase", "positive"
        ),
        (
            "n_l0_v1_howmany", "o_l0_v1_005",
            "Two please. / 我要两个。",
            "n_l0_v1_purchase", "positive"
        ),
        (
            "n_l0_v1_howmany", "o_l0_v1_006",
            "Three please. / 我要三个。",
            "n_l0_v1_purchase", "positive"
        ),

        # After purchase — lesson complete
        (
            "n_l0_v1_purchase", "o_l0_complete_001",
            "Continue",
            "n_l0_complete", "positive"
        ),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO options VALUES (?,?,?,?,?)", options)
    print(f"   Inserted {len(options)} dialogue options")


def populate_events(cursor):
    """
    Events triggered by specific options.
    option_id, event_id, event_type, metadata

    Event types used:
    - LESSON_COMPLETE    → triggers lesson 0 completion
    - ADD_TO_INVENTORY   → adds item to player inventory
    - UNLOCK_LESSON      → unlocks next lesson
    """
    events = [
        # Buying 1 pineapple cake
        (
            "o_l0_v1_004", "e_l0_001",
            "ADD_TO_INVENTORY",
            '{"item_id": "i_pineapple_1", "quantity": 1}'
        ),
        # Buying 2 pineapple cakes
        (
            "o_l0_v1_005", "e_l0_002",
            "ADD_TO_INVENTORY",
            '{"item_id": "i_pineapple_1", "quantity": 2}'
        ),
        # Buying 3 pineapple cakes
        (
            "o_l0_v1_006", "e_l0_003",
            "ADD_TO_INVENTORY",
            '{"item_id": "i_pineapple_1", "quantity": 3}'
        ),
        # Lesson complete — unlock lesson 1
        (
            "o_l0_complete_001", "e_l0_004",
            "LESSON_COMPLETE",
            '{"lesson_id": "lesson_0", "unlocks": "lesson_1"}'
        ),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO events VALUES (?,?,?,?)", events)
    print(f"   Inserted {len(events)} events")


def verify(cursor):
    """Prints a summary of all inserted data for verification."""
    print("\n── Verification ─────────────────────────────────────────────")

    tables = ["npcs", "vendors", "items", "dialogue_nodes",
              "dialogues", "words", "options", "events"]
    for table in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table:20s} → {count} rows")

    print("\n── Sample dialogue flow ─────────────────────────────────────")
    rows = cursor.execute("""
        SELECT d.node_id, d.dialogue, d.translation_HAN
        FROM dialogues d
        ORDER BY d.dialogue_id
    """).fetchall()
    for row in rows:
        print(f"\n  [{row[0]}]")
        print(f"  EN: {row[1]}")
        print(f"  HK: {row[2]}")


def populate():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    print(f"Creating/connecting to: {DB_PATH}\n")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Step 1 — Creating tables...")
    create_tables(cursor)

    print("\nStep 2 — Populating NPCs...")
    populate_npcs(cursor)

    print("\nStep 3 — Populating vendors...")
    populate_vendors(cursor)

    print("\nStep 4 — Populating items...")
    populate_items(cursor)

    print("\nStep 5 — Populating dialogue nodes...")
    populate_dialogue_nodes(cursor)

    print("\nStep 6 — Populating dialogues...")
    populate_dialogues(cursor)

    print("\nStep 7 — Populating vocabulary keywords...")
    populate_words(cursor)

    print("\nStep 8 — Populating player options...")
    populate_options(cursor)

    print("\nStep 9 — Populating events...")
    populate_events(cursor)

    conn.commit()

    print("\nStep 10 — Verifying data...")
    verify(cursor)

    conn.close()
    print("\n Lesson 0 population complete!")
    print(f"   Database saved to: {DB_PATH}")


if __name__ == "__main__":
    populate()