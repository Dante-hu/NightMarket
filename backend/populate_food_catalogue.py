"""
Food Catalogue Population Script
Adds all night market dishes as proper items and vendors
to both hok_test_data.db and hok_lesson_data.db.

Run from your backend root folder:
    python populate_food_catalogue.py

Safe to run multiple times — uses INSERT OR IGNORE.

Covers all dishes from the lesson plan:
    Lesson 0: 凤梨酥, 麻吉
    Lesson 1: 白糖粿, 红豆饼, 地瓜球
    Lesson 2: 胡椒饼, 鸡翅包饭, 新竹贡丸, 筒仔米糕, 芋粿巧
    Lesson 3: 蚵仔煎, 肉圆, 担仔面, 卤肉饭, 牛肉面
    Lesson 4: 豆花, 剉冰, 奶茶
    Lesson 5: 木瓜牛奶, 大肠包小肠
"""

import sqlite3
import os

# Both databases to update
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATHS = {
    "hok_test_data":   os.path.join(BASE_DIR, "database", "hok_test_data.db"),
    "hok_lesson_data": os.path.join(BASE_DIR, "database", "hok_lesson_data.db"),
}

# ── Food catalogue ────────────────────────────────────────────────────────────
# Each entry: (vendor_id, item_id, english_name, chinese_name, romanization,
#              description, price, lesson)

FOOD_CATALOGUE = [

    # ── Lesson 0 ──────────────────────────────────────────────────────────────
    (
        "v_pineapple", "i_pineapple_cake",
        "Pineapple Cake", "凤梨酥", "ông-lâi-soo",
        "A classic Taiwanese pastry filled with sweet pineapple jam. "
        "Crispy on the outside, soft and tangy on the inside. "
        "One of Taiwan's most iconic souvenirs.",
        20, 0
    ),
    (
        "v_mochi", "i_mochi",
        "Mochi", "麻吉", "Muâ-tsî",
        "Soft and chewy Japanese-style rice cake popular in Taiwan. "
        "Comes in various sweet fillings. "
        "Traditionally, family members come together to make mochi, "
        "and it is eaten at weddings.",
        15, 0
    ),

    # ── Lesson 1 ──────────────────────────────────────────────────────────────
    (
        "v_beh_teung_guai", "i_fried_rice_cake",
        "Fried Sweet Rice Cake", "白糖粿", "Beh Teung Guai",
        "A chewy fried sweet rice cake coated in sugar. "
        "A classic Taiwanese street snack with a crispy outside "
        "and soft chewy inside.",
        5, 1
    ),
    (
        "v_red_bean_pancake", "i_red_bean_pancake",
        "Red Bean Pancake", "红豆饼（管仔粿）", "kóng-á-kér",
        "A fluffy pancake filled with sweet red bean paste. "
        "Cooked fresh on a round iron mould at the stall.",
        5, 1
    ),
    (
        "v_sweet_potato", "i_sweet_potato_balls",
        "Sweet Potato Balls", "地瓜球", "ti-kue-kiunn",
        "Crispy golden balls made from sweet potato and tapioca starch. "
        "Light and hollow inside, chewy on the outside. "
        "A popular Taiwanese night market snack.",
        5, 1
    ),

    # ── Lesson 2 ──────────────────────────────────────────────────────────────
    (
        "v_pepper_bun", "i_pepper_bun",
        "Pepper Bun", "胡椒饼", "hû-tsio-piánn",
        "A crispy baked bun filled with juicy pepper-seasoned pork. "
        "Cooked in a clay oven, famous for its smoky charred flavour. "
        "Best eaten hot straight from the oven.",
        6, 2
    ),
    (
        "v_chicken_wing", "i_chicken_wing_rice",
        "Chicken Wing Rice Roll", "鸡翅包饭", "ke-si-pau-png",
        "A deboned chicken wing stuffed with sticky rice and fillings. "
        "A creative and filling Taiwanese street food invention.",
        7, 2
    ),
    (
        "v_pork_ball", "i_pork_ball",
        "Hsinchu Pork Ball", "新竹贡丸", "Kong-uân",
        "Springy pork meatballs originating from Hsinchu city. "
        "Famous for their extremely chewy and bouncy texture. "
        "A specialty product of Hsinchu, Taiwan.",
        5, 2
    ),
    (
        "v_tube_pudding", "i_tube_rice_pudding",
        "Tube Rice Pudding", "筒仔米糕", "tháng-á-bí-ko",
        "Sticky rice cooked in a bamboo tube with pork and mushrooms. "
        "Served upside down with a sweet soy sauce on top. "
        "A traditional Taiwanese comfort food.",
        8, 2
    ),
    (
        "v_taro_cake", "i_taro_cake",
        "Steamed Taro Cake", "芋粿巧", "ōo-kué",
        "A soft steamed cake made from taro and rice flour. "
        "Lightly savoury with a smooth natural taro flavour. "
        "A traditional Hakka-influenced Taiwanese snack.",
        6, 2
    ),

    # ── Lesson 3 ──────────────────────────────────────────────────────────────
    (
        "v_oyster_omelette", "i_oyster_omelette",
        "Oyster Omelette", "蚵仔煎", "o-a-tsian",
        "A savoury omelette made with fresh oysters, egg, and sweet potato starch. "
        "Served with your choice of sauce: original teriyaki, wasabi, "
        "or Thai sweet chili sauce. One of Taiwan's most iconic street foods.",
        80, 3
    ),
    (
        "v_bahwan", "i_bahwan",
        "Bahwan", "肉圆", "bah-uân",
        "A Taiwanese round dumpling made of translucent sweet potato starch "
        "and rice flour, filled with pork and bamboo shoots. "
        "Steamed first then deep fried until golden.",
        50, 3
    ),
    (
        "v_danzai_noodles", "i_danzai_noodles",
        "Danzai Noodles", "担仔面", "Tàⁿ-á-mī",
        "Thin noodles in a rich shrimp broth topped with minced pork, "
        "fresh shrimp, and a braised egg. "
        "Originally sold by fishermen during the off-season in Tainan.",
        60, 3
    ),
    (
        "v_pork_rice", "i_minced_pork_rice",
        "Minced Pork Rice", "卤肉饭", "ló-bah-pn̄g",
        "Braised minced pork belly slow-cooked in soy sauce and spices, "
        "served over steamed white rice. "
        "One of Taiwan's most beloved everyday comfort foods.",
        40, 3
    ),
    (
        "v_beef_noodle", "i_beef_noodle_soup",
        "Taiwan Beef Noodle Soup", "牛肉面", "gû-bah-mī",
        "Thick wheat noodles in a rich braised beef broth with "
        "tender slow-cooked beef slices and vegetables. "
        "Taiwan's most internationally recognized noodle dish.",
        120, 3
    ),

    # ── Lesson 4 ──────────────────────────────────────────────────────────────
    (
        "v_tofu", "i_tofu_pudding",
        "Tofu Pudding", "豆花", "tāu-hue",
        "Silky smooth tofu pudding served with sweet ginger syrup. "
        "Choose your toppings: red bean, taro, peanut, or grass jelly. "
        "Available hot or cold. A classic Taiwanese dessert.",
        40, 4
    ),
    (
        "v_shaved_ice", "i_shaved_ice",
        "Shaved Ice", "冰沙（剉冰）", "Tshuah-ping",
        "Finely shaved ice topped with your choice of toppings: "
        "red bean, taro, taro ball, grass jelly, mung bean, "
        "red sugar syrup, or peanut. "
        "A beloved Taiwanese summer dessert. "
        "Featured in the famous song 剉冰进行曲.",
        50, 4
    ),
    (
        "v_bubble_tea", "i_bubble_tea",
        "Bubble Tea", "奶茶（珍珠奶茶）", "tsin-tsû-ling-tsa",
        "Classic Taiwanese milk tea fully customizable with: "
        "size (large/medium/small), "
        "sugar level (no sugar/30/50/70/100%), "
        "ice level (no/less/normal/extra), "
        "toppings (pearl/coconut jelly/red bean). "
        "Invented in Taiwan in the 1980s.",
        60, 4
    ),

    # ── Lesson 5 ──────────────────────────────────────────────────────────────
    (
        "v_papaya_milk", "i_papaya_milk",
        "Papaya Milk", "木瓜牛奶", "bok-kue-gu-ni",
        "Fresh papaya blended with cold milk and a touch of sugar. "
        "A classic Taiwanese fruit milk drink. "
        "Best enjoyed fresh at the stall.",
        45, 5
    ),
    (
        "v_sausage", "i_sausage_in_sausage",
        "Small Sausage in Large Sausage", "大肠包小肠", "tuā-tn̂g-pau-sió-tn̂g",
        "A grilled sticky rice sausage (large) stuffed with a "
        "grilled pork sausage (small), topped with garlic, "
        "basil, and condiments. "
        "A uniquely Taiwanese street food creation.",
        60, 5
    ),
]

# ── Vendor catalogue ──────────────────────────────────────────────────────────
# New vendors needed for lesson 5 dishes
LESSON_5_VENDORS = [
    ("v_papaya_milk", "n_l5_v1_greet", "npc_papaya_milk",  "木瓜牛奶 Stall"),
    ("v_sausage",     "n_l5_v2_greet", "npc_sausage",      "大肠包小肠 Stall"),
]

LESSON_5_NPCS = [
    ("npc_papaya_milk", "Papaya Milk Vendor"),
    ("npc_sausage",     "Sausage Vendor"),
]


def ensure_tables(cursor):
    """Makes sure all required tables exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS npcs (
            npc_id TEXT PRIMARY KEY,
            npc_name TEXT
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


def populate_db(db_name, db_path):
    if not os.path.isfile(db_path):
        print(f"  ⚠️  {db_name} not found at {db_path} — skipping.")
        return

    print(f"\n{'='*60}")
    print(f"  Updating: {db_name}")
    print(f"{'='*60}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    ensure_tables(cursor)

    # ── Add Lesson 5 NPCs and vendors ────────────────────────────────
    cursor.executemany(
        "INSERT OR IGNORE INTO npcs VALUES (?,?)", LESSON_5_NPCS)
    print(f"  ✅ Inserted/verified Lesson 5 NPCs")

    cursor.executemany(
        "INSERT OR IGNORE INTO vendors VALUES (?,?,?,?)", LESSON_5_VENDORS)
    print(f"  ✅ Inserted/verified Lesson 5 vendors")

    # ── Insert all food items ─────────────────────────────────────────
    inserted = 0
    skipped = 0

    for food in FOOD_CATALOGUE:
        vendor_id, item_id, english_name, chinese_name, romanization, \
            description, price, lesson = food

        # Build full item name: English (Chinese, romanization)
        full_name = f"{english_name} ({chinese_name}, {romanization})"

        existing = cursor.execute(
            "SELECT item_id FROM items WHERE item_id = ?",
            (item_id,)).fetchone()

        if existing:
            # Update existing item with better data
            cursor.execute("""
                UPDATE items
                SET item_name = ?, item_description = ?, item_value = ?
                WHERE item_id = ?
            """, (full_name, description, price, item_id))
            skipped += 1
        else:
            cursor.execute(
                "INSERT INTO items VALUES (?,?,?,?,?)",
                (vendor_id, item_id, full_name, description, price))
            inserted += 1

    conn.commit()

    print(f"  ✅ Inserted {inserted} new items")
    print(f"  ✅ Updated {skipped} existing items")

    # ── Verify ────────────────────────────────────────────────────────
    print(f"\n  ── Food Catalogue ({db_name}) ──────────────────────────")
    rows = cursor.execute("""
        SELECT i.item_id, i.item_name, i.item_value, i.vendor_id
        FROM items i
        ORDER BY i.vendor_id
    """).fetchall()

    current_lesson = -1
    lesson_labels = {
        "v_pineapple": 0, "v_mochi": 0,
        "v_beh_teung_guai": 1, "v_red_bean_pancake": 1, "v_sweet_potato": 1,
        "v_pepper_bun": 2, "v_chicken_wing": 2, "v_pork_ball": 2,
        "v_tube_pudding": 2, "v_taro_cake": 2,
        "v_oyster_omelette": 3, "v_bahwan": 3, "v_danzai_noodles": 3,
        "v_pork_rice": 3, "v_beef_noodle": 3,
        "v_tofu": 4, "v_shaved_ice": 4, "v_bubble_tea": 4,
        "v_papaya_milk": 5, "v_sausage": 5,
    }

    for row in rows:
        lesson = lesson_labels.get(row[3], -1)
        if lesson != current_lesson:
            current_lesson = lesson
            label = f"Lesson {lesson}" if lesson >= 0 else "Other"
            print(f"\n  [{label}]")
        print(f"    {row[0]:30s} | {row[1]:55s} | ${row[2]}")

    conn.close()
    print(f"\n  ✅ {db_name} update complete!")


def populate():
    print("Food Catalogue Population Script")
    print("Updating both hok_test_data.db and hok_lesson_data.db\n")

    for db_name, db_path in DB_PATHS.items():
        populate_db(db_name, db_path)

    print("\n" + "="*60)
    print("All databases updated!")
    print("="*60)
    print("""
Summary of all dishes added:
  Lesson 0: Pineapple Cake, Mochi
  Lesson 1: Fried Sweet Rice Cake, Red Bean Pancake, Sweet Potato Balls
  Lesson 2: Pepper Bun, Chicken Wing Rice Roll, Hsinchu Pork Ball,
            Tube Rice Pudding, Steamed Taro Cake
  Lesson 3: Oyster Omelette, Bahwan, Danzai Noodles,
            Minced Pork Rice, Beef Noodle Soup
  Lesson 4: Tofu Pudding, Shaved Ice, Bubble Tea
  Lesson 5: Papaya Milk, Small Sausage in Large Sausage
    """)


if __name__ == "__main__":
    populate()