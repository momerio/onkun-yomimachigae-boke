
import MeCab
import re
import csv

FILE_PATH = "data/Joyo_Kanji.csv"


class KanjiData:
    def __init__(self):
        self.kanji = None
        self.on = []
        self.kun = []

    def add_kun(self, kun):
        self.kun.append(kun)

    def add_on(self, on):
        self.on.append(on)

    def print(self):
        print("漢字:{}, ヨミ:{}, よみ:{}".format(self.kanji, self.on, self.kun))


import_data = []

# csv読み込み
with open(FILE_PATH, "r", encoding="UTF-8") as f:
    reader = csv.reader(f)
    reader.__next__()  # ラベルスキップ
    for row in reader:
        import_data.append(row)

kanji_data = []

# 正規表現: カタカナ
re_katakana = re.compile(r'[\u30A1-\u30F4]+')

# 正規表現: ひらがな
re_hiragana = re.compile(r'^[あ-ん\-]+$')

i = 0
for data in import_data:
    """
    音読み訓読み判定
    最後の要素，|で分けられる．
    カタカナならば音読み，ひらがなならば訓読み．
    """
    temp_kanjiData = KanjiData()
    temp_kanjiData.kanji = data[1]

    for word in data[-1].split("|"):
        # カタカナならば音読み
        if re_katakana.fullmatch(word):
            temp_kanjiData.add_on(word)
        # ひらがなならば訓読み
        elif re_hiragana.fullmatch(word):
            temp_kanjiData.add_kun(word)

    # data変数に格納
    kanji_data.append(temp_kanjiData)

# for idx in kanji_data[:15]:
#     idx.print()
