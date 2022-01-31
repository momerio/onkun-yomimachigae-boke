# 各ライブラリのインポート 
import requests 
from bs4 import BeautifulSoup as bs 
from fake_useragent import UserAgent 
from selenium import webdriver 
import time 
import jaconv 
from selenium.common.exceptions import NoSuchElementException 
from webdriver_manager.chrome import ChromeDriverManager 
 
# HTML情報を取得する関数 
def get_html(url): 
    headers = {"User-Agent":useragent} 
    res = requests.get(url, headers = headers) 
    return bs(res.content, "html.parser")     
 
# Web操作をするのに必要な準備をする。 
options = webdriver.ChromeOptions()  
options.add_argument('--headless')  
driver =webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)    
 
# UserAgentを作成とランダムにUserAgentに設定 
ua = UserAgent()         
useragent = ua.random    
 
# 訓読みと２文字の漢字を格納するリスト 
new_kanji_list = [] 
kanji_list = [('カイ', '会'), ('カイ', '回'), ('カイ', '灰'), ('カイ', '改'), ('カイ', '快'), ('カイ', '海'), ('カイ', '界'), ('カイ', '械'), ('カイ', '絵'), ('カイ', '開'), ('カイ', '階'), ('カイ', '街'), ('カイ', '解'), ('カイ', '貝'), ('カイ', '下位'), ('カイ', '甲斐')] 
 
# kanji_list内の要素分繰り返す 
for i, kanji in enumerate(kanji_list): 
    # リスト内の漢字が１文字なら音訓読みを判別する 
    if len(kanji[1]) == 1: 
        print(kanji[1]) 
        try: 
            # 漢字検索サイトへアクセス 
            driver.get(r'http://kakijun.com/kanji/yomi/')  
            time.sleep(2) 
            # 該当漢字を入力フォームに挿入 
            form = driver.find_element_by_xpath(r'//*[@id="txt"]') 
            form.send_keys(kanji[1])  
            time.sleep(1) 
            # 検索ボタンを押す 
            search_btn = driver.find_element_by_id("btn") 
            search_btn.click() 
            # 現在のURLを取得 
            cur_url = driver.current_url 
            web_url = r"{}".format(cur_url) 
            # 現在のURLからHTML要素を取得する 
            soups = get_html(web_url) 
            # 訓読みの部分を取得する 
            kunyomi = soups.find(class_='kanjitableinfo').find_all('tr')[3].find(class_='infocontent').text.replace("\n","") 
            # ひらがなをカタカナに変換する(取得してきた訓読みがひらがな表示の為) 
            kunyomi = jaconv.hira2kata(kunyomi) 
            # 訓読みがない場合は「ナシ」を代入 
            if kunyomi == "": 
                kunyomi = "ナシ" 
            # 取得した訓読みとkanji_listに記載されているカタカナが同じ場合はnew_kanji_listに追加。 
            if kunyomi in kanji[0]: 
                print("訓:",kanji_list[i]) 
                new_kanji_list.append(kanji) 
        except NoSuchElementException: 
            # 要素が見つからない場合はGoogle Chromeを閉じる 
            driver.close() 
    else: 
        # ２文字の漢字はnew_kanji_listに追加 
        new_kanji_list.append(kanji) 
        continue 
    time.sleep(5) 
print("元リスト:",kanji_list)
# 最後にnew_kanji_listに追加した訓読みと２文字の漢字を表示する 
print("新リスト:",new_kanji_list) 
driver.close()


