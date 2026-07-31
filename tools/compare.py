"""
比較 寒蟬 兩個檔案之間的差異
"""

from fontTools.ttLib import TTFont

# 載入兩個字型檔案（請替換成你實際的檔案名稱與路徑）
font_large = TTFont('ChillKai.ttf')  # 33080字的版本
font_big5 = TTFont('ChillKai_Big5.ttf')    # 21192字的 Big5 版本

# 取得字碼集合 (Unicode CMAP)
cmap_large = set(font_large.getBestCmap().keys())
cmap_big5 = set(font_big5.getBestCmap().keys())

print(f"【大字集版】收錄字數: {len(cmap_large)}")
print(f"【Big5 版】收錄字數: {len(cmap_big5)}")

only_in_big5 = cmap_big5 - cmap_large
only_in_large = cmap_large - cmap_big5

print(f"➜ 僅在 Big5 版有、大字集版沒有的字碼數: {len(only_in_big5)}")
print(f"➜ 大字集版多出來的字碼數: {len(only_in_large)}")