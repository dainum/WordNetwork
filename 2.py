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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.3029.110 Safari/537.3"
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

t = Tokenizer()

def make_lis(a, G, depth, max_depth):
    if depth > max_depth:
        return []
    assoc = get_Gsearch_results(a)
    saihin = []
    for a_text in assoc:
        for token in t.tokenize(a_text):
            pos = token.part_of_speech.split(',')
            if pos[0] == "名詞" and (pos[1] == '一般' or pos[1] == '固有名詞') and token.surface != '-' and 'サ変接続' not in pos:
                saihin.append(token.surface)
    c = collections.Counter(saihin)
    keywords = [i[0] for i in c.items() if i[1] >= 2]
    create_network_graph(a, keywords, G)
    for keyword in keywords:
        if depth < max_depth:
            make_lis(keyword, G, depth + 1, max_depth)
    return

def create_network_graph(parent, keywords, G):
    G.add_node(parent)
    for keyword in keywords:
        G.add_node(keyword)
        G.add_edge(parent, keyword)

def main():
    G = nx.Graph()
    max_depth = 2  # 再帰の深さを2に設定
    make_lis("りんご", G, 0, max_depth)
    japanize_matplotlib.japanize()
    plt.figure()
    nx.draw(G, with_labels=True, font_family='IPAexGothic', node_size=2000, node_color="lightblue")
    plt.savefig("keywords_network.png", bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    main()
