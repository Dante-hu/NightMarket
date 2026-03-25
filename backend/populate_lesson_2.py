"""
Lesson 2 Population Script — PRICES AND BARGAINING
Adds Lesson 2 content to hok_lesson_data.db.

Run from your backend root folder:
    python populate_lesson_2.py

IMPORTANT: Run populate_lesson_0.py and populate_lesson_1.py first.

Lesson 2 Overview:
    - Player continues wandering night market stalls
    - Focus on prices, quantities, discounts and bargaining
    - Learning objectives:
        * Ask how much something costs (这个多少钱？)
        * Understand quantity words (一个，一盒，一瓶)
        * Understand discount calculations (打X折)
        * Understand BOGO deals (买一送一)
        * Try bargaining (可以便宜点吗？)
        * Cultural note: 生意兴隆

Vendor Path Distribution:
    v1 胡椒饼  (Pepper Bun)         → Regular ordering, buy multiple
    v2 鸡翅包饭 (Chicken Wing Roll)  → Percentage discount (打七折)
    v3 新竹贡丸 (Hsinchu Pork Ball)  → BOGO deal (买一送一)
    v4 筒仔米糕 (Tube Rice Pudding)  → Bargaining REJECTED
    v5 芋粿巧  (Steamed Taro Cake)  → Bargaining ACCEPTED

New Vocab Introduced:
    这个多少钱？  How much is this?
    六块一个      $6 for one
    来两个吧      I'll take two
    原价          original price
    打七折        30% off (70% of original)
    买一送一      Buy one get one free
    可以便宜点吗  Can it be cheaper?
    不行          No / Cannot
    好吧          Okay / Fine
    谢谢          Thank you
    没关系        No worries
    生意兴隆      May your business prosper
"""

import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "database",
    "hok_lesson_data.db"
)


def check_db():
    if not os.path.isfile(DB_PATH):
        print("ERROR: hok_lesson_data.db not found.")
        print("Please run populate_lesson_0.py first.")
        return False
    return True


def populate_npcs(cursor):
    npcs = [
        ("npc_pepper_bun",      "Pepper Bun Vendor"),
        ("npc_chicken_wing",    "Chicken Wing Rice Roll Vendor"),
        ("npc_pork_ball",       "Hsinchu Pork Ball Vendor"),
        ("npc_tube_pudding",    "Tube Rice Pudding Vendor"),
        ("npc_taro_cake",       "Steamed Taro Cake Vendor"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO npcs VALUES (?,?)", npcs)
    print(f"   Inserted {len(npcs)} NPCs")


def populate_vendors(cursor):
    vendors = [
        ("v_pepper_bun",   "n_l2_v1_greet", "npc_pepper_bun",   "胡椒饼 Stall"),
        ("v_chicken_wing", "n_l2_v2_greet", "npc_chicken_wing", "鸡翅包饭 Stall"),
        ("v_pork_ball",    "n_l2_v3_greet", "npc_pork_ball",    "新竹贡丸 Stall"),
        ("v_tube_pudding", "n_l2_v4_greet", "npc_tube_pudding", "筒仔米糕 Stall"),
        ("v_taro_cake",    "n_l2_v5_greet", "npc_taro_cake",    "芋粿巧 Stall"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO vendors VALUES (?,?,?,?)", vendors)
    print(f"   Inserted {len(vendors)} vendors")


def populate_items(cursor):
    items = [
        ("v_pepper_bun",   "i_pepper_bun_1",
         "胡椒饼 (Pepper Bun)",
         "A crispy baked bun filled with juicy pepper-seasoned pork. "
         "Cooked in a clay oven, famous for its smoky flavour.",
         6),

        ("v_chicken_wing", "i_chicken_wing_1",
         "鸡翅包饭 (Chicken Wing Rice Roll)",
         "A chicken wing stuffed with sticky rice and fillings. "
         "A creative and filling Taiwanese street food.",
         7),

        ("v_pork_ball",    "i_pork_ball_1",
         "新竹贡丸 (Hsinchu Pork Ball)",
         "Springy pork meatballs from Hsinchu city, famous for their "
         "chewy texture and savoury flavour.",
         5),

        ("v_tube_pudding", "i_tube_pudding_1",
         "筒仔米糕 (Tube Rice Pudding)",
         "Sticky rice cooked in a bamboo tube with pork and mushrooms. "
         "Served with a sweet sauce on top.",
         8),

        ("v_taro_cake",    "i_taro_cake_1",
         "芋粿巧 (Steamed Taro Cake)",
         "A soft steamed cake made from taro and rice flour. "
         "Lightly savoury with a smooth taro flavour.",
         6),
    ]
    cursor.executemany("INSERT OR IGNORE INTO items VALUES (?,?,?,?,?)", items)
    print(f"   Inserted {len(items)} items")


def populate_dialogue_nodes(cursor):
    """
    Path 1 — 胡椒饼 (Regular ordering, buy multiple)
        greet → howmuch → price → order_two → complete

    Path 2 — 鸡翅包饭 (Percentage discount 打七折)
        greet → howmuch → price_original → discount_explain → order → complete

    Path 3 — 新竹贡丸 (BOGO 买一送一)
        greet → bogo_sign → try → like → order → complete

    Path 4 — 筒仔米糕 (Bargaining rejected)
        greet → howmuch → price → bargain_ask → bargain_reject → order → complete

    Path 5 — 芋粿巧 (Bargaining accepted)
        greet → howmuch → price → bargain_ask → bargain_accept → order → complete
    """
    nodes = [
        # ── Path 1: 胡椒饼 — Regular ordering ────────────────────────
        ("n_l2_v1_greet",    "n_000",           "npc_pepper_bun"),
        ("n_l2_v1_howmuch",  "n_l2_v1_greet",   "npc_pepper_bun"),
        ("n_l2_v1_price",    "n_l2_v1_howmuch",  "npc_pepper_bun"),
        ("n_l2_v1_order",    "n_l2_v1_price",   "npc_pepper_bun"),
        ("n_l2_v1_complete", "n_l2_v1_order",   "npc_pepper_bun"),

        # ── Path 2: 鸡翅包饭 — Percentage discount ───────────────────
        ("n_l2_v2_greet",    "n_000",              "npc_chicken_wing"),
        ("n_l2_v2_howmuch",  "n_l2_v2_greet",      "npc_chicken_wing"),
        ("n_l2_v2_original", "n_l2_v2_howmuch",    "npc_chicken_wing"),
        ("n_l2_v2_discount", "n_l2_v2_original",   "npc_chicken_wing"),
        ("n_l2_v2_order",    "n_l2_v2_discount",   "npc_chicken_wing"),
        ("n_l2_v2_complete", "n_l2_v2_order",      "npc_chicken_wing"),

        # ── Path 3: 新竹贡丸 — BOGO ──────────────────────────────────
        ("n_l2_v3_greet",    "n_000",           "npc_pork_ball"),
        ("n_l2_v3_bogo",     "n_l2_v3_greet",   "npc_pork_ball"),
        ("n_l2_v3_try",      "n_l2_v3_bogo",    "npc_pork_ball"),
        ("n_l2_v3_like",     "n_l2_v3_try",     "npc_pork_ball"),
        ("n_l2_v3_order",    "n_l2_v3_like",    "npc_pork_ball"),
        ("n_l2_v3_complete", "n_l2_v3_order",   "npc_pork_ball"),

        # ── Path 4: 筒仔米糕 — Bargaining rejected ───────────────────
        ("n_l2_v4_greet",    "n_000",              "npc_tube_pudding"),
        ("n_l2_v4_howmuch",  "n_l2_v4_greet",      "npc_tube_pudding"),
        ("n_l2_v4_price",    "n_l2_v4_howmuch",    "npc_tube_pudding"),
        ("n_l2_v4_bargain",  "n_l2_v4_price",      "npc_tube_pudding"),
        ("n_l2_v4_reject",   "n_l2_v4_bargain",    "npc_tube_pudding"),
        ("n_l2_v4_order",    "n_l2_v4_reject",     "npc_tube_pudding"),
        ("n_l2_v4_complete", "n_l2_v4_order",      "npc_tube_pudding"),

        # ── Path 5: 芋粿巧 — Bargaining accepted ─────────────────────
        ("n_l2_v5_greet",    "n_000",              "npc_taro_cake"),
        ("n_l2_v5_howmuch",  "n_l2_v5_greet",      "npc_taro_cake"),
        ("n_l2_v5_price",    "n_l2_v5_howmuch",    "npc_taro_cake"),
        ("n_l2_v5_bargain",  "n_l2_v5_price",      "npc_taro_cake"),
        ("n_l2_v5_accept",   "n_l2_v5_bargain",    "npc_taro_cake"),
        ("n_l2_v5_order",    "n_l2_v5_accept",     "npc_taro_cake"),
        ("n_l2_v5_complete", "n_l2_v5_order",      "npc_taro_cake"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO dialogue_nodes VALUES (?,?,?)", nodes)
    print(f"   Inserted {len(nodes)} dialogue nodes")


def populate_dialogues(cursor):
    dialogues = [
        # ── Path 1: 胡椒饼 — Regular ordering ────────────────────────

        ("n_l2_v1_greet", "d_l2_v1_001",
         "Hello!",
         "老板好！",
         "", "npc_pepper_bun"),

        ("n_l2_v1_howmuch", "d_l2_v1_002",
         "How much is this?",
         "这个多少钱？",
         "", "npc_pepper_bun"),

        ("n_l2_v1_price", "d_l2_v1_003",
         "$6 for one.",
         "六块一个。",
         "", "npc_pepper_bun"),

        ("n_l2_v1_order", "d_l2_v1_004",
         "I will take two then, thank you.",
         "来两个吧，谢谢。",
         "", "npc_pepper_bun"),

        ("n_l2_v1_complete", "d_l2_v1_005",
         "Here you go! Thank you for your support!",
         "来！谢谢惠顾！",
         "", "npc_pepper_bun"),

        # ── Path 2: 鸡翅包饭 — Percentage discount ───────────────────

        ("n_l2_v2_greet", "d_l2_v2_001",
         "Hello!",
         "老板好！",
         "", "npc_chicken_wing"),

        ("n_l2_v2_howmuch", "d_l2_v2_002",
         "How much is this?",
         "这个多少钱？",
         "", "npc_chicken_wing"),

        ("n_l2_v2_original", "d_l2_v2_003",
         "Original price is $7 each.",
         "原价七块一个。",
         "", "npc_chicken_wing"),

        ("n_l2_v2_discount", "d_l2_v2_004",
         "But if you buy a box of six, there is a 30% discount!",
         "但是买一盒六个打七折！",
         "", "npc_chicken_wing"),

        ("n_l2_v2_order", "d_l2_v2_005",
         "Great! I will take a box of six please.",
         "好！我要一盒六个。",
         "", "npc_chicken_wing"),

        ("n_l2_v2_complete", "d_l2_v2_006",
         "Here you go! May your business prosper!",
         "来！生意兴隆！",
         "", "npc_chicken_wing"),

        # ── Path 3: 新竹贡丸 — BOGO ──────────────────────────────────

        ("n_l2_v3_greet", "d_l2_v3_001",
         "Would you like to try some? We have a deal today!",
         "要试吃吗？今天有做活动！",
         "", "npc_pork_ball"),

        ("n_l2_v3_bogo", "d_l2_v3_002",
         "We have a buy one get one free deal today!",
         "今天买一送一！",
         "", "npc_pork_ball"),

        ("n_l2_v3_try", "d_l2_v3_003",
         "Yes, I will try some!",
         "好，我试一点！",
         "", "npc_pork_ball"),

        ("n_l2_v3_like", "d_l2_v3_004",
         "It's delicious!",
         "好好吃呀！",
         "", "npc_pork_ball"),

        ("n_l2_v3_order", "d_l2_v3_005",
         "I will take one then!",
         "那我要一个！",
         "", "npc_pork_ball"),

        ("n_l2_v3_complete", "d_l2_v3_006",
         "Here you go — and here is your free one too!",
         "来！这是你的，买一送一！",
         "", "npc_pork_ball"),

        # ── Path 4: 筒仔米糕 — Bargaining rejected ───────────────────

        ("n_l2_v4_greet", "d_l2_v4_001",
         "Hello!",
         "老板好！",
         "", "npc_tube_pudding"),

        ("n_l2_v4_howmuch", "d_l2_v4_002",
         "How much is this?",
         "这个多少钱？",
         "", "npc_tube_pudding"),

        ("n_l2_v4_price", "d_l2_v4_003",
         "$8 for one.",
         "八块一个。",
         "", "npc_tube_pudding"),

        ("n_l2_v4_bargain", "d_l2_v4_004",
         "Can it be a little cheaper?",
         "可以便宜点吗？",
         "", "npc_tube_pudding"),

        ("n_l2_v4_reject", "d_l2_v4_005",
         "Sorry, cannot. This is already the best price!",
         "不行，这已经是最便宜的价格了！",
         "", "npc_tube_pudding"),

        ("n_l2_v4_order", "d_l2_v4_006",
         "Okay, no worries. I will take one.",
         "没关系，我要一个。",
         "", "npc_tube_pudding"),

        ("n_l2_v4_complete", "d_l2_v4_007",
         "Here you go! Thank you!",
         "来！谢谢！",
         "", "npc_tube_pudding"),

        # ── Path 5: 芋粿巧 — Bargaining accepted ─────────────────────

        ("n_l2_v5_greet", "d_l2_v5_001",
         "Hello!",
         "老板好！",
         "", "npc_taro_cake"),

        ("n_l2_v5_howmuch", "d_l2_v5_002",
         "How much is this?",
         "这个多少钱？",
         "", "npc_taro_cake"),

        ("n_l2_v5_price", "d_l2_v5_003",
         "$6 for one.",
         "六块一个。",
         "", "npc_taro_cake"),

        ("n_l2_v5_bargain", "d_l2_v5_004",
         "Can it be a little cheaper?",
         "可以便宜点吗？",
         "", "npc_taro_cake"),

        ("n_l2_v5_accept", "d_l2_v5_005",
         "Okay fine! $5 for you. You have a good eye!",
         "好吧！给你五块。你很会买东西！",
         "", "npc_taro_cake"),

        ("n_l2_v5_order", "d_l2_v5_006",
         "Thank you so much!",
         "谢谢你！",
         "", "npc_taro_cake"),

        ("n_l2_v5_complete", "d_l2_v5_007",
         "Here you go! Come back again!",
         "来！欢迎再来！",
         "", "npc_taro_cake"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO dialogues VALUES (?,?,?,?,?,?)", dialogues)
    print(f"   Inserted {len(dialogues)} dialogue lines")


def populate_words(cursor):
    words = [
        # ── Path 1: 胡椒饼 keywords ───────────────────────────────────

        ("d_l2_v1_002", "w_l2_001",
         "这个多少钱", "How much is this?",
         "Standard phrase for asking the price of anything at a stall",
         ""),

        ("d_l2_v1_003", "w_l2_002",
         "六块一个", "$6 for one",
         "Price format: amount + 块 (dollar unit) + quantity word",
         ""),

        ("d_l2_v1_004", "w_l2_003",
         "来两个吧", "I'll take two",
         "来 here means 'give me' — casual ordering phrase",
         ""),

        ("d_l2_v1_004", "w_l2_004",
         "谢谢", "Thank you (tsiā-tsiā)",
         "Universal polite expression of gratitude",
         ""),

        # ── Path 2: 鸡翅包饭 keywords ─────────────────────────────────

        ("d_l2_v2_003", "w_l2_005",
         "原价", "Original price",
         "Used by vendors to indicate the price before any discount",
         ""),

        ("d_l2_v2_004", "w_l2_006",
         "打七折", "30% off (70% of original price)",
         "Discount system in Taiwan is flipped: 打7折 = pay 70% = 30% off",
         ""),

        ("d_l2_v2_004", "w_l2_007",
         "一盒", "One box",
         "量词 (measure word) for box-shaped items",
         ""),

        ("d_l2_v2_006", "w_l2_008",
         "生意兴隆", "May your business prosper (sing-i hing-liông)",
         "A blessing said to vendors — a sign of goodwill and good culture",
         ""),

        # ── Path 3: 新竹贡丸 keywords ─────────────────────────────────

        ("d_l2_v3_002", "w_l2_009",
         "买一送一", "Buy one get one free (BOGO)",
         "Common promotional deal at night market stalls",
         ""),

        ("d_l2_v3_001", "w_l2_010",
         "做活动", "Running a promotion / Having a deal",
         "Used by vendors to announce a special offer",
         ""),

        ("d_l2_v3_004", "w_l2_011",
         "好好吃", "So delicious / Really tasty",
         "Casual expression of enjoyment after tasting food",
         ""),

        # ── Path 4: 筒仔米糕 keywords ─────────────────────────────────

        ("d_l2_v4_004", "w_l2_012",
         "可以便宜点吗", "Can it be cheaper? (khó-í pîn-gî tiám-á bô?)",
         "Polite way to ask for a discount — works at some stalls not all",
         ""),

        ("d_l2_v4_005", "w_l2_013",
         "不行", "Cannot / Not possible (put-hâng)",
         "Direct refusal — vendor is firm on the price",
         ""),

        ("d_l2_v4_006", "w_l2_014",
         "没关系", "No worries / It's okay (bô-kuan-hē)",
         "Used to accept a situation gracefully with no hard feelings",
         ""),

        # ── Path 5: 芋粿巧 keywords ───────────────────────────────────

        ("d_l2_v5_005", "w_l2_015",
         "好吧", "Okay fine / Alright then",
         "Vendor agrees reluctantly — indicates bargaining was successful",
         ""),

        ("d_l2_v5_006", "w_l2_016",
         "谢谢你", "Thank you (to someone specific)",
         "Adding 你 makes it more personal and warm",
         ""),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO words VALUES (?,?,?,?,?,?)", words)
    print(f"   Inserted {len(words)} keyword vocabulary entries")


def populate_options(cursor):
    options = [
        # ── Path 1: 胡椒饼 ────────────────────────────────────────────
        # After vendor gives price → player orders two
        ("n_l2_v1_price", "o_l2_v1_001",
         "I will take two. / 来两个吧，谢谢。",
         "n_l2_v1_order", "positive"),

        # ── Path 2: 鸡翅包饭 ──────────────────────────────────────────
        # After vendor explains discount → player orders box
        ("n_l2_v2_discount", "o_l2_v2_001",
         "I will take a box of six. / 我要一盒六个。",
         "n_l2_v2_order", "positive"),

        # ── Path 3: 新竹贡丸 ──────────────────────────────────────────
        # Vendor announces BOGO → player tries
        ("n_l2_v3_bogo", "o_l2_v3_001",
         "Yes, I will try some! / 好，我试一点！",
         "n_l2_v3_try", "positive"),

        # After trying → player likes it and orders
        ("n_l2_v3_like", "o_l2_v3_002",
         "I will take one! / 那我要一个！",
         "n_l2_v3_order", "positive"),

        # ── Path 4: 筒仔米糕 — Bargaining rejected ───────────────────
        # After vendor gives price → player tries to bargain
        ("n_l2_v4_price", "o_l2_v4_001",
         "Can it be cheaper? / 可以便宜点吗？",
         "n_l2_v4_bargain", "neutral"),

        # After vendor rejects → player accepts and orders
        ("n_l2_v4_reject", "o_l2_v4_002",
         "No worries, I will take one. / 没关系，我要一个。",
         "n_l2_v4_order", "positive"),

        # ── Path 5: 芋粿巧 — Bargaining accepted ─────────────────────
        # After vendor gives price → player tries to bargain
        ("n_l2_v5_price", "o_l2_v5_001",
         "Can it be cheaper? / 可以便宜点吗？",
         "n_l2_v5_bargain", "neutral"),

        # After vendor accepts → player thanks and orders
        ("n_l2_v5_accept", "o_l2_v5_002",
         "Thank you so much! / 谢谢你！",
         "n_l2_v5_order", "positive"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO options VALUES (?,?,?,?,?)", options)
    print(f"   Inserted {len(options)} dialogue options")


def populate_events(cursor):
    events = [
        # Path 1 — buy 2 pepper buns
        ("o_l2_v1_001", "e_l2_001",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_pepper_bun_1", "quantity": 2}'),

        # Path 2 — buy box of 6 chicken wings (discounted)
        ("o_l2_v2_001", "e_l2_002",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_chicken_wing_1", "quantity": 6}'),

        # Path 3 — buy 1 pork ball, get 1 free (BOGO)
        ("o_l2_v3_002", "e_l2_003",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_pork_ball_1", "quantity": 2}'),

        # Path 4 — buy 1 tube pudding (no discount)
        ("o_l2_v4_002", "e_l2_004",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_tube_pudding_1", "quantity": 1}'),

        # Path 5 — buy 1 taro cake (discounted price)
        ("o_l2_v5_002", "e_l2_005",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_taro_cake_1", "quantity": 1}'),
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

    print("\n── Lesson 2 Vendors ─────────────────────────────────────────")
    rows = cursor.execute("""
        SELECT v.vendor_id, v.vendor_name, n.npc_name
        FROM vendors v JOIN npcs n ON n.npc_id = v.npc_id
        WHERE v.vendor_id LIKE 'v_%' AND v.node_id LIKE 'n_l2_%'
        ORDER BY v.vendor_id
    """).fetchall()
    for row in rows:
        print(f"  {row[0]:20s} | {row[1]:25s} | {row[2]}")

    print("\n── Sample: Path 4 Bargaining Rejected ──────────────────────")
    rows = cursor.execute("""
        SELECT node_id, dialogue, translation
        FROM dialogues
        WHERE node_id LIKE 'n_l2_v4%'
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
            print(f"  → {opt[0]} | next: {opt[1]}")


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
    print("\n Lesson 2 population complete!")
    print(f"   Database: {DB_PATH}")


if __name__ == "__main__":
    populate()