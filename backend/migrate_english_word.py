"""
Migration Script — Add english_word column to words table
Adds english_word to both hok_test_data.db and hok_lesson_data.db
and populates it for all existing keywords.

Run from your backend root folder:
    python migrate_english_word.py

Safe to run multiple times.
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATHS = {
    "hok_test_data":   os.path.join(BASE_DIR, "database", "hok_test_data.db"),
    "hok_lesson_data": os.path.join(BASE_DIR, "database", "hok_lesson_data.db"),
}

# ── English word mappings ─────────────────────────────────────────────────────
# word_id → english_word (the exact English word/phrase in the dialogue text
#            that should be replaced by the Chinese keyword)
ENGLISH_WORD_MAP = {

    # ── Lesson 0 ──────────────────────────────────────────────────────────────
    "w_l0_001": "Excuse me",          # 麻烦问一下
    "w_l0_002": "what is this",       # 这个是什么
    "w_l0_003": "pineapple cake",     # 凤梨酥
    "w_l0_004": "Excuse me",          # 请问
    "w_l0_005": "where to buy",       # 在哪里买
    "w_l0_006": "Hello",              # 老板好
    "w_l0_007": "what is this",       # 请问这是什么
    "w_l0_008": "try",                # 试吃
    "w_l0_009": "Yes",                # 好啊
    "w_l0_010": "pride",              # 台湾的骄傲
    "w_l0_011": "How many",           # 你要几个
    "w_l0_012": "Enjoy",              # 请慢用

    # ── Lesson 1 ──────────────────────────────────────────────────────────────
    "w_l1_001": "Hello",              # 老板好
    "w_l1_002": "what is this",       # 请问这是什么
    "w_l1_003": "fried sweet rice cake", # 白糖粿
    "w_l1_004": "sell",               # 怎么卖
    "w_l1_005": "five",               # 五块
    "w_l1_006": "twelve",             # 十二块
    "w_l1_007": "red bean pancake",   # 红豆饼
    "w_l1_008": "sell",               # 怎么卖
    "w_l1_009": "sweet potato balls", # 地瓜球
    "w_l1_010": "sell",               # 怎么卖

    # ── Lesson 2 ──────────────────────────────────────────────────────────────
    "w_l2_001": "much",               # 这个多少钱
    "w_l2_002": "six",                # 六块一个
    "w_l2_003": "two",                # 来两个吧
    "w_l2_004": "thank you",          # 谢谢
    "w_l2_005": "original",           # 原价
    "w_l2_006": "discount",           # 打七折
    "w_l2_007": "box",                # 一盒
    "w_l2_008": "prosper",            # 生意兴隆
    "w_l2_009": "free",               # 买一送一
    "w_l2_010": "deal",               # 做活动
    "w_l2_011": "delicious",          # 好好吃
    "w_l2_012": "cheaper",            # 可以便宜点吗
    "w_l2_013": "cannot",             # 不行
    "w_l2_014": "worries",            # 没关系
    "w_l2_015": "okay",               # 好吧
    "w_l2_016": "thank you",          # 谢谢你

    # ── Lesson 3 ──────────────────────────────────────────────────────────────
    "w_l3_001": "inside",             # 里面有什么
    "w_l3_002": "No thank you",       # 不用了，谢谢
    "w_l3_003": "Bahwan",             # 肉圆
    "w_l3_004": "starch",             # 地瓜粉
    "w_l3_005": "steam",              # 先蒸过再炸
    "w_l3_006": "contain",            # 这个里面有...吗
    "w_l3_007": "allergic",           # 过敏
    "w_l3_008": "allergic to beef",   # 我对牛肉过敏
    "w_l3_009": "beef",               # 牛肉
    "w_l3_010": "pork rice",          # 卤肉饭
    "w_l3_011": "seafood",            # 海鲜
    "w_l3_012": "oyster omelette",    # 蚵仔煎
    "w_l3_013": "original",           # 原味照烧酱
    "w_l3_014": "wasabi",             # 哇沙米
    "w_l3_015": "chili",              # 泰式甜辣酱

    # ── Lesson 4 ──────────────────────────────────────────────────────────────
    "w_l4_001": "bubble tea",         # 珍珠奶茶
    "w_l4_002": "large",              # 大杯
    "w_l4_003": "sugar",              # 几分糖
    "w_l4_004": "no sugar",           # 无糖
    "w_l4_005": "sugar",              # 三分糖
    "w_l4_006": "sugar",              # 半糖
    "w_l4_007": "sugar",              # 七分糖
    "w_l4_008": "sugar",              # 全糖
    "w_l4_009": "ice",                # 几分冰
    "w_l4_010": "no ice",             # 去冰
    "w_l4_011": "less ice",           # 少冰
    "w_l4_012": "normal ice",         # 正常冰
    "w_l4_013": "extra ice",          # 多冰
    "w_l4_014": "topping",            # 加什么料
    "w_l4_015": "pearls",             # 珍珠
    "w_l4_016": "coconut",            # 椰果
    "w_l4_017": "tofu",               # 豆花
    "w_l4_018": "more",               # 多放一点
    "w_l4_019": "less",               # 少放点
    "w_l4_020": "grass jelly",        # 仙草
    "w_l4_021": "peanut",             # 花生
    "w_l4_022": "shaved ice",         # 剉冰
    "w_l4_023": "taro balls",         # 芋圆
    "w_l4_024": "mung bean",          # 绿豆
}


def migrate_db(db_name, db_path):
    if not os.path.isfile(db_path):
        print(f"  ⚠️  {db_name} not found at {db_path} — skipping.")
        return

    print(f"\n{'='*60}")
    print(f"  Migrating: {db_name}")
    print(f"{'='*60}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 1 — Add english_word column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE words ADD COLUMN english_word TEXT DEFAULT ''")
        conn.commit()
        print("  ✅ Added english_word column to words table")
    except sqlite3.OperationalError:
        print("  ✅ english_word column already exists — skipping ALTER")

    # Step 2 — Populate english_word for all known word_ids
    updated = 0
    not_found = 0

    for word_id, english_word in ENGLISH_WORD_MAP.items():
        cursor.execute(
            "UPDATE words SET english_word = ? WHERE word_id = ?",
            (english_word, word_id)
        )
        if cursor.rowcount > 0:
            updated += 1
        else:
            not_found += 1

    conn.commit()
    print(f"  ✅ Updated {updated} keywords with english_word")
    if not_found > 0:
        print(f"  ⚠️  {not_found} word_ids not found in this db (expected if db is test only)")

    # Step 3 — Verify
    print(f"\n  ── Sample keywords with english_word ───────────────────")
    rows = cursor.execute("""
        SELECT word_id, word, english_word, translation
        FROM words
        WHERE english_word != '' AND english_word IS NOT NULL
        LIMIT 10
    """).fetchall()

    for row in rows:
        print(f"  {row[0]:12s} | {row[1]:15s} | EN: {row[2]:20s} | {row[3]}")

    total = cursor.execute(
        "SELECT COUNT(*) FROM words WHERE english_word != '' AND english_word IS NOT NULL"
    ).fetchone()[0]
    print(f"\n  Total keywords with english_word: {total}")

    conn.close()
    print(f"  ✅ {db_name} migration complete!")


def migrate():
    print("Adding english_word column to words table")
    print("Updating both databases...\n")

    for db_name, db_path in DB_PATHS.items():
        migrate_db(db_name, db_path)

    print(f"\n{'='*60}")
    print("Migration complete!")
    print("="*60)
    print("""
Next steps:
  1. In APIModel.cs  — add: public string english_word;  to KeyWordData
  2. In WordHoverHandler.cs — add: public string english_word; to KeyWordEntry
  3. In NPC.cs — pass english_word when building KeyWordEntry list
  4. Run the game and keywords should now replace in dialogue text!
    """)


if __name__ == "__main__":
    migrate()