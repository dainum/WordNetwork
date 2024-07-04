import requests
from bs4 import BeautifulSoup
import time
import collections
import matplotlib.pyplot as plt
import networkx as nx
import japanize_matplotlib
from janome.tokenizer import Tokenizer

def get_Gsearch_results(keyword, num_pages=1):
    search_results = []
    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;WIn64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/45.0.3029.110 Safari/537.3"
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

def extract_keywords(assoc, t):
    saihin = []
    for a_text in assoc:
        for token in t.tokenize(a_text):
            pos = token.part_of_speech.split(',')
            if pos[0] == "名詞" and (pos[1] == '一般' or pos[1] == '固有名詞') and token.surface not in lis and token.surface != '-' and 'サ変接続' not in pos:
                saihin.append(token.surface)
    return saihin

def create_network_graph(keywords):
    G = nx.Graph()
    for i, keyword in enumerate(keywords):
        G.add_node(keyword)
        if i > 0:
            G.add_edge(keywords[i-1], keyword)
    japanize_matplotlib.japanize()
    plt.figure()
    nx.draw(G, with_labels=True, font_family='IPAexGothic')
    plt.savefig("test/photo/keywords_network.png", bbox_inches="tight")
    plt.show()

kw = "りんご"
t = Tokenizer()
lis = []

def recursive_search(keyword):
    assoc = get_Gsearch_results(keyword)
    saihin = extract_keywords(assoc, t)
    c = collections.Counter(saihin)
    common_keywords = [i[0] for i in c.items() if i[1] >= 2]
    if not common_keywords:
        return
    Moco = common_keywords[0]
    lis.append(Moco)
    if len(lis) <= 10:
        recursive_search(Moco)
    else:
        return

recursive_search(kw)
print(lis)

create_network_graph(lis)
