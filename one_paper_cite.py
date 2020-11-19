# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 17:22:52 2020

@author: LINMUX
"""

import pandas as pd
import numpy as np
import cite
import networkx as nx
import matplotlib.pyplot as plt 


def plot_nx(title, cite_titles):
    G = nx.DiGraph()
    G.add_nodes_from(cite_titles)
    G.add_node(title)
    G.add_edges_from([(title, item) for item in cite_titles])
    
    pos = nx.spring_layout(G, k=0.4)
    options = {
        "edge_color": "grey",
        "linewidths": 0,
        "width": 0.1,
    }
    nx.draw_networkx(G, pos)
    nodes = list(G.nodes())
    plt.figure(figsize=(32,32))
    nx.draw(G, pos, **options)
    for i in range(nodes.__len__()):
        plt.annotate(s=nodes[i], xy=list(pos.values())[i]-np.array([len(nodes[i])/2*0.0001, 0]), xytext=list(pos.values())[i]-np.array([len(nodes[i])/2*0.005, 0]))
    plt.savefig('./{}.jpg'.format(title))



Cite_class = cite.Cite()
title = 'ImageNet-trained CNNs are biased towards texture; increasing shape bias improves accuracy and robustness'
cite_titles = Cite_class.dig_onepaper_title(title, mode='cite')
Cite_class.browser.quit()

