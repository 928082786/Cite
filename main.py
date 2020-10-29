#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 07:55:47 2020

@author: cx
"""
import pandas as pd
import numpy as np
import cite

with open('/home/cx/LINMUX/Code/python/Utils/ref.txt') as f:
    ref_texts = f.readlines()


cite = cite.Cite()
phrases = []
failures = []
for item in failures_new:
    try:
        ref, bibtex = cite.get_cite(ref_texts[item])
        phrase = cite.phrase_bibtex(bibtex)
        phrase['ref'] = ref
        phrases.append(phrase)
        print('do:', item)
    except:
        print('undo:', item)
        failures.append(item)
        pass

pd_cite = pd.DataFrame(phrases)
pd_cite.to_csv('./ref.csv')