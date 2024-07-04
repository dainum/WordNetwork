import requests
from bs4 import BeautifulSoup
import random
from janome.tokenizer import Tokenizer
import collections
import  time


def get_Gsearch_results(keyword,num_pages=1):
    #url = f"https://www.google.com/search?q={keyword}"
    #print(url)
    search_results=[]
    headers={
        "User-Agent":
            #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
            #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15"
           # "Mozilla/5.0(Windows NT 10.0;WIn64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/45.0.3029.110 Safari/537.3"
        #"Mozilla/5.0(Windows NT 10.0;WIn64;x64) AppleWebKit/555.35(KHTML, like Gecko) Chrome/48.20.3029.1100 Safari/545.3"
        "Mozilla/5.0(Windows NT 10.0;WIn64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/45.0.3029.110 Safari/537.3"
        
        #,
    }
    for page in range(num_pages):
        start = page * 10
        
        url = f"https://www.google.com/search?q={keyword}&start={start}"
        
        response = requests.get(url, headers=headers)
        time.sleep(1)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("h3")
        search_results.extend([r.text for r in results])

    return search_results
kw="りんご"
#assoc = get_Gsearch_results(kw)
#print("ANSWE:\n",assoc)

#print("JANOME")

t=Tokenizer()
lis=[]

count = 0
def r(a):
    Moco=""
    assoc = get_Gsearch_results(a)
    saihin = []
    for a_text in assoc:        
        #print(a_text)
        for token in t.tokenize(a_text):
            pos = token.part_of_speech.split(',')
            if pos[0]=="名詞" and (pos[1]=='一般' or pos[1]=='固有名詞')and token.surface not in lis and token.surface!='-' and 'サ変接続' not in pos:
                saihin.append(token.surface)
                #print(saihin)
    c = collections.Counter(saihin)
    #print(c)#回数が見れる
    print([i[0] for i in c.items() if i[1] >= 2])
    Moco=c.most_common()[0][0]
    #print(Moco)

    #print("単語は%sで回数は%d"%(Moco,c.most_common()[0][1]))
    lis.append(Moco)
    if len(lis)<=10:
        r(Moco)
    else :
        return       

"""
毎回変わる？['りんご', 'オンライン', '使い方', '文章', '書き方', '漢字', 'ペディア', 'エクスペディア', 'Expedia', 'ホテル', 'トラベル']14:15 2024年5月10日
['りんご', 'リンゴ', 'JA', '東京', '天気', '日本', '国土', '交通省', 'ニュース', 'NHK', '協会'] 14:21
['りんご', 'リンゴ', 'JA', '東京', 'TOKYO', 'Tokyo', 'Wikipedia', 'ウィキペディア', '使い方', '文章', '書き方']この後2回連続で同じ
時間で変化するのかもしれない
['りんご', '通販', 'ファッション', 'サイト', 'Google', 'ログイン', 'アカウント', '方法', '辞書', '
辞典', '国語']
"""

        
r(kw)
print(lis)
