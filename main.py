"""
MeCabを利用した超簡単なロジックの漢字読み間違え
"""
import sys
import MeCab

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

print()
print("入力単語:", text)
print("変換前ヨミ -> ", before_text)


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

print()
print("-"*10)
print()
print("変換後ヨミ ->", output_text)
print()
