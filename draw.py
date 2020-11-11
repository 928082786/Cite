#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 08:30:19 2020

@author: cx
"""

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

def parse_edges(ref_papers, searched, ref_df):
    '''
    Parameters
    ----------
    ref_papers : list
        reference relationship.
        for example, ref_papers[0] = ['@inproceedingsKrizhevsky2017ImageNetCW','@inproceedingsZeiler2014VisualizingAU','@articleBengio2007LearningDA',]
        papers[0] = ref_df[ref_df['title']==searched[0]]['id'][0]
    
    searched: deque
        already searched papers
    
    red_df: paper_dataframe
    
    Returns
    -------
    list.
    '''
    assert len(ref_papers)==len(searched)
    edges = []
    for i in range(len(searched)):
        p = ref_df[ref_df['title']==searched[i]]['id'].item()
        for idx in ref_papers[i]:
            edges.append((p, idx))
    return edges


def plot_nx(nodes, edges, ref_df):
    '''
    Parameters
    ----------
    nodes : list
        paper_id.
    edges : references
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
     
    pos = nx.spring_layout(G, k=0.2)
    options = {
        "edge_color": "grey",
        "linewidths": 0,
        "width": 0.1,
    }
    
    G_deg = list(G.degree())
    node_size = [de for idx, de in G_deg]
    argsort = np.argsort(np.array(node_size))
    
    plt.figure(figsize=(16,16))
    nx.draw(G, pos, **options, node_size = node_size, node_color = node_size)
    for i in range(10):
        plt.annotate(text=G_deg[argsort[-i-1]], xy=list(pos.values())[argsort[-i-1]], xytext=list(pos.values())[argsort[-i-1]]+np.array([0.1*(i-5), 0.15*(i-7)]), arrowprops=dict(arrowstyle='-|>'))
    plt.savefig('./paper.jpg')
    
def plot(ref_papers, searched, ref_df):
    nodes = ref_df['id'].tolist()
    edges = parse_edges(ref_papers, searched, ref_df)
    plot_nx(nodes, edges)