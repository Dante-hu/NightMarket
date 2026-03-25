"""
Lesson 3 Population Script — MAIN DISH EXPLORATION
Adds Lesson 3 content to hok_lesson_data.db.

Run from your backend root folder:
    python populate_lesson_3.py

IMPORTANT: Run populate_lesson_0.py, 1.py, and 2.py first.

Vendor Path Distribution:
    v1 蚵仔煎  Oyster Omelette    → Path 5: Sauce options
    v2 肉圆    Bahwan             → Path 2: Buys + unique preparation
    v3 担仔面  Danzai Noodles     → Path 1: Asks, does not buy
    v4 卤肉饭  Minced Pork Rice   → Path 4: No allergen, buys
    v5 牛肉面  Beef Noodle Soup   → Path 3: Contains allergen, does not buy
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
        ("npc_oyster_omelette", "Oyster Omelette Vendor"),
        ("npc_bahwan",          "Bahwan Vendor"),
        ("npc_danzai_noodles",  "Danzai Noodles Vendor"),
        ("npc_pork_rice",       "Minced Pork Rice Vendor"),
        ("npc_beef_noodle",     "Beef Noodle Soup Vendor"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO npcs VALUES (?,?)", npcs)
    print(f"  Inserted {len(npcs)} NPCs")


def populate_vendors(cursor):
    vendors = [
        ("v_oyster_omelette", "n_l3_v1_greet", "npc_oyster_omelette", "蚵仔煎 Stall"),
        ("v_bahwan",          "n_l3_v2_greet", "npc_bahwan",          "肉圆 Stall"),
        ("v_danzai_noodles",  "n_l3_v3_greet", "npc_danzai_noodles",  "担仔面 Stall"),
        ("v_pork_rice",       "n_l3_v4_greet", "npc_pork_rice",       "卤肉饭 Stall"),
        ("v_beef_noodle",     "n_l3_v5_greet", "npc_beef_noodle",     "牛肉面 Stall"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO vendors VALUES (?,?,?,?)", vendors)
    print(f"  Inserted {len(vendors)} vendors")


def populate_items(cursor):
    items = [
        ("v_oyster_omelette", "i_oyster_omelette_1",
         "蚵仔煎 (Oyster Omelette)",
         "A savoury omelette made with oysters, egg, and starch. Served with a sweet sauce.",
         80),
        ("v_bahwan", "i_bahwan_1",
         "肉圆 (Bahwan)",
         "A Taiwanese dumpling made of translucent starch and rice flour, filled with pork and vegetables.",
         50),
        ("v_danzai_noodles", "i_danzai_noodles_1",
         "担仔面 (Danzai Noodles)",
         "Thin noodles in a rich shrimp broth topped with minced pork, shrimp, and a boiled egg.",
         60),
        ("v_pork_rice", "i_pork_rice_1",
         "卤肉饭 (Minced Pork Rice)",
         "Braised minced pork belly served over white rice. A beloved Taiwanese comfort food.",
         40),
        ("v_beef_noodle", "i_beef_noodle_1",
         "牛肉面 (Taiwan Beef Noodle Soup)",
         "Thick wheat noodles in a rich braised beef broth with tender beef slices.",
         120),
    ]
    cursor.executemany("INSERT OR IGNORE INTO items VALUES (?,?,?,?,?)", items)
    print(f"  Inserted {len(items)} items")


def populate_dialogue_nodes(cursor):
    nodes = [
        # Path 1: 担仔面 — Asks, does not buy
        ("n_l3_v3_greet",         "n_000",                 "npc_danzai_noodles"),
        ("n_l3_v3_whatis",        "n_l3_v3_greet",         "npc_danzai_noodles"),
        ("n_l3_v3_explain",       "n_l3_v3_whatis",        "npc_danzai_noodles"),
        ("n_l3_v3_inside",        "n_l3_v3_explain",       "npc_danzai_noodles"),
        ("n_l3_v3_vendor_inside", "n_l3_v3_inside",        "npc_danzai_noodles"),
        ("n_l3_v3_decline",       "n_l3_v3_vendor_inside", "npc_danzai_noodles"),
        ("n_l3_v3_end",           "n_l3_v3_decline",       "npc_danzai_noodles"),

        # Path 2: 肉圆 — Buys + unique prep
        ("n_l3_v2_greet",         "n_000",                  "npc_bahwan"),
        ("n_l3_v2_whatis",        "n_l3_v2_greet",          "npc_bahwan"),
        ("n_l3_v2_explain",       "n_l3_v2_whatis",         "npc_bahwan"),
        ("n_l3_v2_inside",        "n_l3_v2_explain",        "npc_bahwan"),
        ("n_l3_v2_vendor_inside", "n_l3_v2_inside",         "npc_bahwan"),
        ("n_l3_v2_order",         "n_l3_v2_vendor_inside",  "npc_bahwan"),
        ("n_l3_v2_prep_note",     "n_l3_v2_order",          "npc_bahwan"),
        ("n_l3_v2_complete",      "n_l3_v2_prep_note",      "npc_bahwan"),

        # Path 3: 牛肉面 — Contains allergen, does not buy
        ("n_l3_v5_greet",         "n_000",                  "npc_beef_noodle"),
        ("n_l3_v5_whatis",        "n_l3_v5_greet",          "npc_beef_noodle"),
        ("n_l3_v5_explain",       "n_l3_v5_whatis",         "npc_beef_noodle"),
        ("n_l3_v5_allergen_ask",  "n_l3_v5_explain",        "npc_beef_noodle"),
        ("n_l3_v5_has_allergen",  "n_l3_v5_allergen_ask",   "npc_beef_noodle"),
        ("n_l3_v5_decline",       "n_l3_v5_has_allergen",   "npc_beef_noodle"),
        ("n_l3_v5_end",           "n_l3_v5_decline",        "npc_beef_noodle"),

        # Path 4: 卤肉饭 — No allergen, buys
        ("n_l3_v4_greet",         "n_000",                  "npc_pork_rice"),
        ("n_l3_v4_whatis",        "n_l3_v4_greet",          "npc_pork_rice"),
        ("n_l3_v4_explain",       "n_l3_v4_whatis",         "npc_pork_rice"),
        ("n_l3_v4_allergen_ask",  "n_l3_v4_explain",        "npc_pork_rice"),
        ("n_l3_v4_no_allergen",   "n_l3_v4_allergen_ask",   "npc_pork_rice"),
        ("n_l3_v4_order",         "n_l3_v4_no_allergen",    "npc_pork_rice"),
        ("n_l3_v4_complete",      "n_l3_v4_order",          "npc_pork_rice"),

        # Path 5: 蚵仔煎 — Sauce options
        ("n_l3_v1_greet",         "n_000",                  "npc_oyster_omelette"),
        ("n_l3_v1_whatis",        "n_l3_v1_greet",          "npc_oyster_omelette"),
        ("n_l3_v1_explain",       "n_l3_v1_whatis",         "npc_oyster_omelette"),
        ("n_l3_v1_inside",        "n_l3_v1_explain",        "npc_oyster_omelette"),
        ("n_l3_v1_vendor_inside", "n_l3_v1_inside",         "npc_oyster_omelette"),
        ("n_l3_v1_sauce_ask",     "n_l3_v1_vendor_inside",  "npc_oyster_omelette"),
        ("n_l3_v1_sauce_options", "n_l3_v1_sauce_ask",      "npc_oyster_omelette"),
        ("n_l3_v1_original",      "n_l3_v1_sauce_options",  "npc_oyster_omelette"),
        ("n_l3_v1_wasabi",        "n_l3_v1_sauce_options",  "npc_oyster_omelette"),
        ("n_l3_v1_thai_chili",    "n_l3_v1_sauce_options",  "npc_oyster_omelette"),
        ("n_l3_v1_complete",      "n_l3_v1_original",       "npc_oyster_omelette"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO dialogue_nodes VALUES (?,?,?)", nodes)
    print(f"  Inserted {len(nodes)} dialogue nodes")


def populate_dialogues(cursor):
    dialogues = [
        # Path 1: 担仔面 — Asks, does not buy
        ("n_l3_v3_greet",         "d_l3_v3_001", "Hello!", "老板好！", "", "npc_danzai_noodles"),
        ("n_l3_v3_whatis",        "d_l3_v3_002", "Excuse me, what is this dish?", "请问这是什么？", "", "npc_danzai_noodles"),
        ("n_l3_v3_explain",       "d_l3_v3_003", "This is danzai noodles! Thin noodles in a rich shrimp broth.", "这是担仔面！细面条配上鲜美的虾汤。", "", "npc_danzai_noodles"),
        ("n_l3_v3_inside",        "d_l3_v3_004", "What is inside?", "里面有什么？", "", "npc_danzai_noodles"),
        ("n_l3_v3_vendor_inside", "d_l3_v3_005", "Inside there is minced pork, shrimp, and a boiled egg!", "里面有肉燥、虾子还有卤蛋！", "", "npc_danzai_noodles"),
        ("n_l3_v3_decline",       "d_l3_v3_006", "It sounds delicious, but I am too full. No thank you!", "听起来很好吃，但是我吃太饱了。不用了，谢谢！", "", "npc_danzai_noodles"),
        ("n_l3_v3_end",           "d_l3_v3_007", "No problem! Come back next time!", "没关系！下次再来！", "", "npc_danzai_noodles"),

        # Path 2: 肉圆 — Buys + unique prep
        ("n_l3_v2_greet",         "d_l3_v2_001", "Hello!", "老板好！", "", "npc_bahwan"),
        ("n_l3_v2_whatis",        "d_l3_v2_002", "Excuse me, what is this dish?", "请问这是什么？", "", "npc_bahwan"),
        ("n_l3_v2_explain",       "d_l3_v2_003", "This is Bahwan! A traditional Taiwanese dumpling.", "这是肉圆！台湾传统小吃。", "", "npc_bahwan"),
        ("n_l3_v2_inside",        "d_l3_v2_004", "What is inside?", "里面有什么？", "", "npc_bahwan"),
        ("n_l3_v2_vendor_inside", "d_l3_v2_005", "Inside there is pork and bamboo shoots! The skin is made from sweet potato starch and rice flour.", "里面有猪肉和竹笋！外皮是用地瓜粉和在来米粉做的。", "", "npc_bahwan"),
        ("n_l3_v2_order",         "d_l3_v2_006", "That sounds amazing! I will take one.", "听起来很特别！我要一个。", "", "npc_bahwan"),
        ("n_l3_v2_prep_note",     "d_l3_v2_007", "Watch closely — we steam it first, then fry it until golden!", "你看！先蒸过再炸到金黄色！", "", "npc_bahwan"),
        ("n_l3_v2_complete",      "d_l3_v2_008", "Here you go! Enjoy your Bahwan!", "来！请慢用！", "", "npc_bahwan"),

        # Path 3: 牛肉面 — Contains allergen, does not buy
        ("n_l3_v5_greet",         "d_l3_v5_001", "Hello!", "老板好！", "", "npc_beef_noodle"),
        ("n_l3_v5_whatis",        "d_l3_v5_002", "Excuse me, what is this dish?", "请问这是什么？", "", "npc_beef_noodle"),
        ("n_l3_v5_explain",       "d_l3_v5_003", "This is Taiwan beef noodle soup! Our broth is simmered for 12 hours.", "这是台湾牛肉面！我们的汤头熬了十二个小时。", "", "npc_beef_noodle"),
        ("n_l3_v5_allergen_ask",  "d_l3_v5_004", "Does this contain beef? I am allergic to beef.", "这个里面有牛肉吗？我对牛肉过敏。", "", "npc_beef_noodle"),
        ("n_l3_v5_has_allergen",  "d_l3_v5_005", "Yes, it does contain beef. I am sorry!", "对，里面有牛肉。不好意思！", "", "npc_beef_noodle"),
        ("n_l3_v5_decline",       "d_l3_v5_006", "No problem. No thank you then!", "没关系。不用了，谢谢！", "", "npc_beef_noodle"),
        ("n_l3_v5_end",           "d_l3_v5_007", "Sorry about that! Come back for something else!", "不好意思！欢迎下次再来！", "", "npc_beef_noodle"),

        # Path 4: 卤肉饭 — No allergen, buys
        ("n_l3_v4_greet",         "d_l3_v4_001", "Hello!", "老板好！", "", "npc_pork_rice"),
        ("n_l3_v4_whatis",        "d_l3_v4_002", "Excuse me, what is this dish?", "请问这是什么？", "", "npc_pork_rice"),
        ("n_l3_v4_explain",       "d_l3_v4_003", "This is minced pork rice! Braised pork belly over white rice.", "这是卤肉饭！卤猪肉配白饭。", "", "npc_pork_rice"),
        ("n_l3_v4_allergen_ask",  "d_l3_v4_004", "Does this contain seafood? I am allergic to seafood.", "这个里面有海鲜吗？我对海鲜过敏。", "", "npc_pork_rice"),
        ("n_l3_v4_no_allergen",   "d_l3_v4_005", "No seafood at all! Just pork, soy sauce, and spices.", "完全没有海鲜！只有猪肉、酱油和香料。", "", "npc_pork_rice"),
        ("n_l3_v4_order",         "d_l3_v4_006", "Perfect! I will take one then.", "太好了！那我要一个。", "", "npc_pork_rice"),
        ("n_l3_v4_complete",      "d_l3_v4_007", "Here you go! Enjoy!", "来！请慢用！", "", "npc_pork_rice"),

        # Path 5: 蚵仔煎 — Sauce options
        ("n_l3_v1_greet",         "d_l3_v1_001", "Hello!", "老板好！", "", "npc_oyster_omelette"),
        ("n_l3_v1_whatis",        "d_l3_v1_002", "Excuse me, what is this dish?", "请问这是什么？", "", "npc_oyster_omelette"),
        ("n_l3_v1_explain",       "d_l3_v1_003", "This is oyster omelette! Made with fresh oysters and egg.", "这是蚵仔煎！用新鲜蚵仔和鸡蛋做的。", "", "npc_oyster_omelette"),
        ("n_l3_v1_inside",        "d_l3_v1_004", "What is inside?", "里面有什么？", "", "npc_oyster_omelette"),
        ("n_l3_v1_vendor_inside", "d_l3_v1_005", "Oysters, egg, sweet potato starch, and vegetables!", "蚵仔、鸡蛋、地瓜粉还有蔬菜！", "", "npc_oyster_omelette"),
        ("n_l3_v1_sauce_ask",     "d_l3_v1_006", "Which sauce would you like?", "你要哪种酱？", "", "npc_oyster_omelette"),
        ("n_l3_v1_sauce_options", "d_l3_v1_007", "We have original sauce, wasabi, or Thai sweet chili sauce!", "我们有原味照烧酱、哇沙米、或泰式甜辣酱！", "", "npc_oyster_omelette"),
        ("n_l3_v1_original",      "d_l3_v1_008", "Original sauce please!", "原味照烧酱！", "", "npc_oyster_omelette"),
        ("n_l3_v1_wasabi",        "d_l3_v1_009", "Wasabi please!", "哇沙米！", "", "npc_oyster_omelette"),
        ("n_l3_v1_thai_chili",    "d_l3_v1_010", "Thai sweet chili sauce please!", "泰式甜辣酱！", "", "npc_oyster_omelette"),
        ("n_l3_v1_complete",      "d_l3_v1_011", "Here you go! Enjoy!", "来！请慢用！", "", "npc_oyster_omelette"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO dialogues VALUES (?,?,?,?,?,?)", dialogues)
    print(f"  Inserted {len(dialogues)} dialogue lines")


def populate_words(cursor):
    words = [
        # Path 1: 担仔面 keywords
        ("d_l3_v3_004", "w_l3_001", "里面有什么", "What is inside?",
         "Used to ask about the ingredients of an unfamiliar dish", ""),
        ("d_l3_v3_006", "w_l3_002", "不用了，谢谢", "No thank you (put-iong-ah, tsia-tsia)",
         "Polite way to decline something offered to you", ""),

        # Path 2: 肉圆 keywords
        ("d_l3_v2_003", "w_l3_003", "肉圆", "Bahwan / Taiwanese Dumpling",
         "Made from sweet potato starch and rice flour, unique to Taiwan", ""),
        ("d_l3_v2_005", "w_l3_004", "地瓜粉", "Sweet potato starch",
         "Key ingredient in many Taiwanese dishes including Bahwan", ""),
        ("d_l3_v2_007", "w_l3_005", "先蒸过再炸", "Steam first then fry",
         "Unique preparation method that gives Bahwan its texture", ""),

        # Path 3: 牛肉面 keywords
        ("d_l3_v5_004", "w_l3_006", "这个里面有...吗", "Does this contain...?",
         "Used to ask about specific ingredients before ordering", ""),
        ("d_l3_v5_004", "w_l3_007", "过敏", "Allergy (kòo-bín)",
         "Important word to know when dining out with dietary restrictions", ""),
        ("d_l3_v5_004", "w_l3_008", "我对牛肉过敏", "I am allergic to beef",
         "Pattern: 我对 + allergen + 过敏", ""),
        ("d_l3_v5_004", "w_l3_009", "牛肉", "Beef (gû-bah)",
         "Common dietary restriction — some people avoid beef for religious reasons", ""),

        # Path 4: 卤肉饭 keywords
        ("d_l3_v4_003", "w_l3_010", "卤肉饭", "Minced Pork Rice (ló-bah-pn̄g)",
         "One of Taiwan's most iconic and beloved comfort foods", ""),
        ("d_l3_v4_004", "w_l3_011", "海鲜", "Seafood (hái-sian)",
         "Common allergen — always good to check before ordering", ""),

        # Path 5: 蚵仔煎 keywords
        ("d_l3_v1_003", "w_l3_012", "蚵仔煎", "Oyster Omelette (o-a-tsian)",
         "One of the most famous Taiwanese night market dishes", ""),
        ("d_l3_v1_007", "w_l3_013", "原味照烧酱", "Original teriyaki sauce",
         "The classic sauce served with oyster omelette", ""),
        ("d_l3_v1_007", "w_l3_014", "哇沙米", "Wasabi",
         "Japanese-influenced condiment popular in Taiwan", ""),
        ("d_l3_v1_007", "w_l3_015", "泰式甜辣酱", "Thai sweet chili sauce",
         "Southeast Asian influence in Taiwanese night market food", ""),
    ]
    cursor.executemany("INSERT OR IGNORE INTO words VALUES (?,?,?,?,?,?)", words)
    print(f"  Inserted {len(words)} keyword vocabulary entries")


def populate_options(cursor):
    options = [
        # Path 1: 担仔面 — player declines after learning about dish
        ("n_l3_v3_vendor_inside", "o_l3_v3_001",
         "No thank you, I am too full. / 不用了，谢谢，我吃太饱了。",
         "n_l3_v3_decline", "neutral"),

        # Path 2: 肉圆 — player orders after learning about dish
        ("n_l3_v2_vendor_inside", "o_l3_v2_001",
         "That sounds amazing! I will take one. / 听起来很特别！我要一个。",
         "n_l3_v2_order", "positive"),

        # Path 3: 牛肉面 — player asks about allergen
        ("n_l3_v5_explain", "o_l3_v5_001",
         "Does this contain beef? I am allergic. / 这个里面有牛肉吗？我对牛肉过敏。",
         "n_l3_v5_allergen_ask", "neutral"),

        # After vendor confirms allergen — player declines
        ("n_l3_v5_has_allergen", "o_l3_v5_002",
         "No thank you then. / 不用了，谢谢！",
         "n_l3_v5_decline", "neutral"),

        # Path 4: 卤肉饭 — player asks about allergen
        ("n_l3_v4_explain", "o_l3_v4_001",
         "Does this contain seafood? I am allergic. / 这个里面有海鲜吗？我对海鲜过敏。",
         "n_l3_v4_allergen_ask", "neutral"),

        # After vendor confirms no allergen — player orders
        ("n_l3_v4_no_allergen", "o_l3_v4_002",
         "Perfect! I will take one. / 太好了！我要一个。",
         "n_l3_v4_order", "positive"),

        # Path 5: 蚵仔煎 — player asks what is inside
        ("n_l3_v1_vendor_inside", "o_l3_v1_001",
         "Which sauce do you have? / 有哪些酱？",
         "n_l3_v1_sauce_ask", "positive"),

        # Sauce options — player picks one of three
        ("n_l3_v1_sauce_options", "o_l3_v1_002",
         "Original sauce please! / 原味照烧酱！",
         "n_l3_v1_original", "positive"),
        ("n_l3_v1_sauce_options", "o_l3_v1_003",
         "Wasabi please! / 哇沙米！",
         "n_l3_v1_wasabi", "positive"),
        ("n_l3_v1_sauce_options", "o_l3_v1_004",
         "Thai sweet chili sauce please! / 泰式甜辣酱！",
         "n_l3_v1_thai_chili", "positive"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO options VALUES (?,?,?,?,?)", options)
    print(f"  Inserted {len(options)} dialogue options")


def populate_events(cursor):
    events = [
        # Path 2: buy 1 Bahwan
        ("o_l3_v2_001", "e_l3_001",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_bahwan_1", "quantity": 1}'),

        # Path 4: buy 1 minced pork rice
        ("o_l3_v4_002", "e_l3_002",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_pork_rice_1", "quantity": 1}'),

        # Path 5: buy oyster omelette regardless of sauce choice
        ("o_l3_v1_002", "e_l3_003",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_oyster_omelette_1", "quantity": 1}'),
        ("o_l3_v1_003", "e_l3_004",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_oyster_omelette_1", "quantity": 1}'),
        ("o_l3_v1_004", "e_l3_005",
         "ADD_TO_INVENTORY",
         '{"item_id": "i_oyster_omelette_1", "quantity": 1}'),
    ]
    cursor.executemany("INSERT OR IGNORE INTO events VALUES (?,?,?,?)", events)
    print(f"  Inserted {len(events)} events")


def verify(cursor):
    print("\n── Verification ─────────────────────────────────────────────")
    tables = ["npcs", "vendors", "items", "dialogue_nodes",
              "dialogues", "words", "options", "events"]
    for table in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table:20s} → {count} total rows")

    print("\n── Lesson 3 Vendors ─────────────────────────────────────────")
    rows = cursor.execute("""
        SELECT v.vendor_id, v.vendor_name, n.npc_name
        FROM vendors v JOIN npcs n ON n.npc_id = v.npc_id
        WHERE v.node_id LIKE 'n_l3_%'
        ORDER BY v.vendor_id
    """).fetchall()
    for row in rows:
        print(f"  {row[0]:22s} | {row[1]:25s} | {row[2]}")

    print("\n── Sample: Sauce Options Path (蚵仔煎) ──────────────────────")
    rows = cursor.execute("""
        SELECT node_id, dialogue, translation
        FROM dialogues WHERE node_id LIKE 'n_l3_v1%'
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
            print(f"  -> {opt[0]} | next: {opt[1]}")


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
    print("\nLesson 3 population complete!")
    print(f"   Database: {DB_PATH}")


if __name__ == "__main__":
    populate()