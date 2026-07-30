import os
from fontTools.ttLib import TTFont
from fontTools.merge import Merger

# 取得當前腳本所在的目錄，確保路徑正確
script_dir = os.path.dirname(os.path.abspath(__file__))

file_big5 = os.path.join(script_dir, "ChillKai_Big5.ttf")
file_large = os.path.join(script_dir, "ChillKai.ttf")
temp_big5 = os.path.join(script_dir, "temp_big5.ttf")
temp_large = os.path.join(script_dir, "temp_large.ttf")
output_file = os.path.join(script_dir, "ChillKai-Merged.ttf")

print("1. 正在載入字型檔...")
font1 = TTFont(file_big5)
font2 = TTFont(file_large)

# 清除造成合併崩潰的 OpenType Layout 表格 (GSUB, GPOS, GDEF)
print("2. 清理無效的排版表格 (GSUB / GPOS / GDEF)...")
layout_tables = ["GSUB", "GPOS", "GDEF"]
for tag in layout_tables:
    if tag in font1:
        del font1[tag]
    if tag in font2:
        del font2[tag]

# 儲存為乾淨的臨時檔
font1.save(temp_big5)
font2.save(temp_large)

print("3. 開始進行字型合併...")
merger = Merger()
merged_font = merger.merge([temp_big5, temp_large])

print("4. 儲存合併成果...")
merged_font.save(output_file)

# 刪除臨時檔
if os.path.exists(temp_big5):
    os.remove(temp_big5)
if os.path.exists(temp_large):
    os.remove(temp_large)

print("✨ 成功！已生成合併後的字型檔：ChillKai-Merged.ttf")
