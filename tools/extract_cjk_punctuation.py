"""
製作全字庫繁體楷書標點符號字型

🟢限制：
寒蟬正楷體 源自於 全字庫楷體。由於 全字庫正楷體 使用的是 1024 × 1024 的"畫布"，而 寒蟬正楷體 的作者在修改時，將畫布縮放改成了 1000 × 1000 的標準。所以無法透過 fontTools 合併出一個新的「具有繁體標點的寒蟬楷體」。

🟢新的策略：
用 Python 從《全字庫》中單獨切出一個只有 169 個標點符號的迷你字型（TW-Kai-Punct.ttf）。
將這個迷你字型跑 cn-font-split。
在 CSS 的 font-family 中，把標點符號字型排在第一順位，寒蟬正楷體排在第二順位。利用 CSS 字型備援 (Fallback)來處理標點問題。瀏覽器非常聰明，它會自動處理 1024 與 1000 的縮放問題，讓標點符號完美對齊！

這個做法的三大好處：
完全避開 UPM 錯誤：不用冒險修改字型的底層畫布，瀏覽器渲染引擎會自動幫你無縫縮放對齊。
模組化：未來如果你又找到了另一款大陸的好字型，你完全可以直接套用這個 tw-kai-punct 標點包，把它排在第一順位，瞬間就能把任何字型的標點「繁中化」！
極度輕量：因為只有標點，檔案極小，完全不影響載入速度。

🟢後續處理：

將輸出的 "TW-Kai-Punct.ttf" 進行切片。

在切片後的 result.css，搜尋「font-family:"TW-Kai"」取代為「font-family:"TW-Kai-Punct"」，這就是CSS中使用的名稱。(開頭註解部分的 TW-Kai 也可以順便加 -Punct ，不過不是必要的。)

以同樣的方式也製作 TW-Sung-Punct 供宋體使用。

"""

import os
import unicodedata
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

script_dir = os.path.dirname(os.path.abspath(__file__))

# 檔案路徑設定
input_path = os.path.join(script_dir, "TW-Kai-98_1.ttf")
output_path = os.path.join(script_dir, "TW-Kai-Punct.ttf")  # 只輸出純標點字型
# input_path = os.path.join(script_dir, "TW-Sung-98_1.ttf")
# output_path = os.path.join(script_dir, "TW-Sung-Punct.ttf")

print("1. 正在分析 Unicode 區塊並自動篩選中文標點字碼...")
TARGET_BLOCKS = [
    (0x2000, 0x206F),
    (0x3000, 0x303F),
    (0xFE10, 0xFE1F),
    (0xFE30, 0xFE4F),
    (0xFF00, 0xFFEF),
]

punctuation_unicodes = set()
for start, end in TARGET_BLOCKS:
    for codepoint in range(start, end + 1):
        char = chr(codepoint)
        category = unicodedata.category(char)
        if category.startswith("P") or codepoint == 0x3000:
            punctuation_unicodes.add(codepoint)

print(f"   -> 共鎖定 {len(punctuation_unicodes)} 個標點/全形空白字碼。")

print("2. 正在從《全字庫》擷取居中標點...")
tw_font = TTFont(input_path)

options = Options()
# 為了網頁載入最佳化，我們不保留多餘的排版表格
options.layout_features = []
subsetter = Subsetter(options=options)
subsetter.populate(unicodes=punctuation_unicodes)
subsetter.subset(tw_font)

print("3. 儲存純標點字型...")
tw_font.save(output_path)

print("✨ 成功！已生成只有標點符號的迷你字型")
