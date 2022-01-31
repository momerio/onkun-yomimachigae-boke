
from logging import BufferingFormatter
import sys
import MeCab
# import re
# import csv

# FILE_PATH = "data/Joyo_Kanji.csv"


# class KanjiData:
#     def __init__(self):
#         self.kanji = None
#         self.on = []
#         self.kun = []

#     def add_kun(self, kun):
#         self.kun.append(kun)

#     def add_on(self, on):
#         self.on.append(on)

#     def print(self):
#         print("漢字:{}, ヨミ:{}, よみ:{}".format(self.kanji, self.on, self.kun))


# import_data = []

# # csv読み込み
# with open(FILE_PATH, "r", encoding="UTF-8") as f:
#     reader = csv.reader(f)
#     reader.__next__()  # ラベルスキップ
#     for row in reader:
#         import_data.append(row)

# kanji_data = []

# # 正規表現: カタカナ
# re_katakana = re.compile(r'[\u30A1-\u30F4]+')

# # 正規表現: ひらがな
# re_hiragana = re.compile(r'^[あ-ん\-]+$')

# i = 0
# for data in import_data:
#     """
#     音読み訓読み判定
#     最後の要素，|で分けられる．
#     カタカナならば音読み，ひらがなならば訓読み．
#     """
#     temp_kanjiData = KanjiData()
#     temp_kanjiData.kanji = data[1]

#     for before_words in data[-1].split("|"):
#         # カタカナならば音読み
#         if re_katakana.fullmatch(before_words):
#             temp_kanjiData.add_on(before_words)
#         # ひらがなならば訓読み
#         elif re_hiragana.fullmatch(before_words):
#             temp_kanjiData.add_kun(before_words)

#     # data変数に格納
#     kanji_data.append(temp_kanjiData)

# for idx in kanji_data[:15]:
#     idx.print()


# mecab

mecab = MeCab.Tagger("-Ochasen")
text = sys.argv[1]


def get_word_info(text):
    mecab_result = []
    for line in mecab.parse(text).split("\n"):
        if line == "EOS":
            break
        else:
            mecab_result.append(line.split())
    return mecab_result


class Word:
    def __init__(self, kanji, yomi, hinshi):
        self.kanji = kanji
        self.yomi = yomi
        self.hinshi = hinshi


def set_word(mecab):
    word_list = []
    for word in mecab:
        hinshi_go = word[3].split("-")
        hinshi = hinshi_go[0]
        word_list.append(Word(word[0], word[1], hinshi))
    return word_list


# Wordクラスに格納して，形態素解析をする
before_words = set_word(get_word_info(text))

# print(get_word_info(sent))

before_text = ""
# チェック
for idx in before_words:
    before_text += idx.yomi
print("入力単語:", text)
print("変換前:", before_text)


"""
1文字ずつ変換
"""
combination_list = []
for idx in text:
    combination_list.append(get_word_info(idx))

after_words = []
for idx in combination_list:
    after_words.append(set_word(idx)[0])
# print(after_words)

output_text = ""

# チェック
for idx in after_words:
    # print(idx.kanji, idx.yomi, idx.hinshi)
    output_text += idx.yomi

print("-"*10)
print("変換後:", output_text)
