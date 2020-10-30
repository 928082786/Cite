#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 07:55:47 2020

@author: cx
"""
import pandas as pd
import numpy as np
import cite

def get_paper_ref(title):
    phrase = []
    failures = []
    ref_title = cite.dig_ref(title)
    for idx in range(len(ref_title)):
        try:
            ref, bibtex = cite.get_cite(ref_title[idx])
            phrase.append(cite.phrase_bibtex(ref, bibtex))
        except:
            failures.append(idx)
            pass
    
    return phrase

def enhance(failures, ref_title):
    phrase = []
    failure
        
cite = cite.Cite()

ref_df = pd.read_csv('./ref.csv', index_col=0)
searched = pd.read_csv('./searched.csv', index_col=0)
unsearched = pd.read_csv('./unsearched.csv', index_col=0)

phrase = get_paper_ref(searched['title'])

