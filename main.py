#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 07:55:47 2020

@author: cx
"""
import pandas as pd
import numpy as np
import cite
import collections

def unique_title_df(refs_title):
    exist_titles = []
    no_exists_titles = []
    for item in refs_title:
        if item in ref_df['title'].tolist():
            exist_titles.append(item)
        else:
            no_exists_titles.append(item)
            
    return exist_titles, no_exists_titles

def unique_id_df(df):
    for i in df.index:
        if df.loc[i,'id'] in ref_df['id']:
            df = df.drop(i)
    return df


def df_where(exist_titles):
    ref_papers_id = []
    for item in exist_titles:
        idx = ref_df[(ref_df['title']==item)]['id'].tolist()
        ref_papers_id.extend(idx)
    return ref_papers_id


cite = cite.Cite()

ref_df = pd.read_csv('./data/ref.csv', index_col=0)
ref_papers = np.load('./data/ref_paper.npy', allow_pickle=True).tolist()
searched = pd.read_csv('./data/searched.csv', index_col=0)['0'].tolist()
searched = collections.deque(searched)
unsearched = pd.read_csv('./data/unsearched.csv', index_col=0)['0'].tolist()
unsearched = collections.deque(unsearched)


#cite.__init__()
while(len(unsearched)):
    ref_papers_id = []
    pop_title = unsearched.popleft()
    refs_title = cite.dig_onepaper_title(pop_title, mode='ref')
    exist_titles, no_exists_titles = unique_title_df(refs_title)
    no_exists_standard = cite.dig_onepaper_refs_standard(no_exists_titles)
    no_exists_standard = pd.DataFrame(no_exists_standard).drop_duplicates(['id'])
    exist_titles_id = [] if exist_titles is None else df_where(exist_titles)
    ref_papers_id.extend(exist_titles_id)
    ref_papers_id.extend(no_exists_standard['id'].tolist()) if len(no_exists_standard)>0 else None
    ref_papers.append(ref_papers_id)
    
    no_exists_standard = unique_id_df(no_exists_standard)
    ref_df = ref_df.append(no_exists_standard)
    searched.append(pop_title)
    unsearched.extend(no_exists_standard['title'].tolist()) if len(no_exists_standard)>0 else None
    cite.browser.quit()
    cite.__init__()
    
    print('save')
    ref_df.drop_duplicates(['id']).to_csv('./ref.csv')
    pd.DataFrame([i for i in searched]).to_csv('./searched.csv')
    pd.DataFrame([i for i in unsearched]).to_csv('./unsearched.csv')
    np.save('./ref_paper.npy', np.array(ref_papers))  


#clean ref_papers_id
#ref_papers = [list(set(item)) for item in ref_papers]
