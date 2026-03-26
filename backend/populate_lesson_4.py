"""
Lesson 4 Population Script — CUSTOMIZATION
Adds Lesson 4 content to hok_lesson_data.db.

Run from your backend root folder:
    python populate_lesson_4.py

IMPORTANT: Run populate_lesson_0.py through 3.py first.

Lesson 4 Overview:
    - Player is full from main dishes and wants dessert/drinks
    - Focus on customizing orders to personal preference
    - Learning objectives:
        * Common customization terms (不要, 多放, 少放)
        * Sugar levels (无糖/三分糖/半糖/七分糖/全糖)
        * Ice levels (去冰/少冰/正常冰/多冰)
        * Toppings (珍珠/椰果/红豆)
        * Size (大/中/小)

Vendor Path Distribution:
    v1 奶茶  Bubble Tea  → Full customization (size + sugar + ice + toppings)
    v2 豆花  Tofu        → Toppings selection (不要 and 多放)
    v3 剉冰  Shaved Ice  → Toppings + sweetness level

New Vocab Introduced:
    不要        don't want
    多放        add more
    少放点      a little less
    无糖        no sugar
    三分糖      30% sugar
    半糖        50% sugar
    七分糖      70% sugar
    全糖        100% sugar
    去冰        no ice
    少冰        less ice
    正常冰      normal ice
    多冰        extra ice
    大/中/小    large/medium/small
    珍珠        tapioca pearls
    椰果        coconut jelly
    红豆        red bean
    芋头        taro
    花生        peanut
    仙草        grass jelly
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
        ("npc_bubble_tea",  "Bubble Tea Vendor"),
        ("npc_tofu",        "Tofu Vendor"),
        ("npc_shaved_ice",  "Shaved Ice Vendor"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO npcs VALUES (?,?)", npcs)
    print(f"  Inserted {len(npcs)} NPCs")


def populate_vendors(cursor):
    vendors = [
        ("v_bubble_tea", "n_l4_v1_greet", "npc_bubble_tea", "奶茶 Stall"),
        ("v_tofu",       "n_l4_v2_greet", "npc_tofu",       "豆花 Stall"),
        ("v_shaved_ice", "n_l4_v3_greet", "npc_shaved_ice", "剉冰 Stall"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO vendors VALUES (?,?,?,?)", vendors)
    print(f"  Inserted {len(vendors)} vendors")


def populate_items(cursor):
    items = [
        ("v_bubble_tea", "i_bubble_tea_1",
         "珍珠奶茶 (Bubble Tea)",
         "Classic Taiwanese milk tea with chewy tapioca pearls. "
         "Fully customizable with size, sugar, ice and toppings.",
         60),

        ("v_tofu", "i_tofu_1",
         "豆花 (Tofu Pudding)",
         "Silky smooth tofu pudding served with sweet syrup and toppings. "
         "A classic Taiwanese dessert enjoyed hot or cold.",
         40),

        ("v_shaved_ice", "i_shaved_ice_1",
         "剉冰 (Shaved Ice)",
         "Finely shaved ice topped with various sweet toppings and syrup. "
         "A refreshing Taiwanese summer dessert.",
         50),
    ]
    cursor.executemany("INSERT OR IGNORE INTO items VALUES (?,?,?,?,?)", items)
    print(f"  Inserted {len(items)} items")


def populate_dialogue_nodes(cursor):
    """
    Path 1 — 奶茶 Bubble Tea (Full customization)
        greet → menu → size_ask → [large/medium/small] →
        sugar_ask → [no/30/50/70/100] →
        ice_ask → [no/less/normal/extra] →
        topping_ask → [pearl/coconut/red_bean/none] →
        complete

    Path 2 — 豆花 Tofu (Toppings — 不要 and 多放)
        greet → explain → topping_ask →
        [red_bean / taro / peanut / grass_jelly] →
        adjust_ask → [more_syrup / less_syrup / fine] →
        complete

    Path 3 — 剉冰 Shaved Ice (Toppings + sweetness)
        greet → explain → topping_ask →
        [pick toppings] → syrup_ask →
        [no_sugar / half_sugar / full_sugar] →
        complete
    """
    nodes = [
        # Path 1: 奶茶 Bubble Tea — full customization
        ("n_l4_v1_greet",       "n_000",             "npc_bubble_tea"),
        ("n_l4_v1_menu",        "n_l4_v1_greet",     "npc_bubble_tea"),
        ("n_l4_v1_size_ask",    "n_l4_v1_menu",      "npc_bubble_tea"),
        ("n_l4_v1_large",       "n_l4_v1_size_ask",  "npc_bubble_tea"),
        ("n_l4_v1_medium",      "n_l4_v1_size_ask",  "npc_bubble_tea"),
        ("n_l4_v1_small",       "n_l4_v1_size_ask",  "npc_bubble_tea"),
        ("n_l4_v1_sugar_ask",   "n_l4_v1_large",     "npc_bubble_tea"),
        ("n_l4_v1_no_sugar",    "n_l4_v1_sugar_ask", "npc_bubble_tea"),
        ("n_l4_v1_30_sugar",    "n_l4_v1_sugar_ask", "npc_bubble_tea"),
        ("n_l4_v1_50_sugar",    "n_l4_v1_sugar_ask", "npc_bubble_tea"),
        ("n_l4_v1_70_sugar",    "n_l4_v1_sugar_ask", "npc_bubble_tea"),
        ("n_l4_v1_100_sugar",   "n_l4_v1_sugar_ask", "npc_bubble_tea"),
        ("n_l4_v1_ice_ask",     "n_l4_v1_no_sugar",  "npc_bubble_tea"),
        ("n_l4_v1_no_ice",      "n_l4_v1_ice_ask",   "npc_bubble_tea"),
        ("n_l4_v1_less_ice",    "n_l4_v1_ice_ask",   "npc_bubble_tea"),
        ("n_l4_v1_normal_ice",  "n_l4_v1_ice_ask",   "npc_bubble_tea"),
        ("n_l4_v1_extra_ice",   "n_l4_v1_ice_ask",   "npc_bubble_tea"),
        ("n_l4_v1_topping_ask", "n_l4_v1_no_ice",    "npc_bubble_tea"),
        ("n_l4_v1_pearl",       "n_l4_v1_topping_ask","npc_bubble_tea"),
        ("n_l4_v1_coconut",     "n_l4_v1_topping_ask","npc_bubble_tea"),
        ("n_l4_v1_red_bean",    "n_l4_v1_topping_ask","npc_bubble_tea"),
        ("n_l4_v1_no_topping",  "n_l4_v1_topping_ask","npc_bubble_tea"),
        ("n_l4_v1_complete",    "n_l4_v1_pearl",     "npc_bubble_tea"),

        # Path 2: 豆花 Tofu — toppings + adjust
        ("n_l4_v2_greet",       "n_000",              "npc_tofu"),
        ("n_l4_v2_explain",     "n_l4_v2_greet",      "npc_tofu"),
        ("n_l4_v2_topping_ask", "n_l4_v2_explain",    "npc_tofu"),
        ("n_l4_v2_red_bean",    "n_l4_v2_topping_ask","npc_tofu"),
        ("n_l4_v2_taro",        "n_l4_v2_topping_ask","npc_tofu"),
        ("n_l4_v2_peanut",      "n_l4_v2_topping_ask","npc_tofu"),
        ("n_l4_v2_grass_jelly", "n_l4_v2_topping_ask","npc_tofu"),
        ("n_l4_v2_adjust_ask",  "n_l4_v2_red_bean",   "npc_tofu"),
        ("n_l4_v2_more_syrup",  "n_l4_v2_adjust_ask", "npc_tofu"),
        ("n_l4_v2_less_syrup",  "n_l4_v2_adjust_ask", "npc_tofu"),
        ("n_l4_v2_fine",        "n_l4_v2_adjust_ask", "npc_tofu"),
        ("n_l4_v2_complete",    "n_l4_v2_more_syrup", "npc_tofu"),

        # Path 3: 剉冰 Shaved Ice — toppings + sweetness
        ("n_l4_v3_greet",       "n_000",              "npc_shaved_ice"),
        ("n_l4_v3_explain",     "n_l4_v3_greet",      "npc_shaved_ice"),
        ("n_l4_v3_topping_ask", "n_l4_v3_explain",    "npc_shaved_ice"),
        ("n_l4_v3_taro_ball",   "n_l4_v3_topping_ask","npc_shaved_ice"),
        ("n_l4_v3_red_bean",    "n_l4_v3_topping_ask","npc_shaved_ice"),
        ("n_l4_v3_mung_bean",   "n_l4_v3_topping_ask","npc_shaved_ice"),
        ("n_l4_v3_syrup_ask",   "n_l4_v3_taro_ball",  "npc_shaved_ice"),
        ("n_l4_v3_no_sugar",    "n_l4_v3_syrup_ask",  "npc_shaved_ice"),
        ("n_l4_v3_half_sugar",  "n_l4_v3_syrup_ask",  "npc_shaved_ice"),
        ("n_l4_v3_full_sugar",  "n_l4_v3_syrup_ask",  "npc_shaved_ice"),
        ("n_l4_v3_complete",    "n_l4_v3_no_sugar",   "npc_shaved_ice"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO dialogue_nodes VALUES (?,?,?)", nodes)
    print(f"  Inserted {len(nodes)} dialogue nodes")


def populate_dialogues(cursor):
    dialogues = [
        # Path 1: 奶茶 Bubble Tea
        ("n_l4_v1_greet",       "d_l4_v1_001",
         "Hello!", "老板好！", "", "npc_bubble_tea"),

        ("n_l4_v1_menu",        "d_l4_v1_002",
         "Welcome! What would you like?",
         "欢迎！你要什么？", "", "npc_bubble_tea"),

        ("n_l4_v1_size_ask",    "d_l4_v1_003",
         "I would like a bubble tea please. What sizes do you have?",
         "我要一杯珍珠奶茶。请问有什么size？", "", "npc_bubble_tea"),

        ("n_l4_v1_large",       "d_l4_v1_004",
         "Large please!",
         "大杯！", "", "npc_bubble_tea"),

        ("n_l4_v1_medium",      "d_l4_v1_005",
         "Medium please!",
         "中杯！", "", "npc_bubble_tea"),

        ("n_l4_v1_small",       "d_l4_v1_006",
         "Small please!",
         "小杯！", "", "npc_bubble_tea"),

        ("n_l4_v1_sugar_ask",   "d_l4_v1_007",
         "What sugar level would you like?",
         "你要几分糖？", "", "npc_bubble_tea"),

        ("n_l4_v1_no_sugar",    "d_l4_v1_008",
         "No sugar please!",
         "无糖！", "", "npc_bubble_tea"),

        ("n_l4_v1_30_sugar",    "d_l4_v1_009",
         "30% sugar please!",
         "三分糖！", "", "npc_bubble_tea"),

        ("n_l4_v1_50_sugar",    "d_l4_v1_010",
         "Half sugar please!",
         "半糖！", "", "npc_bubble_tea"),

        ("n_l4_v1_70_sugar",    "d_l4_v1_011",
         "70% sugar please!",
         "七分糖！", "", "npc_bubble_tea"),

        ("n_l4_v1_100_sugar",   "d_l4_v1_012",
         "Full sugar please!",
         "全糖！", "", "npc_bubble_tea"),

        ("n_l4_v1_ice_ask",     "d_l4_v1_013",
         "What ice level would you like?",
         "你要几分冰？", "", "npc_bubble_tea"),

        ("n_l4_v1_no_ice",      "d_l4_v1_014",
         "No ice please!",
         "去冰！", "", "npc_bubble_tea"),

        ("n_l4_v1_less_ice",    "d_l4_v1_015",
         "Less ice please!",
         "少冰！", "", "npc_bubble_tea"),

        ("n_l4_v1_normal_ice",  "d_l4_v1_016",
         "Normal ice please!",
         "正常冰！", "", "npc_bubble_tea"),

        ("n_l4_v1_extra_ice",   "d_l4_v1_017",
         "Extra ice please!",
         "多冰！", "", "npc_bubble_tea"),

        ("n_l4_v1_topping_ask", "d_l4_v1_018",
         "Which topping would you like?",
         "你要加什么料？", "", "npc_bubble_tea"),

        ("n_l4_v1_pearl",       "d_l4_v1_019",
         "Tapioca pearls please!",
         "加珍珠！", "", "npc_bubble_tea"),

        ("n_l4_v1_coconut",     "d_l4_v1_020",
         "Coconut jelly please!",
         "加椰果！", "", "npc_bubble_tea"),

        ("n_l4_v1_red_bean",    "d_l4_v1_021",
         "Red bean please!",
         "加红豆！", "", "npc_bubble_tea"),

        ("n_l4_v1_no_topping",  "d_l4_v1_022",
         "No toppings please!",
         "不要加料！", "", "npc_bubble_tea"),

        ("n_l4_v1_complete",    "d_l4_v1_023",
         "Coming right up! Here is your bubble tea!",
         "好的！你的珍珠奶茶来了！", "", "npc_bubble_tea"),

        # Path 2: 豆花 Tofu
        ("n_l4_v2_greet",       "d_l4_v2_001",
         "Hello!", "老板好！", "", "npc_tofu"),

        ("n_l4_v2_explain",     "d_l4_v2_002",
         "Welcome! Our tofu pudding is very smooth today! "
         "Which topping would you like?",
         "欢迎！我们今天的豆花很嫩！你要加什么料？",
         "", "npc_tofu"),

        ("n_l4_v2_topping_ask", "d_l4_v2_003",
         "We have red bean, taro, peanut, and grass jelly!",
         "我们有红豆、芋头、花生还有仙草！",
         "", "npc_tofu"),

        ("n_l4_v2_red_bean",    "d_l4_v2_004",
         "Red bean please! And add more syrup!",
         "加红豆！然后多放一点糖水！", "", "npc_tofu"),

        ("n_l4_v2_taro",        "d_l4_v2_005",
         "Taro please! And less syrup!",
         "加芋头！然后少放点糖水！", "", "npc_tofu"),

        ("n_l4_v2_peanut",      "d_l4_v2_006",
         "Peanut please!",
         "加花生！", "", "npc_tofu"),

        ("n_l4_v2_grass_jelly", "d_l4_v2_007",
         "Grass jelly please!",
         "加仙草！", "", "npc_tofu"),

        ("n_l4_v2_adjust_ask",  "d_l4_v2_008",
         "Would you like more or less syrup?",
         "糖水要多一点还是少一点？", "", "npc_tofu"),

        ("n_l4_v2_more_syrup",  "d_l4_v2_009",
         "More syrup please!",
         "多放一点！", "", "npc_tofu"),

        ("n_l4_v2_less_syrup",  "d_l4_v2_010",
         "Less syrup please!",
         "少放点！", "", "npc_tofu"),

        ("n_l4_v2_fine",        "d_l4_v2_011",
         "It is perfect as it is, thank you!",
         "这样就好了，谢谢！", "", "npc_tofu"),

        ("n_l4_v2_complete",    "d_l4_v2_012",
         "Here you go! Enjoy your tofu pudding!",
         "来！请慢用！", "", "npc_tofu"),

        # Path 3: 剉冰 Shaved Ice
        ("n_l4_v3_greet",       "d_l4_v3_001",
         "Hello!", "老板好！", "", "npc_shaved_ice"),

        ("n_l4_v3_explain",     "d_l4_v3_002",
         "Welcome! Our shaved ice is very refreshing! "
         "What toppings would you like?",
         "欢迎！我们的剉冰很消暑！你要加什么料？",
         "", "npc_shaved_ice"),

        ("n_l4_v3_topping_ask", "d_l4_v3_003",
         "We have taro balls, red bean, and mung bean!",
         "我们有芋圆、红豆还有绿豆！",
         "", "npc_shaved_ice"),

        ("n_l4_v3_taro_ball",   "d_l4_v3_004",
         "Taro balls please!",
         "加芋圆！", "", "npc_shaved_ice"),

        ("n_l4_v3_red_bean",    "d_l4_v3_005",
         "Red bean please!",
         "加红豆！", "", "npc_shaved_ice"),

        ("n_l4_v3_mung_bean",   "d_l4_v3_006",
         "Mung bean please!",
         "加绿豆！", "", "npc_shaved_ice"),

        ("n_l4_v3_syrup_ask",   "d_l4_v3_007",
         "How much syrup would you like?",
         "你要加多少糖水？", "", "npc_shaved_ice"),

        ("n_l4_v3_no_sugar",    "d_l4_v3_008",
         "No syrup please!",
         "不要糖水！", "", "npc_shaved_ice"),

        ("n_l4_v3_half_sugar",  "d_l4_v3_009",
         "Half syrup please!",
         "半糖！", "", "npc_shaved_ice"),

        ("n_l4_v3_full_sugar",  "d_l4_v3_010",
         "Full syrup please!",
         "全糖！", "", "npc_shaved_ice"),

        ("n_l4_v3_complete",    "d_l4_v3_011",
         "Here you go! Stay cool!",
         "来！消暑一下！", "", "npc_shaved_ice"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO dialogues VALUES (?,?,?,?,?,?)", dialogues)
    print(f"  Inserted {len(dialogues)} dialogue lines")


def populate_words(cursor):
    words = [
        # Path 1: 奶茶 keywords
        ("d_l4_v1_003", "w_l4_001",
         "珍珠奶茶", "Bubble Tea / Pearl Milk Tea",
         "Taiwan's most famous drink export, invented in the 1980s", ""),

        ("d_l4_v1_004", "w_l4_002",
         "大杯", "Large size",
         "Size customization: 大(large) 中(medium) 小(small)", ""),

        ("d_l4_v1_007", "w_l4_003",
         "几分糖", "How many percent sugar?",
         "Sugar level system unique to Taiwanese drink shops", ""),

        ("d_l4_v1_008", "w_l4_004",
         "无糖", "No sugar (bû-thn̂g)",
         "Zero sugar — for those who prefer unsweetened drinks", ""),

        ("d_l4_v1_009", "w_l4_005",
         "三分糖", "30% sugar",
         "Very lightly sweetened — popular health-conscious choice", ""),

        ("d_l4_v1_010", "w_l4_006",
         "半糖", "Half sugar / 50% sugar",
         "Most popular sugar level in Taiwan", ""),

        ("d_l4_v1_011", "w_l4_007",
         "七分糖", "70% sugar",
         "Slightly sweeter than half sugar", ""),

        ("d_l4_v1_012", "w_l4_008",
         "全糖", "Full sugar / 100% sugar",
         "Maximum sweetness — the default if you don't specify", ""),

        ("d_l4_v1_013", "w_l4_009",
         "几分冰", "How much ice?",
         "Ice level customization unique to Taiwanese drink shops", ""),

        ("d_l4_v1_014", "w_l4_010",
         "去冰", "No ice (khi-ping)",
         "Removes all ice — drink served at room temperature", ""),

        ("d_l4_v1_015", "w_l4_011",
         "少冰", "Less ice (sió-ping)",
         "Reduced ice — still cold but less diluted", ""),

        ("d_l4_v1_016", "w_l4_012",
         "正常冰", "Normal ice",
         "Standard amount of ice — default if not specified", ""),

        ("d_l4_v1_017", "w_l4_013",
         "多冰", "Extra ice",
         "Maximum ice — extra cold drink", ""),

        ("d_l4_v1_018", "w_l4_014",
         "加什么料", "What topping to add?",
         "料 means topping or ingredient added to a drink", ""),

        ("d_l4_v1_019", "w_l4_015",
         "珍珠", "Tapioca pearls (tsin-tsû)",
         "The iconic black chewy balls in bubble tea", ""),

        ("d_l4_v1_020", "w_l4_016",
         "椰果", "Coconut jelly",
         "Translucent cubes made from coconut water — chewy and refreshing", ""),

        # Path 2: 豆花 keywords
        ("d_l4_v2_002", "w_l4_017",
         "豆花", "Tofu Pudding (tāu-hue)",
         "Silky smooth tofu dessert — a classic Taiwanese comfort food", ""),

        ("d_l4_v2_004", "w_l4_018",
         "多放一点", "Add a little more",
         "Used to request more of something — syrup, toppings etc.", ""),

        ("d_l4_v2_005", "w_l4_019",
         "少放点", "A little less please",
         "Used to request less of something", ""),

        ("d_l4_v2_003", "w_l4_020",
         "仙草", "Grass jelly (sian-tsháu)",
         "A dark herbal jelly made from Chinese mesona plant", ""),

        ("d_l4_v2_003", "w_l4_021",
         "花生", "Peanut (hue-sing)",
         "Crushed peanuts are a popular topping for tofu pudding", ""),

        # Path 3: 剉冰 keywords
        ("d_l4_v3_002", "w_l4_022",
         "剉冰", "Shaved Ice (Tshuah-ping)",
         "Finely shaved ice — a beloved Taiwanese summer dessert", ""),

        ("d_l4_v3_004", "w_l4_023",
         "芋圆", "Taro balls (ōo-înn)",
         "Chewy taro-flavoured balls — a popular shaved ice topping", ""),

        ("d_l4_v3_006", "w_l4_024",
         "绿豆", "Mung bean (lio̍k-tāu)",
         "Sweet cooked mung beans — a refreshing shaved ice topping", ""),
    ]
    cursor.executemany("INSERT OR IGNORE INTO words VALUES (?,?,?,?,?,?)", words)
    print(f"  Inserted {len(words)} keyword vocabulary entries")


def populate_options(cursor):
    options = [
        # Path 1: 奶茶 — size selection
        ("n_l4_v1_menu", "o_l4_v1_001",
         "Large bubble tea please! / 大杯珍珠奶茶！",
         "n_l4_v1_large", "positive"),
        ("n_l4_v1_menu", "o_l4_v1_002",
         "Medium bubble tea please! / 中杯珍珠奶茶！",
         "n_l4_v1_medium", "positive"),
        ("n_l4_v1_menu", "o_l4_v1_003",
         "Small bubble tea please! / 小杯珍珠奶茶！",
         "n_l4_v1_small", "positive"),

        # Sugar level (shown after any size choice — using large as example)
        ("n_l4_v1_size_ask", "o_l4_v1_004",
         "No sugar! / 无糖！", "n_l4_v1_no_sugar", "positive"),
        ("n_l4_v1_size_ask", "o_l4_v1_005",
         "30% sugar! / 三分糖！", "n_l4_v1_30_sugar", "positive"),
        ("n_l4_v1_size_ask", "o_l4_v1_006",
         "Half sugar! / 半糖！", "n_l4_v1_50_sugar", "positive"),
        ("n_l4_v1_size_ask", "o_l4_v1_007",
         "70% sugar! / 七分糖！", "n_l4_v1_70_sugar", "positive"),
        ("n_l4_v1_size_ask", "o_l4_v1_008",
         "Full sugar! / 全糖！", "n_l4_v1_100_sugar", "positive"),

        # Ice level
        ("n_l4_v1_sugar_ask", "o_l4_v1_009",
         "No ice! / 去冰！", "n_l4_v1_no_ice", "positive"),
        ("n_l4_v1_sugar_ask", "o_l4_v1_010",
         "Less ice! / 少冰！", "n_l4_v1_less_ice", "positive"),
        ("n_l4_v1_sugar_ask", "o_l4_v1_011",
         "Normal ice! / 正常冰！", "n_l4_v1_normal_ice", "positive"),
        ("n_l4_v1_sugar_ask", "o_l4_v1_012",
         "Extra ice! / 多冰！", "n_l4_v1_extra_ice", "positive"),

        # Toppings
        ("n_l4_v1_ice_ask", "o_l4_v1_013",
         "Tapioca pearls please! / 加珍珠！",
         "n_l4_v1_pearl", "positive"),
        ("n_l4_v1_ice_ask", "o_l4_v1_014",
         "Coconut jelly please! / 加椰果！",
         "n_l4_v1_coconut", "positive"),
        ("n_l4_v1_ice_ask", "o_l4_v1_015",
         "Red bean please! / 加红豆！",
         "n_l4_v1_red_bean", "positive"),
        ("n_l4_v1_ice_ask", "o_l4_v1_016",
         "No toppings! / 不要加料！",
         "n_l4_v1_no_topping", "positive"),

        # Path 2: 豆花 — topping selection
        ("n_l4_v2_topping_ask", "o_l4_v2_001",
         "Red bean please! / 加红豆！",
         "n_l4_v2_red_bean", "positive"),
        ("n_l4_v2_topping_ask", "o_l4_v2_002",
         "Taro please! / 加芋头！",
         "n_l4_v2_taro", "positive"),
        ("n_l4_v2_topping_ask", "o_l4_v2_003",
         "Peanut please! / 加花生！",
         "n_l4_v2_peanut", "positive"),
        ("n_l4_v2_topping_ask", "o_l4_v2_004",
         "Grass jelly please! / 加仙草！",
         "n_l4_v2_grass_jelly", "positive"),

        # Syrup adjustment
        ("n_l4_v2_adjust_ask", "o_l4_v2_005",
         "More syrup please! / 多放一点！",
         "n_l4_v2_more_syrup", "positive"),
        ("n_l4_v2_adjust_ask", "o_l4_v2_006",
         "Less syrup please! / 少放点！",
         "n_l4_v2_less_syrup", "positive"),
        ("n_l4_v2_adjust_ask", "o_l4_v2_007",
         "It is fine as is! / 这样就好了！",
         "n_l4_v2_fine", "positive"),

        # Path 3: 剉冰 — topping selection
        ("n_l4_v3_topping_ask", "o_l4_v3_001",
         "Taro balls please! / 加芋圆！",
         "n_l4_v3_taro_ball", "positive"),
        ("n_l4_v3_topping_ask", "o_l4_v3_002",
         "Red bean please! / 加红豆！",
         "n_l4_v3_red_bean", "positive"),
        ("n_l4_v3_topping_ask", "o_l4_v3_003",
         "Mung bean please! / 加绿豆！",
         "n_l4_v3_mung_bean", "positive"),

        # Syrup level
        ("n_l4_v3_syrup_ask", "o_l4_v3_004",
         "No syrup! / 不要糖水！",
         "n_l4_v3_no_sugar", "positive"),
        ("n_l4_v3_syrup_ask", "o_l4_v3_005",
         "Half syrup! / 半糖！",
         "n_l4_v3_half_sugar", "positive"),
        ("n_l4_v3_syrup_ask", "o_l4_v3_006",
         "Full syrup! / 全糖！",
         "n_l4_v3_full_sugar", "positive"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO options VALUES (?,?,?,?,?)", options)
    print(f"  Inserted {len(options)} dialogue options")


def populate_events(cursor):
    events = [
        # Bubble tea — add to inventory regardless of customization
        ("o_l4_v1_013", "e_l4_001", "ADD_TO_INVENTORY",
         '{"item_id": "i_bubble_tea_1", "quantity": 1}'),
        ("o_l4_v1_014", "e_l4_002", "ADD_TO_INVENTORY",
         '{"item_id": "i_bubble_tea_1", "quantity": 1}'),
        ("o_l4_v1_015", "e_l4_003", "ADD_TO_INVENTORY",
         '{"item_id": "i_bubble_tea_1", "quantity": 1}'),
        ("o_l4_v1_016", "e_l4_004", "ADD_TO_INVENTORY",
         '{"item_id": "i_bubble_tea_1", "quantity": 1}'),

        # Tofu — add to inventory
        ("o_l4_v2_001", "e_l4_005", "ADD_TO_INVENTORY",
         '{"item_id": "i_tofu_1", "quantity": 1}'),
        ("o_l4_v2_002", "e_l4_006", "ADD_TO_INVENTORY",
         '{"item_id": "i_tofu_1", "quantity": 1}'),
        ("o_l4_v2_003", "e_l4_007", "ADD_TO_INVENTORY",
         '{"item_id": "i_tofu_1", "quantity": 1}'),
        ("o_l4_v2_004", "e_l4_008", "ADD_TO_INVENTORY",
         '{"item_id": "i_tofu_1", "quantity": 1}'),

        # Shaved ice — add to inventory
        ("o_l4_v3_001", "e_l4_009", "ADD_TO_INVENTORY",
         '{"item_id": "i_shaved_ice_1", "quantity": 1}'),
        ("o_l4_v3_002", "e_l4_010", "ADD_TO_INVENTORY",
         '{"item_id": "i_shaved_ice_1", "quantity": 1}'),
        ("o_l4_v3_003", "e_l4_011", "ADD_TO_INVENTORY",
         '{"item_id": "i_shaved_ice_1", "quantity": 1}'),
    ]
    cursor.executemany("INSERT OR IGNORE INTO events VALUES (?,?,?,?)", events)
    print(f"  Inserted {len(events)} events")


def verify(cursor):
    print("\n── Verification ")
    tables = ["npcs", "vendors", "items", "dialogue_nodes",
              "dialogues", "words", "options", "events"]
    for table in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table:20s} → {count} total rows")

    print("\n── Lesson 4 Vendors ")
    rows = cursor.execute("""
        SELECT v.vendor_id, v.vendor_name, n.npc_name
        FROM vendors v JOIN npcs n ON n.npc_id = v.npc_id
        WHERE v.node_id LIKE 'n_l4_%'
        ORDER BY v.vendor_id
    """).fetchall()
    for row in rows:
        print(f"  {row[0]:20s} | {row[1]:20s} | {row[2]}")

    print("\n── Sample: Bubble Tea Sugar Options ")
    opts = cursor.execute("""
        SELECT option_TEXT, next_node_id FROM options
        WHERE node_id = 'n_l4_v1_size_ask'
    """).fetchall()
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
    print("\nLesson 4 population complete!")
    print(f"   Database: {DB_PATH}")


if __name__ == "__main__":
    populate()