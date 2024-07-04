import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
import japanize_matplotlib
#fonts = set([f.name for f in matplotlib.font_manager.fontManager.ttflist])
G = nx.Graph()
#print(fonts)
 
# nodeデータの追加
G.add_nodes_from(["りんご", "B", "C", "D", "E", "F"])
 
# edgeデータの追加
G.add_edges_from([("りんご", "B"), ("B", "C"), ("B", "F"),("C", "D"), ("C", "E"), ("C", "F"), ("B", "F")])

japanize_matplotlib.japanize()
plt.figure()
# ネットワークの可視化
nx.draw(G, with_labels = True,font_family='IPAexGothic')
plt.savefig("test/photo/3.png", bbox_inches="tight")
plt.legend()
plt.show()

#url